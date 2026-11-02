
"""NizhalAI: Tamil-English community climate safety assistant."""

import argparse
import json
import logging
import os
import sys
import time

from strands import Agent
from strands.models import BedrockModel

from . import tools
from .plan import Answer


MODEL_ID = os.environ.get(
    "SHIP_MODEL",
    "global.amazon.nova-2-lite-v1:0"
)

REGION = os.environ.get(
    "AWS_REGION",
    "ap-southeast-2"
)

logging.getLogger("strands").setLevel(logging.WARNING)


SYSTEM_PROMPT = """
You are NizhalAI, a Tamil-English community climate safety assistant.

MISSION:
Help communities understand heat exposure, water stress, and
practical climate preparedness.

AVAILABLE TOOLS:
1. lookup_guidance: Retrieve curated climate safety guidance.
2. analyze_heat_risk: Estimate preliminary heat-exposure risk.
3. create_preparedness_plan: Create a community preparedness plan.

LANGUAGE RULES:
- Respond in the same language as the user.
- If the user writes in Tamil, respond entirely in natural Tamil script.
- If the user writes in English, respond in English.
- Use simple, fluent language that ordinary people can understand.
- Use correct Tamil terms such as:
  குடிநீர், நிழல் பகுதி, வெப்ப அழுத்தம், உடல்நலப் பாதிப்பு.
- Translate recommendations naturally. Do not produce word-for-word
  translations that sound unnatural.

SAFETY AND ACCURACY:
- Use the tools whenever relevant.
- Use only guidance supported by the tools.
- Cite only guidance IDs actually returned by lookup_guidance.
- Never invent official weather alerts, temperatures, or forecasts.
- Never present an illustrative risk score as an official IMD measurement.
- Do not invent a fixed daily water-intake target.
- Do not diagnose medical conditions.
- Do not recommend unsupported treatments or diets.
- If someone reports unconsciousness, seizures, confusion, or suspected
  heat stroke, advise them to seek emergency medical help immediately.
- Do not claim to have contacted emergency services.
- Ask for missing information instead of guessing.

RECOMMENDATIONS:
- Pay special attention to outdoor workers, street vendors,
  older adults, children, and vulnerable communities.
- Give short, practical, actionable recommendations.
- Mention drinking water, shade, rest breaks, and safer working hours
  when relevant.
- Explain risk estimates in simple language.

OUTPUT:
Return the answer using the required structured output fields:
language, answer, steps, escalation, and citations.
"""


def _model():
    return BedrockModel(
        model_id=MODEL_ID,
        region_name=REGION,
        temperature=0.2
    )


def build_agent():
    return Agent(
        model=_model(),
        name="NizhalAI",
        system_prompt=SYSTEM_PROMPT,
        tools=[
            tools.lookup_guidance,
            tools.analyze_heat_risk,
            tools.create_preparedness_plan
        ],
        structured_output_model=Answer,
        callback_handler=None
    )


def emergency_response(language):
    if language == "ta":
        return Answer(
            language="ta",
            answer=(
                "இது அவசர மருத்துவ நிலையாக இருக்கலாம். "
                "உடனடியாக அவசர மருத்துவ உதவியை நாடுங்கள்."
            ),
            steps=[
                "உடனடியாக மருத்துவ உதவியைப் பெறுங்கள்.",
                "மருத்துவ உதவி பெறுவதைத் தாமதிக்காதீர்கள்."
            ],
            escalation=(
                "உடனடியாக அவசர மருத்துவ உதவியை நாடுங்கள்."
            ),
            citations=[]
        )

    return Answer(
        language="en",
        answer=(
            "This may be a medical emergency. "
            "Seek emergency medical help immediately."
        ),
        steps=[
            "Get emergency medical assistance immediately.",
            "Do not delay seeking medical care."
        ],
        escalation="Seek emergency medical help immediately.",
        citations=[]
    )


def run(case: dict) -> dict:
    start_time = time.time()

    user_text = case["text"]
    language = case.get("lang") or tools.language_of(user_text)

    # Emergency detection in English and Tamil
    emergency_terms = [
        # English emergency terms
        "unconscious",
        "seizure",
        "convulsion",
        "heat stroke",
        "heatstroke",
        "fainted",
        "fainting",
        "passed out",
        "not responding",
        "loss of consciousness",
        "severe confusion",
        "suddenly confused",

        # Tamil emergency terms
        "மயங்கி விழுந்த",
        "நினைவிழந்த",
        "நினைவற்ற",
        "வலிப்பு",
        "வலிப்பு ஏற்பட்ட",
        "பேச்சு குழறல்",
        "குழப்ப நிலையில்"
    ]

    normalized_text = user_text.lower()

    is_emergency = any(
        term in normalized_text
        for term in emergency_terms
    )

    # Handle emergencies without waiting for the AI model
    if is_emergency:
        answer = emergency_response(language)

        return {
            "plan": answer.model_dump(),
            "meta": {
                "path": "emergency_handoff",
                "latency_ms": int(
                    (time.time() - start_time) * 1000
                )
            }
        }

    # Normal AI agent response
    agent = build_agent()

    response = agent(
        f"User language: {language}\n"
        f"User question: {user_text}"
    )

    answer = response.structured_output

    # Diagnostic information if structured output is missing
    if answer is None:
        print("\n========== NIZHALAI DEBUG ==========")

        print("\nRaw Strands response:")
        print(response)

        print("\nResponse message:")
        print(
            getattr(
                response,
                "message",
                "No message available"
            )
        )

        print("\nStructured output:")
        print(
            getattr(
                response,
                "structured_output",
                None
            )
        )

        print("\n====================================")

        raise RuntimeError(
            "NizhalAI did not return structured output. "
            "Check the debug information above."
        )

    return {
        "plan": answer.model_dump(),
        "meta": {
            "path": "agent",
            "latency_ms": int(
                (time.time() - start_time) * 1000
            )
        }
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="python -m agent.app",
        description="NizhalAI climate safety assistant"
    )

    parser.add_argument(
        "text",
        help="Your question for NizhalAI"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Display the complete JSON response"
    )

    args = parser.parse_args(argv)

    result = run({
        "text": args.text
    })

    if args.json:
        print(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2
            )
        )
    else:
        plan = result["plan"]

        print("\n" + plan["answer"])

        if plan["steps"]:
            print("\nSuggested actions:")

            for step in plan["steps"]:
                print("- " + step)

        if plan["escalation"]:
            print("\nWhen to seek help:")
            print(plan["escalation"])

        if plan["citations"]:
            print("\nGuidance references:")
            print(", ".join(plan["citations"]))

    return 0


if __name__ == "__main__":
    sys.exit(main())
