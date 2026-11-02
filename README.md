# NizhalAI 🌿

### A Tamil-English AI Assistant for Community Climate Preparedness

NizhalAI is an AI-powered community climate-safety assistant designed to help people understand heat-related risks, adopt safer practices, conserve water, and prepare for climate challenges.

Built using **Python, AWS Strands Agents, Amazon Bedrock Nova 2 Lite, and Streamlit**, NizhalAI aims to make practical climate-safety guidance accessible through English and Tamil.

## 🌍 Problem Statement

Communities facing extreme heat and water stress need accessible, understandable, and actionable information.

Language barriers, limited awareness, and a lack of practical preparedness guidance can make climate-related risks more difficult to manage.

NizhalAI addresses this challenge through a conversational AI assistant that provides community-focused climate guidance.

## ✨ Key Features

- **Heat Risk Analyzer:** Provides preliminary heat-risk screening using temperature, humidity, outdoor work duration, and vulnerability factors.
- **Heat Safety Assistant:** Offers practical guidance for heat exposure, hydration, protective clothing, and outdoor work safety.
- **Water Conservation Advisor:** Shares water-saving and rainwater-harvesting guidance.
- **Community Preparedness Planner:** Generates actionable preparedness suggestions based on occupation, community, and primary concern.
- **Tamil-English Support:** Supports climate-safety interactions in English and Tamil.
- **Emergency Escalation:** Detects selected emergency-related phrases and provides immediate safety guidance instead of proceeding with a normal AI response.

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python 3.12 |
| Agent framework | AWS Strands Agents |
| AI model | Amazon Nova 2 Lite |
| AI infrastructure | Amazon Bedrock |
| Frontend | Streamlit |
| Data format | JSON |
| Validation | Pydantic |

## 🏗️ Project Structure

```text
NizhalAI/
│
├── agent/
│   ├── app.py
│   ├── tools.py
│   ├── plan.py
│   └── data/
│       └── guidance.json
│
├── app/
│   └── app.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.12
- AWS account with Amazon Bedrock access
- Access to the Amazon Nova 2 Lite model

### 1. Clone the repository

```powershell
git clone YOUR_GITHUB_REPOSITORY_URL
cd NizhalAI
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 5. Configure Amazon Bedrock

Set your Bedrock API key as an environment variable in PowerShell:

```powershell
$env:AWS_BEARER_TOKEN_BEDROCK = "YOUR_BEDROCK_API_KEY"
```

Do not commit API keys or credentials to GitHub.

### 6. Launch NizhalAI

```powershell
python -m streamlit run app/app.py
```

Open the local URL displayed in your terminal to interact with NizhalAI.

## 🧠 How It Works

1. The user submits a climate-related question through the Streamlit interface.
2. The application identifies the language and checks for selected emergency-related phrases.
3. For normal queries, the Strands agent uses the available tools and relevant guidance data.
4. Amazon Bedrock powers the conversational response.
5. The application presents the answer, recommended actions, escalation guidance, and relevant guidance references.

## 📚 Guidance Sources

The current guidance dataset includes material from:

- India Meteorological Department (IMD) — Heat safety and heat-stress guidance.
- Central Ground Water Board (CGWB) — Rainwater harvesting guidance.

## ⚠️ Safety and Limitations

- Heat-risk screening is an illustrative preliminary assessment, not an official IMD heat index or medically validated risk score.
- NizhalAI does not replace official weather alerts, emergency services, or professional medical advice.
- Emergency phrase detection covers selected English and Tamil expressions; it cannot guarantee detection of every emergency.
- The application does not claim to provide live weather conditions or verified live alerts unless connected to an authoritative live data source.

## 🎯 Project Vision

NizhalAI aims to make climate preparedness more accessible by combining AI assistance, local-language interaction, and practical community-focused guidance.

**Building safer communities, one informed action at a time.**