# Email Triage Environment

An OpenEnv-compliant environment for AI agents to learn email triage and prioritization.

## Overview

This environment simulates a real-world email inbox where an AI agent must classify, prioritize, and manage emails just like a human would. The agent receives partial rewards for correct decisions and penalties for mistakes, enabling effective reinforcement learning.

## Why Email Triage?

Email management is a genuine daily task for millions of professionals. Training AI agents to handle email triage can:
- Reduce cognitive load on human workers
- Automate repetitive classification tasks
- Ensure urgent communications are never missed

## Environment Features

### Three Difficulty Levels

| Task | Emails | Difficulty | Description |
|------|--------|------------|-------------|
| **Easy** | 3 | 🔵 Simple | Clear urgent/normal/spam signals |
| **Medium** | 5 | 🟡 Moderate | Subtle differences requiring careful reading |
| **Hard** | 5 (evolving) | 🔴 Challenging | New emails arrive during processing |

### Action Space (6 Actions)

| Action | Description |
|--------|-------------|
| `urgent` | Mark as high priority (critical issues, deadlines) |
| `normal` | Mark as regular priority (standard work emails) |
| `spam` | Mark as junk (promotions, scams, newsletters) |
| `delete` | Permanently remove email |
| `archive` | Save for later reference |
| `skip` | Temporarily defer to next email |

### Observation Space

Each step provides the AI with:
- Current email (subject, body, sender)
- Remaining emails count
- Current step number
- Last action result (success/error message)

**Note:** The correct answer is hidden from the AI - it must actually read and understand the email!

### Reward Function

| Scenario | Reward | Reasoning |
|----------|--------|-----------|
| Correct urgent | +0.5 | High value for catching emergencies |
| Correct normal | +0.3 | Baseline positive reward |
| Correct spam | +0.4 | Slightly higher to encourage filtering |
| Missed urgent | -0.8 | Severe penalty for missing emergencies |
| Wrong classification | -0.2 to -0.4 | Proportional to error severity |

## Hard Task Scoring (Weighted)

The hard task uses a sophisticated scoring system:

| Component | Weight | Description |
|-----------|--------|-------------|
| Accuracy | 70% | Correct classification of all emails |
| Efficiency | 20% | Minimizing extra actions |
| Priority | 10% | Processing urgent emails first |

This encourages realistic email management behavior!

## Installation

```bash
# Clone the repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/email-triage-env

# Install dependencies
pip install -r requirements.txt

# Set up API key (for inference)
echo "OPENAI_API_KEY=your_key_here" > .env