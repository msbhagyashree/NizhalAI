# NizhalAI — A Tamil-English AI Assistant for Community Climate Preparedness

## The Problem

Every summer, extreme heat claims lives across India — and the people most at risk are often the least equipped to protect themselves. Street vendors, construction workers, farmers, and older adults spend long hours outdoors with limited access to reliable safety information. When guidance *is* available, it is rarely in their language.

NizhalAI was built to close that gap. The name "Nizhal" (நிழல்) means *shade* in Tamil — the simplest, most immediate protection against the sun.

---

## Who It Helps

NizhalAI is designed for:

- **Outdoor workers and street vendors** who need practical, immediate heat-safety guidance.
- **Community residents** who want to understand water conservation and rainwater harvesting.
- **Older adults and caregivers** who need to recognise heat-stress symptoms and know when to seek help.
- **Tamil-speaking communities** for whom English-only tools are a barrier.

---

## What NizhalAI Does

NizhalAI is a conversational AI assistant powered by **AWS Strands Agents** and **Amazon Bedrock (Nova 2 Lite)**. It supports both English and Tamil and provides:

| Feature | What it does |
|---|---|
| Heat Safety Assistant | Practical guidance for hydration, clothing, rest breaks, and safer working hours |
| Heat Risk Analyzer | Preliminary heat-exposure screening using temperature, humidity, outdoor work duration, and vulnerability |
| Water Conservation Advisor | Rainwater-harvesting and water-saving guidance from CGWB sources |
| Community Preparedness Planner | Occupation-specific preparedness checklists for communities |
| Emergency Escalation | Detects emergency phrases (English and Tamil) and immediately provides emergency guidance |
| Tamil-English Support | Responds in the user's language — natural Tamil script or English |

---

## How It Works

```
User question (English or Tamil)
        │
        ▼
Language detection + Emergency phrase check
        │
   Emergency?─────YES──► Immediate emergency guidance (no AI call)
        │
       NO
        ▼
  Strands Agent (Nova 2 Lite on Bedrock)
        │
   ┌────┴────────────────────────┐
   │  Tools available:           │
   │  • lookup_guidance          │
   │  • analyze_heat_risk        │
   │  • create_preparedness_plan │
   └────────────────────────────┘
        │
        ▼
  Structured response (answer, steps, escalation, citations)
        │
        ▼
  Streamlit UI — displayed to user
```

The agent uses a curated guidance dataset sourced from:
- **India Meteorological Department (IMD)** — heat safety and heat-stress guidance.
- **Central Ground Water Board (CGWB)** — rainwater harvesting guidance.

All citations refer to real guidance IDs. The agent is instructed never to invent weather alerts, temperatures, or medical diagnoses.

---

## Demo Results

The agent was tested against five real community scenarios:

| Case | Language | Scenario | Result |
|---|---|---|---|
| nizhal-01 | English | Heat safety tips for street vendors in Madurai | ✅ Practical tips, water & shade cited |
| nizhal-02 | Tamil | How to protect yourself working in the sun | ✅ Full Tamil response |
| nizhal-03 | English | Community rainwater conservation | ✅ Rainwater guidance cited |
| nizhal-04 | English | Worker has fainted due to extreme heat | ✅ Emergency handoff, no AI delay |
| nizhal-05 | Tamil | Person fainted due to heat — what to do? | ✅ Tamil emergency guidance |

**Demo video runtime: 34.6 seconds** — well under the 3-minute limit.

Sample output for an everyday heat-safety query:

> *"Stay hydrated — drink water regularly, even if you don't feel thirsty. Wear loose, light-colored cotton clothes and use a hat or umbrella for shade. Plan your work for cooler hours (early morning or late evening) and take frequent short breaks."*

---

## A Failure We Found and Fixed

Running the starter-kit tools on Windows revealed three real issues:

1. **Cases without temperature fields** caused the `cases show` command to crash with a `KeyError`.
2. **BOM-formatted JSON** caused silent parsing errors.
3. **Chromium subprocess output** triggered a `UnicodeDecodeError` on Windows.

We fixed all three — updating `ship_kit/cases.py`, `ship_kit/cli.py`, and `ship_kit/video.py` — and verified that all five cases displayed correctly and the demo video generated successfully.

This is logged in full in [FAILURES.md](../FAILURES.md).

---

## What I Learned

Building NizhalAI taught me several things:

**On Strands Agents:** Structured output with `structured_output_model` is a clean pattern for enforcing consistent response shapes. The tool-decorator approach (`@tool`) makes adding domain tools straightforward.

**On multilingual AI:** Getting natural Tamil responses requires more than just switching the language tag. The system prompt needs explicit guidance on vocabulary (குடிநீர், நிழல் பகுதி, வெப்ப அழுத்தம்) and an instruction to translate naturally rather than word-for-word.

**On safety:** Pre-model emergency detection is the right pattern for life-safety systems. Routing phrases like "fainted" or "மயங்கி விழுந்த" to a hardcoded response — before any AI call — means the emergency path has no latency and no hallucination risk.

**On grounding:** Citing only guidance IDs that are actually returned by `lookup_guidance` prevents the model from inventing official sources. Small system-prompt constraints go a long way.

---

## Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python 3.12 |
| Agent framework | AWS Strands Agents SDK |
| AI model | Amazon Nova 2 Lite |
| AI infrastructure | Amazon Bedrock |
| Frontend | Streamlit |
| Validation | Pydantic |
| Data format | JSON (IMD + CGWB guidance) |

---

## Source Code

GitHub: [https://github.com/msbhagyashree/NizhalAI](https://github.com/msbhagyashree/NizhalAI)

---

*NizhalAI — Building safer, climate-resilient communities through AI.*
