"""
test_inference.py - Test version without OpenAI API
Uses random actions to test environment structure
"""

import random
from typing import List, Tuple
from environment import EmailTriageEnvironment
from models import EmailAction, ActionType
from tasks import grade_task

# Available actions
ACTIONS = [ActionType.MARK_URGENT, ActionType.MARK_NORMAL, ActionType.MARK_SPAM]

def run_task(task_id: str, task_name: str) -> Tuple[float, int, List[float]]:
    """Run a task with random actions"""
    print(f"\n{'='*50}")
    print(f"📧 Running: {task_name}")
    print(f"{'='*50}")
    
    env = EmailTriageEnvironment(task_id=task_id)
    rewards = []
    actions_taken = []
    
    observation = env.reset()
    print(f"Inbox size: {len(env.inbox)} emails")
    
    done = False
    step = 0
    
    while not done and step < 50:
        step += 1
        
        # Take a random action (for testing)
        random_action = random.choice(ACTIONS)
        action = EmailAction(
            email_id=observation.current_email.id,
            action=random_action
        )
        
        observation, reward, done, info = env.step(action)
        rewards.append(reward)
        actions_taken.append(action)
        
        print(f"  Step {step}: {random_action.value} on email {action.email_id} -> reward {reward:+.2f}")
        if info.get("breakdown"):
            print(f"    {info['breakdown'].get('message', '')}")
    
    # Calculate final score using grader
    final_score = grade_task(task_id, actions_taken, env.inbox)
    print(f"\n📊 Final Score: {final_score:.3f} / 1.0")
    print(f"Total Steps: {step}")
    print(f"Total Reward: {sum(rewards):.2f}")
    
    env.close()
    return final_score, step, rewards

def main():
    print("\n" + "="*60)
    print("🧪 EMAIL TRIAGE ENVIRONMENT - TEST MODE")
    print("(Using random actions - no OpenAI API needed)")
    print("="*60)
    
    tasks = [
        ("easy_classification", "Easy: 3 Simple Emails"),
        ("medium_prioritization", "Medium: 5 Subtle Emails"),
        ("hard_evolving", "Hard: Evolving Inbox"),
    ]
    
    results = []
    for task_id, task_name in tasks:
        score, steps, rewards = run_task(task_id, task_name)
        results.append({
            "task_name": task_name,
            "score": score,
            "steps": steps,
            "total_reward": sum(rewards)
        })
    
    # Summary
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    for r in results:
        print(f"{r['task_name']:<25} Score: {r['score']:.3f} | Steps: {r['steps']} | Reward: {r['total_reward']:.2f}")
    
    avg = sum(r["score"] for r in results) / len(results)
    print(f"\n🏆 Average Score: {avg:.3f} / 1.0")

if __name__ == "__main__":
    main()