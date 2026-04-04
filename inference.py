"""
inference.py - For OpenRouter API
Works with free models like llama-3-8b-instruct:free
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
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))  # Lower for more consistent
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "150"))
MAX_STEPS = 50
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

if not API_KEY:
    print("❌ ERROR: OPENAI_API_KEY not found in .env file!")
    print("Get your key from: https://openrouter.ai/keys")
    sys.exit(1)

# Initialize OpenAI client with OpenRouter base URL
client = OpenAI(
    api_key=API_KEY,
    base_url=API_BASE_URL,
    default_headers={
        "HTTP-Referer": os.getenv("OPENROUTER_SITE_URL", "http://localhost"),
        "X-Title": os.getenv("OPENROUTER_APP_NAME", "Email Triage Env"),
    }
)

print(f"✅ Connected to: {API_BASE_URL}")
print(f"📦 Model: {MODEL_NAME}")

# ============================================
# SYSTEM PROMPT (Simplified for better responses)
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
    # Try to find JSON
    json_match = re.search(r'\{[^{}]*\}', response_text)
    if json_match:
        try:
            data = json.loads(json_match.group())
            if "email_id" in data and "action" in data:
                action = data["action"].lower().strip()
                # Map to valid actions
                if action in ["urgent", "normal", "spam", "skip", "delete", "archive"]:
                    return {"email_id": data["email_id"], "action": action}
        except:
            pass
    
    # Fallback: use current email with default action
    return {"email_id": current_email_id, "action": "normal"}

def run_task(task_id: str, task_name: str) -> Tuple[float, int, List[float]]:
    """Run a single task"""
    print(f"\n{'='*55}")
    print(f"📧 {task_name}")
    print(f"{'='*55}")
    
    env = EmailTriageEnvironment(task_id=task_id)
    rewards = []
    actions_taken = []
    
    observation = env.reset()
    total_emails = len(env.inbox)
    print(f"📬 Inbox: {total_emails} emails\n")
    
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
            
            if DEBUG:
                print(f"🤖 AI: {response[:100]}...")
                
        except Exception as e:
            print(f"⚠️ API Error: {e}")
            response = ""
        
        action_data = parse_action(response, current_email.id)
        action = EmailAction(
            email_id=action_data["email_id"],
            action=ActionType(action_data["action"])
        )
        
        observation, reward, done, info = env.step(action)
        rewards.append(reward)
        actions_taken.append(action)
        
        # Print result
        result_symbol = "✓" if reward > 0 else "✗"
        print(f"  {result_symbol} Step {step}: {action.action.value} on email {action.email_id} -> {reward:+.2f}")
        
        if DEBUG and info.get("breakdown"):
            msg = info['breakdown'].get('message', '')
            if msg:
                print(f"     {msg}")
    
    final_score = grade_task(task_id, actions_taken, env.inbox)
    total_reward = sum(rewards)
    
    print(f"\n📊 Score: {final_score:.3f}/1.0 | Total Reward: {total_reward:.2f} | Steps: {step}")
    
    env.close()
    return final_score, step, rewards

def main():
    print("\n" + "="*60)
    print("📧 EMAIL TRIAGE ENVIRONMENT")
    print(f"🔗 API: {API_BASE_URL}")
    print(f"🤖 Model: {MODEL_NAME}")
    print(f"🌡️ Temperature: {TEMPERATURE}")
    print("="*60)
    
    tasks = [
        ("easy_classification", "EASY: 10 Simple Emails"),
        ("medium_prioritization", "MEDIUM: 15 Subtle Emails"),
        ("hard_evolving", "HARD: 40 Evolving Inbox"),
    ]
    
    results = []
    for task_id, task_name in tasks:
        score, steps, rewards = run_task(task_id, task_name)
        results.append({"name": task_name, "score": score, "steps": steps})
    
    # Summary
    print("\n" + "="*60)
    print("📊 FINAL RESULTS")
    print("="*60)
    
    for r in results:
        print(f"  {r['name']}: {r['score']:.3f}/1.0 ({r['steps']} steps)")
    
    avg_score = sum(r["score"] for r in results) / len(results)
    print(f"\n🏆 AVERAGE SCORE: {avg_score:.3f}/1.0")
    print("="*60)

if __name__ == "__main__":
    main()