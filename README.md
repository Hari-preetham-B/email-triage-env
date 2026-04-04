---
title: Email Triage AI
emoji: 📧
colorFrom: purple
colorTo: pink
sdk: docker
sdk_version: "1.0"
app_port: 7860
pinned: false
---

# 📧 Email Triage Environment

An OpenEnv-compliant environment for AI agents to learn email triage and prioritization with memory, explainable AI, and fake urgency detection.

## 🎯 Overview

This environment simulates a real-world email inbox where an AI agent must classify, prioritize, and manage emails just like a human would. The agent receives partial rewards for correct decisions and penalties for mistakes, enabling effective reinforcement learning.

**Why Email Triage?** Email management is a genuine daily task for millions of professionals. Training AI agents to handle email triage can reduce cognitive load, automate repetitive classification, and ensure urgent communications are never missed.

## 🚀 Live Demo

This Space is deployed at:
**[https://huggingface.co/spaces/Haripreetham/email-triage-env](https://huggingface.co/spaces/Haripreetham/email-triage-env)**

## 🔧 Environment Variables (Required for Testing)

This Space requires the following secrets to be configured in Settings → Repository secrets:

| Secret Name | Value Example | Description |
|-------------|---------------|-------------|
| `OPENAI_API_KEY` | `gsk_xxx...` | Groq or OpenAI API key |
| `API_BASE_URL` | `https://api.groq.com/openai/v1` | API endpoint URL |
| `MODEL_NAME` | `llama-3.3-70b-versatile` | Model identifier |

**Note for evaluators:** Please add your own API keys as secrets before testing the Space.

## ✨ Features

### 🤖 Intelligent AI Agent
- **Memory**: Remembers past interactions with each sender
- **Explainable AI**: Provides confidence scores and reasoning for every decision
- **Fake Urgency Detection**: Identifies scam emails, phishing attempts, and emotional manipulation
- **Real-time Processing**: Watch AI make decisions live in the dashboard

### 📊 Three Difficulty Levels

| Task | Emails | Difficulty | Description |
|------|--------|------------|-------------|
| **Easy** | 12 | 🔵 Simple | Clear urgent/normal/spam signals |
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
| Accuracy | 70% | Correct classification |
| Efficiency | 20% | Minimizing extra actions |
| Priority | 10% | Processing urgent emails first |

### 🎮 Visual Dashboard with 3 Modes

The environment includes a professional Streamlit dashboard with three modes:

#### 1. 🚀 NORMAL MODE
- Run AI on all 3 tasks
- Live email processing with confidence scores
- Memory display showing past interactions
- Progress timeline and success sound
- JSON results download

#### 2. 🎲 AI vs RANDOM MODE
- Compare AI performance against random baseline
- Side-by-side live processing
- Bar graph comparison
- Shows AI improvement percentage

#### 3. 📝 EDIT EMAILS MODE
- View, edit, add, or delete emails for each task
- Save custom email templates to JSON
- Changes automatically used in NORMAL MODE
- No coding required to create test cases

### 🧠 Multi-User Memory

The AI remembers past interactions with each sender. Example memory display:
🧠 Memory: Previously 'Project Deadline Update' → NORMAL;
Previously 'Client Meeting Request' → URGENT;

text

## 📊 Baseline Performance

Using GPT-3.5 / Groq (with proper API keys):

| Task | Score | Accuracy |
|------|-------|----------|
| Easy (12 emails) | 1.000 | 100% |
| Medium (15 emails) | 0.887 | 89% |
| Hard (40 emails) | 0.908 | 91% |
| **Average** | **0.932** | **93.2%** |

**AI is approximately 180% better than random guessing (0.333 baseline)!**

## 🛠️ Local Installation

### Prerequisites
- Python 3.10+
- Groq API key (free) or OpenAI API key

### Setup

```bash
# Clone the repository
git clone https://huggingface.co/spaces/Haripreetham/email-triage-env
cd email-triage-env

# Install dependencies
pip install -r requirements.txt

# Set up API key
echo "OPENAI_API_KEY=your_groq_key_here" > .env
echo "API_BASE_URL=https://api.groq.com/openai/v1" >> .env
echo "MODEL_NAME=llama-3.3-70b-versatile" >> .env
Run Locally
bash
# Run the dashboard
streamlit run dashboard.py

# Run baseline inference
python inference.py
📁 Project Structure
text
email-triage-env/
├── dashboard.py           # Main Streamlit dashboard (3 modes)
├── environment.py         # Core environment logic with JSON loading
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

🏆 Hackathon Compliance
Requirement	Status
Real-world task simulation	✅ Email triage
OpenEnv spec compliance	✅ reset(), step(), state(), typed models
3+ tasks with graders	✅ Easy (12), Medium (15), Hard (40)
Meaningful reward function	✅ Partial rewards (+0.5 to -0.8)
Baseline inference script	✅ Works with Groq/OpenAI
Deploy to HF Spaces	✅ Live demo
Dockerfile	✅ Working container
Documentation	✅ Complete README
🤝 Acknowledgments
Built with OpenEnv

Powered by Groq (free tier) and OpenAI

Inspired by real-world email security challenges

📄 License
MIT

👨‍💻 Author
Haripreetham

🚀 Built for the Meta AI Hackathon | Transparent Grading | Explainable AI | Memory-Enhanced Learning | Custom Email Editor