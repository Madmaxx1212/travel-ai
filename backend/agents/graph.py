"""
AI Travel Guardian+ — LangGraph Multi-Agent Pipeline
Wires all 7 agents into a state graph with conditional routing.
"""

import json
from typing import Optional
from agents.state import TravelState
from agents.intent_agent import intent_agent
from agents.flight_agent import flight_agent
from agents.risk_agent import risk_agent
from agents.explanation_agent import explanation_agent
from agents.hotel_agent import hotel_agent
from agents.itinerary_agent import itinerary_agent
from agents.replan_agent import replan_agent
from ml.delay_predictor import FlightDelayPredictor
from llm.groq_client import GroqLLMClient
from llm.prompts import GENERAL_CHAT_PROMPT
from rag.retriever import RAGRetriever
from utils.helpers import IATA_TO_CITY


class TravelAgentPipeline:
    """Orchestrates the 7-agent pipeline for travel planning."""

    def __init__(self, llm_client: GroqLLMClient, delay_predictor: FlightDelayPredictor,
                 rag_retriever: Optional[RAGRetriever] = None):
        self.llm = llm_client
        self.delay_predictor = delay_predictor
        self.rag = rag_retriever

    def run(self, state: TravelState) -> TravelState:
        """Execute the multi-agent pipeline based on user input."""
        try:
            # Step 1: Intent extraction (always runs first)
            intent_updates = intent_agent(state, self.llm)
            state.update(intent_updates)

            # If clarification needed, return early
            if state.get("needs_clarification"):
                state["response_type"] = "clarification"
                return state

            # Check if this is a replan request (if existing trip data)
            has_existing_trip = state.get("ranked_flights") or state.get("itinerary")
            if has_existing_trip:
                replan_updates = replan_agent(state, self.llm)
                state.update(replan_updates)

                if state.get("requires_replanning"):
                    return self._handle_replan(state)

            # Check if we have enough info for a full search
            source = state.get("source")
            destination = state.get("destination")

            if not source or not destination:
                # General chat / question
                return self._handle_general_chat(state)

            # Step 2: Flight search + ranking
            flight_updates = flight_agent(state, self.delay_predictor)
            state.update(flight_updates)

            if not state.get("ranked_flights"):
                return self._handle_general_chat(state)

            # Step 3: Risk analysis
            risk_updates = risk_agent(state, self.llm)
            state.update(risk_updates)

            # Step 4: Explanation generation
            expl_updates = explanation_agent(state, self.llm)
            state.update(expl_updates)

            # Step 5: Hotel recommendations
            hotel_updates = hotel_agent(state, self.llm)
            state.update(hotel_updates)

            # Step 6: Itinerary + food recommendations (always run when trip found)
            if not state.get("num_days"):
                state["num_days"] = 3  # default to 3 days
            itin_updates = itinerary_agent(state, self.llm)
            state.update(itin_updates)

            # Compose final response
            state["response_type"] = "trip_plan"
            state["response_text"] = self._compose_response(state)

            return state

        except Exception as e:
            state["error"] = str(e)
            state["response_type"] = "general"
            state["response_text"] = f"I encountered an issue while planning your trip. Please try again. (Error: {str(e)[:100]})"
            return state

    def _handle_replan(self, state: TravelState) -> TravelState:
        """Handle replanning based on change type."""
        change_type = state.get("replan_change_type", "no_change")

        if change_type in ("date_change", "priority_change"):
            flight_updates = flight_agent(state, self.delay_predictor)
            state.update(flight_updates)
            risk_updates = risk_agent(state, self.llm)
            state.update(risk_updates)
            expl_updates = explanation_agent(state, self.llm)
            state.update(expl_updates)

        elif change_type in ("duration_change",):
            itin_updates = itinerary_agent(state, self.llm)
            state.update(itin_updates)

        elif change_type in ("budget_change",):
            hotel_updates = hotel_agent(state, self.llm)
            state.update(hotel_updates)
            # Re-rank flights with new budget
            flight_updates = flight_agent(state, self.delay_predictor)
            state.update(flight_updates)

        elif change_type in ("passenger_change",):
            pass  # Just update cost

        elif change_type in ("destination_change",):
            # Full replan
            flight_updates = flight_agent(state, self.delay_predictor)
            state.update(flight_updates)
            if state.get("ranked_flights"):
                risk_updates = risk_agent(state, self.llm)
                state.update(risk_updates)
                expl_updates = explanation_agent(state, self.llm)
                state.update(expl_updates)
            hotel_updates = hotel_agent(state, self.llm)
            state.update(hotel_updates)
            if not state.get("num_days"):
                state["num_days"] = 3
            itin_updates = itinerary_agent(state, self.llm)
            state.update(itin_updates)

        state["response_type"] = "replan"
        confirm = state.get("response_text", "")
        state["response_text"] = confirm or "[OK] Your trip plan has been updated!"
        return state

    def _handle_general_chat(self, state: TravelState) -> TravelState:
        """Handle general questions via LLM with RAG context."""
        user_message = state.get("user_message", "")
        conversation_history = state.get("conversation_history", [])

        # Build context
        context = "\n".join([
            f"{msg.get('role', 'user')}: {msg.get('content', '')}"
            for msg in conversation_history[-6:]
        ])

        trip_context = ""
        if state.get("destination"):
            dest_city = IATA_TO_CITY.get(state["destination"], state["destination"])
            trip_context = f"Active trip: {state.get('source', 'N/A')} → {dest_city}, {state.get('travel_date', 'TBD')}, {state.get('num_days', 'N/A')} days, {state.get('budget', 'medium')} budget"

        rag_context = ""
        if self.rag and self.rag.is_initialized:
            rag_context = self.rag.retrieve_context(user_message, k=3)

        prompt = GENERAL_CHAT_PROMPT.format(
            context=context or "No prior context",
            trip_context=trip_context or "No active trip",
            rag_context=rag_context or "No additional context",
        )

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message},
        ]

        try:
            response = self.llm.chat(messages, model=self.llm.fast_model, temperature=0.5, max_tokens=500)
        except Exception:
            response = "I'm having trouble connecting to my AI backend right now. Could you try again in a moment?"

        state["response_type"] = "general"
        state["response_text"] = response
        return state

    def _compose_response(self, state: TravelState) -> str:
        """Compose the final trip plan response text."""
        parts = []

        # Flight explanation
        explanation = state.get("flight_explanation", "")
        if explanation:
            parts.append(explanation)

        # Risk warnings summary
        warnings = state.get("risk_warnings", [])
        if warnings:
            red_warnings = [w for w in warnings if w.get("severity") == "red"]
            if red_warnings:
                parts.append("\n**Important Warnings:**")
                for w in red_warnings:
                    parts.append(f"  [!] {w.get('message', '')}")

        # Hotel summary
        hotels = state.get("recommended_hotels", [])
        if hotels:
            top_hotel = hotels[0]
            parts.append(f"\n**Top Hotel Pick:** {top_hotel.get('name', 'N/A')} -- Rs.{top_hotel.get('price_per_night', 0):,.0f}/night, {top_hotel.get('rating', 0)}/5 rating")

        # Itinerary summary
        itinerary = state.get("itinerary", {})
        if itinerary and "days" in itinerary:
            num_days = len(itinerary["days"])
            parts.append(f"\nI've prepared a **{num_days}-day itinerary** for you. Check the trip panel for the full day-by-day plan!")

        return "\n".join(parts) if parts else "Here's your trip plan! Check the panel on the right for all details."
