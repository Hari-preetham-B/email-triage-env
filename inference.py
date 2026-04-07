"""
inference.py - For OpenRouter API with structured logging
Follows hackathon required [START], [STEP], [END] format
"""

import os
import sys
import json
import re
from typing import List, Tuple
from dotenv import load_dotenv
from openai import OpenAI

from environment import EmailTriageEnvironment
from models import EmailAction, ActionType
from tasks import grade_task

load_dotenv()

# ============================================
# CONFIGURATION
# ============================================

API_BASE_URL = os.getenv("API_BASE_URL", "https://openrouter.ai/api/v1")
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/llama-3-8b-instruct:free")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "150"))
MAX_STEPS = 50
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

if not API_KEY:
    print("❌ ERROR: OPENAI_API_KEY not found in .env file!")
    print("Get your key from: https://openrouter.ai/keys")
    sys.exit(1)

# Initialize OpenAI client
client = OpenAI(
    api_key=API_KEY,
    base_url=API_BASE_URL,
    default_headers={
        "HTTP-Referer": os.getenv("OPENROUTER_SITE_URL", "http://localhost"),
        "X-Title": os.getenv("OPENROUTER_APP_NAME", "Email Triage Env"),
    }
)

# ============================================
# STRUCTURED LOGGING FUNCTIONS
# ============================================

def log_start(task: str, env: str, model: str):
    """Emit structured START log"""
    print(f"[START] task={task}, env={env}, model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: str = None):
    """Emit structured STEP log"""
    error_str = "null" if error is None else f"\"{error}\""
    print(f"[STEP] step={step}, action={action}, reward={reward:.3f}, done={str(done).lower()}, error={error_str}", flush=True)


def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    """Emit structured END log"""
    rewards_str = ",".join([f"{r:.3f}" for r in rewards])
    print(f"[END] success={str(success).lower()}, steps={steps}, score={score:.3f}, rewards=[{rewards_str}]", flush=True)


# ============================================
# SYSTEM PROMPT
# ============================================

SYSTEM_PROMPT = """You are an AI email assistant. Your job is to classify emails.

Actions you can take:
- "urgent" - Mark as urgent (for critical issues, deadlines, emergencies)
- "normal" - Mark as normal (regular work emails)
- "spam" - Mark as spam (junk, promotions, scams)
- "skip" - Skip this email for now

IMPORTANT RULES:
1. Respond with ONLY a JSON object
2. Format: {"email_id": <id>, "action": "<action>"}
3. Example: {"email_id": 1, "action": "urgent"}

Do NOT add any explanation. Only output JSON."""


def parse_action(response_text: str, current_email_id: int) -> dict:
    """Parse AI response into action dict"""
    json_match = re.search(r'\{[^{}]*\}', response_text)
    if json_match:
        try:
            data = json.loads(json_match.group())
            if "email_id" in data and "action" in data:
                action = data["action"].lower().strip()
                if action in ["urgent", "normal", "spam", "skip", "delete", "archive"]:
                    return {"email_id": data["email_id"], "action": action}
        except:
            pass
    
    return {"email_id": current_email_id, "action": "normal"}


def run_task(task_id: str, task_name: str, env_name: str) -> Tuple[float, int, List[float]]:
    """Run a single task with structured logging"""
    env = EmailTriageEnvironment(task_id=task_id)
    rewards = []
    actions_taken = []
    
    observation = env.reset()
    total_emails = len(env.inbox)
    
    done = False
    step = 0
    
    while not done and step < MAX_STEPS:
        step += 1
        current_email = observation.current_email
        
        # Build prompt
        user_prompt = f"""Email ID: {current_email.id}
From: {current_email.sender}
Subject: {current_email.subject}
Body: {current_email.body[:300]}

Choose action:"""

        try:
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
            )
            response = completion.choices[0].message.content or ""
        except Exception as e:
            response = ""
        
        action_data = parse_action(response, current_email.id)
        action = EmailAction(
            email_id=action_data["email_id"],
            action=ActionType(action_data["action"])
        )
        
        observation, reward, done, info = env.step(action)
        rewards.append(reward)
        actions_taken.append(action)
        
        # Emit structured STEP log
        error = info.get('breakdown', {}).get('message', None)
        log_step(step=step, action=action.action.value, reward=reward, done=done, error=error)
    
    final_score = grade_task(task_id, actions_taken, env.inbox)
    env.close()
    
    return final_score, len(actions_taken), rewards


def main():
    # Print environment info (optional, not part of structured logs)
    print(f"Connected to: {API_BASE_URL}", flush=True)
    print(f"Model: {MODEL_NAME}", flush=True)
    
    tasks = [
        ("easy_classification", "EASY", "email-triage-env"),
        ("medium_prioritization", "MEDIUM", "email-triage-env"),
        ("hard_evolving", "HARD", "email-triage-env"),
    ]
    
    all_rewards = []
    total_steps = 0
    total_score = 0.0
    
    for task_id, task_name, env_name in tasks:
        # Emit START log
        log_start(task=task_name, env=env_name, model=MODEL_NAME)
        
        # Run task
        score, steps, rewards = run_task(task_id, task_name, env_name)
        
        # Emit END log
        success = score >= 0.5
        log_end(success=success, steps=steps, score=score, rewards=rewards)
        
        total_score += score
        total_steps += steps
        all_rewards.extend(rewards)
    
    avg_score = total_score / 3
    print(f"\nAverage Score: {avg_score:.3f}/1.0", flush=True)


if __name__ == "__main__":
    main()