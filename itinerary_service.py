import os
from datetime import date

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API"))


def generate_itinerary(
    destination: str,
    start_date: date,
    end_date: date,
    places: str,
    food: str,
    activities: str,
    budget: float,
) -> str:
    prompt = f"""
    You are a professional travel planner.
    Create a **detailed, human-readable travel itinerary** with clear explanations and cost estimation.

    Destination: {destination}
    Travel Dates: {start_date} to {end_date}
    Places to Visit: {places}
    Food Preferences: {food}
    Activities: {activities}
    Budget: {budget}

    Provide, in order:
    1. A short high-level trip overview (2–4 sentences).
    2. A **day-wise itinerary**, with each day clearly labeled (e.g. "Day 1 – Arrival and City Exploration").
    3. For each day:
       - Places to visit with brief explanations.
       - Food recommendations with reasons (local specialties, budget level).
       - Activities with short descriptions and timing suggestions.
       - An **estimated daily cost** with a short breakdown (transport, activities, food, etc.).
    4. A final **trip summary section** that explains the trip flow in plain English.
    5. A clearly separated line at the very end in the exact format:
       "Total Estimated Cost: <currency> <amount>"

    Very important formatting rules:
    - DO NOT use CSV, tables, or markdown table syntax.
    - Use headings and bullet points where helpful, but keep everything as readable text.
    - Make sure the last line of the entire response is exactly the total cost line.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional travel planner."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content

