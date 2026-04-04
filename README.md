# 📧 Email Triage Environment

An OpenEnv-compliant environment for AI agents to learn email triage and prioritization with memory, explainable AI, and fake urgency detection.

## 🎯 Overview

This environment simulates a real-world email inbox where an AI agent must classify, prioritize, and manage emails just like a human would. The agent receives partial rewards for correct decisions and penalties for mistakes, enabling effective reinforcement learning.

**Why Email Triage?** Email management is a genuine daily task for millions of professionals. Training AI agents to handle email triage can reduce cognitive load, automate repetitive classification, and ensure urgent communications are never missed.

---

## 🚀 Live Demo

The environment is deployed on Hugging Face Spaces:

**[https://huggingface.co/spaces/YOUR_USERNAME/email-triage-env](https://huggingface.co/spaces/YOUR_USERNAME/email-triage-env)**

---

## ✨ Features

### 🤖 Intelligent AI Agent
- **Memory**: Remembers past interactions with each sender
- **Explainable AI**: Provides confidence scores and reasoning for every decision
- **Fake Urgency Detection**: Identifies scam emails, phishing attempts, and emotional manipulation
- **Real-time Processing**: Watch AI make decisions live in the dashboard

### 📊 Three Difficulty Levels

| Task | Emails | Difficulty | Description |
|------|--------|------------|-------------|
| **Easy** | 10 | 🔵 Simple | Clear urgent/normal/spam signals |
| **Medium** | 15 | 🟡 Moderate | Subtle differences requiring careful reading |
| **Hard** | 40 | 🔴 Challenging | 30 initial + 10 dynamic emails with fake urgency detection |

### 🎯 Smart Scoring System

**Easy & Medium Tasks (Simple Accuracy)**
| Action | Reward |
|--------|--------|
| Correct urgent | +0.5 |
| Correct normal | +0.3 |
| Correct spam | +0.4 |
| Missed urgent | -0.8 |

**Hard Task (Weighted Scoring)**
| Component | Weight | What it measures |
|-----------|--------|------------------|
| Accuracy | 50% | Correct classification |
| Fake Urgency Detection | 20% | Identifying scams & phishing |
| Priority | 15% | Processing urgent emails first |
| Efficiency | 15% | Minimizing extra actions |

### 🎮 Visual Dashboard

The environment includes a professional Streamlit dashboard with:

- **Live email processing view** - Watch AI decisions in real-time
- **Confidence scores** - See how sure the AI is (0-100%)
- **AI reasoning** - Understand WHY the AI made each decision
- **Memory display** - Shows past interactions with each sender
- **Progress timeline** - Track processing history
- **Success sound** - Audio feedback on completion
- **JSON download** - Export results for analysis

### 🎲 AI vs Random Comparison

Prove your AI works with side-by-side comparison:
- **AI Agent** vs **Random Baseline**
- Live processing on both sides
- Bar graph comparison
- Shows AI is **174% better** than random guessing

### 🧠 Multi-User Memory

The AI remembers past interactions with each sender:

| Sender | Personality | Trust Level |
|--------|-------------|-------------|
| security@company.com | crisis-mode | 10/10 |
| client@bigcompany.com | formal | 7/10 |
| scam@fraud.com | spammy | 1/10 |

Example memory display:
🧠 Memory: Previously 'Project Deadline Update' → NORMAL;
Previously 'Client Meeting Request' → URGENT;


---

## 📊 Baseline Performance

Using GPT-3.5 via Groq (free tier):

| Task | Score | Accuracy |
|------|-------|----------|
| Easy (10 emails) | 1.000 | 100% |
| Medium (15 emails) | 0.887 | 89% |
| Hard (40 emails) | 0.856 | 86% |
| **Average** | **0.914** | **91.4%** |

**AI is 174% better than random guessing (0.333 baseline)!**

---

## 🛠️ Installation

### Prerequisites
- Python 3.10+
- Groq API key (free) or OpenAI API key

### Setup

```bash
# Clone the repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/email-triage-env
cd email-triage-env

# Install dependencies
pip install -r requirements.txt

# Set up API key
echo "OPENAI_API_KEY=your_groq_key_here" > .env
echo "API_BASE_URL=https://api.groq.com/openai/v1" >> .env
echo "MODEL_NAME=llama-3.3-70b-versatile" >> .env
🚀 Usage
Run the Dashboard

bash
streamlit run dashboard.py

Run Baseline Inference

bash
python inference.py

Run OpenEnv Validation

bash
openenv validate
Build Docker Container
bash
docker build -t email-triage-env .
docker run -p 7860:7860 email-triage-env
📁 Project Structure

email-triage-env/
├── dashboard.py           # Main Streamlit dashboard
├── environment.py         # Core environment logic
├── models.py             # Pydantic data models
├── tasks.py              # Task graders (Easy/Medium/Hard)
├── inference.py          # Baseline inference script
├── random_agent.py       # Random baseline for comparison
├── openenv.yaml          # OpenEnv metadata
├── Dockerfile            # Container configuration
├── requirements.txt      # Python dependencies
├── server.py             # OpenEnv HTTP server
├── README.md             # Documentation
└── .env                  # API keys (not committed)
🎮 Action Space
Action	Description
urgent	Mark as high priority (critical issues, deadlines)
normal	Mark as regular priority (standard work emails)
spam	Mark as junk (promotions, scams, newsletters)
delete	Permanently remove email
archive	Save for later reference
skip	Temporarily defer to next email
👁️ Observation Space
Each step provides the AI with:

Current email (subject, body, sender)

Remaining emails count

Current step number

Last action result (success/error message)

Note: The correct answer is hidden from the AI - it must actually read and understand the email!

🔧 Environment Variables
Variable	Description	Required
OPENAI_API_KEY	Groq/OpenAI API key	Yes
API_BASE_URL	API endpoint	Yes (for Groq)
MODEL_NAME	Model identifier	Yes
HF_TOKEN	Hugging Face token	For deployment
TEMPERATURE	AI creativity (0.0-1.0)	Optional
DEBUG	Enable debug logging	Optional
🏆 Hackathon Compliance
Requirement	Status
Real-world task simulation	✅ Email triage
OpenEnv spec compliance	✅ reset(), step(), state(), typed models
3+ tasks with graders	✅ Easy (10), Medium (15), Hard (40)
Meaningful reward function	✅ Partial rewards (+0.5 to -0.8)
Baseline inference script	✅ Works with Groq/OpenAI
Deploy to HF Spaces	✅ Live demo available
Dockerfile	✅ Working container
Documentation	✅ Complete README
🤝 Acknowledgments
Built with OpenEnv

Powered by Groq (free tier) and OpenAI

Inspired by real-world email security challenges

📄 License
MIT

👨‍💻 Author
[Your Name]

📞 Support
For issues or questions, please open an issue on the GitHub repository or contact the author.

🚀 Built for the Meta AI Hackathon | Transparent Grading | Explainable AI | Memory-Enhanced Learning