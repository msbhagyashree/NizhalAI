
"""NizhalAI: climate guidance and community risk tools."""

import json
import re
from functools import lru_cache
from pathlib import Path

from strands import tool

DATA = Path(__file__).parent / "data"
TAMIL = re.compile(r"[\u0B80-\u0BFF]")


# Tamil words mapped to English keywords used in guidance.json
TAMIL_KEYWORDS = {
    "வெயில்": ["heat", "hot", "sun"],
    "வெப்பம்": ["heat", "temperature"],
    "தண்ணீர்": ["water", "drinking"],
    "நீர்": ["water"],
    "தாகம்": ["water", "drink"],
    "நிழல்": ["shade", "rest"],
    "தலைவலி": ["headache"],
    "மயக்கம்": ["dizziness"],
    "குமட்டல்": ["nausea"],
    "வியர்வை": ["heat", "temperature"],
    "வெப்ப அலை": ["heat", "hot"],
    "மழைநீர்": ["rainwater", "harvesting"],
    "மழை": ["rainwater", "harvesting"],
    "நீர்ப்பற்றாக்குறை": ["water", "conservation"],
    "தெரு": ["outdoor", "worker"],
    "வியாபாரி": ["outdoor", "worker"],
    "தொழிலாளர்": ["outdoor", "worker"],
    "முதியோர்": ["older", "vulnerable"],
    "குழந்தைகள்": ["children", "vulnerable"],
}


@lru_cache(maxsize=1)
def guidance():
    """Load curated climate guidance."""
    path = DATA / "guidance.json"
    return json.loads(path.read_text(encoding="utf-8-sig"))


def guidance_ids():
    return {item["id"] for item in guidance()["items"]}


def language_of(text):
    """Detect Tamil or English based on the script."""
    return "ta" if TAMIL.search(text or "") else "en"


def has_tamil(text):
    return bool(TAMIL.search(text or ""))


def expand_tamil_keywords(topic):
    """Convert recognized Tamil keywords into English search keywords."""
    words = [
        word for word in re.findall(r"\w+", topic.lower())
        if len(word) > 2
    ]

    for tamil_word, english_words in TAMIL_KEYWORDS.items():
        if tamil_word in topic:
            words.extend(english_words)

    return list(set(words))


@tool
def lookup_guidance(topic: str) -> list[dict]:
    """Find official curated climate guidance.

    Supports common Tamil and English climate-related keywords.

    Args:
        topic: Climate topic or keywords to search.
    """
    words = expand_tamil_keywords(topic)

    if not words:
        return []

    items = guidance()["items"]

    hits = [
        item for item in items
        if any(
            word in (
                item["id"] + " " + item["text"]
            ).lower()
            for word in words
        )
    ]

    return [
        {
            "id": item["id"],
            "text": item["text"],
            "source": guidance()["sources"][item["source"]]
        }
        for item in hits[:6]
    ]


@tool
def analyze_heat_risk(
    temperature_c: float,
    humidity_percent: float,
    outdoor_work_hours: float,
    is_vulnerable: bool
) -> dict:
    """Estimate preliminary heat-exposure risk from user inputs.

    This is an illustrative screening rule, NOT an official IMD heat
    index, validated prediction, or medical diagnosis.

    Args:
        temperature_c: Air temperature in Celsius.
        humidity_percent: Relative humidity from 0 to 100.
        outdoor_work_hours: Hours spent working outdoors per day.
        is_vulnerable: Whether the person is elderly, a child, or has
            a health condition that increases heat vulnerability.
    """
    if not 0 <= humidity_percent <= 100:
        return {"error": "Humidity must be between 0 and 100 percent."}

    if not 0 <= outdoor_work_hours <= 24:
        return {"error": "Outdoor work hours must be between 0 and 24."}

    if not -10 <= temperature_c <= 60:
        return {"error": "Please enter a plausible temperature in Celsius."}

    score = 0

    if temperature_c >= 40:
        score += 3
    elif temperature_c >= 35:
        score += 2
    elif temperature_c >= 30:
        score += 1

    if humidity_percent >= 70:
        score += 2
    elif humidity_percent >= 50:
        score += 1

    if outdoor_work_hours >= 6:
        score += 2
    elif outdoor_work_hours >= 3:
        score += 1

    if is_vulnerable:
        score += 2

    if score >= 7:
        risk = "High"
    elif score >= 4:
        risk = "Moderate"
    else:
        risk = "Lower"

    return {
        "risk_level": risk,
        "screening_score": score,
        "message": (
            "This is a preliminary screening estimate based only "
            "on the values provided. It is not an official weather "
            "alert or a validated heat-index calculation."
        )
    }


@tool
def create_preparedness_plan(
    occupation: str,
    community: str,
    main_concern: str
) -> dict:
    """Create a preliminary community climate-preparedness plan.

    Args:
        occupation: Example: street vendor, construction worker, farmer.
        community: Example: Madurai neighbourhood or village.
        main_concern: Example: extreme heat, water shortage, or both.
    """
    return {
        "community": community,
        "occupation": occupation,
        "main_concern": main_concern,
        "suggested_actions": [
            "Identify people who may need extra help during extreme heat.",
            "Identify accessible drinking-water points.",
            "Identify shaded places where outdoor workers can rest.",
            "Share verified local weather warnings.",
            "Discuss practical water-saving and rainwater-harvesting options."
        ],
        "note": (
            "This is a preliminary planning checklist. "
            "Confirm local conditions and resources with the community."
        )
    }
