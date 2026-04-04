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

## 📊 Baseline Performance

Using GPT-3.5 via Groq:

| Task | Score | Accuracy |
|------|-------|----------|
| Easy (10 emails) | 1.000 | 100% |
| Medium (15 emails) | 0.887 | 89% |
| Hard (40 emails) | 0.856 | 86% |
| **Average** | **0.914** | **91.4%** |

**AI is 174% better than random guessing (0.333 baseline)!**

## 🚀 Usage

Click **"LAUNCH FULL DEMO"** to see the AI agent process all emails in real-time.

Switch to **"AI vs RANDOM MODE"** to compare AI performance against random baseline.

## 🔧 Environment Variables

The following secrets are configured in this Space:

| Secret | Description |
|--------|-------------|
| `OPENAI_API_KEY` | Groq API key for LLM access |
| `API_BASE_URL` | Groq API endpoint |
| `MODEL_NAME` | Model identifier (llama-3.3-70b-versatile) |

## 🏆 Hackathon Compliance

| Requirement | Status |
|-------------|--------|
| Real-world task simulation | ✅ Email triage |
| OpenEnv spec compliance | ✅ reset(), step(), state(), typed models |
| 3+ tasks with graders | ✅ Easy (10), Medium (15), Hard (40) |
| Meaningful reward function | ✅ Partial rewards (+0.5 to -0.8) |
| Baseline inference script | ✅ Works with Groq/OpenAI |
| Deploy to HF Spaces | ✅ Live demo |
| Dockerfile | ✅ Working container |

## 📄 License

MIT

---

**🚀 Built for the Meta AI Hackathon | Transparent Grading | Explainable AI | Memory-Enhanced Learning**