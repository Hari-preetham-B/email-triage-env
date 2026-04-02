"""
dashboard.py - Professional Email Triage Dashboard
Single-click execution | 3D Cosmic Design | AI Agent Demo | Grader Breakdown
"""

import streamlit as st
import time
import json
import re
import base64
from datetime import datetime
from dotenv import load_dotenv
import os
import pandas as pd
from typing import List, Tuple

# Import your environment
from environment import EmailTriageEnvironment
from models import Email,EmailAction, ActionType
from tasks import grade_task, grade_task_with_feedback

load_dotenv()

# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="Email Triage AI | Cosmic Interface",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# 3D COSMIC CSS STYLES
# ============================================

st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Space+Grotesk:wght@300;400;600&display=swap');
    
    /* Main Container */
    .stApp {
        background: linear-gradient(135deg, #0a0a2a 0%, #1a1a3e 50%, #0d0d2b 100%);
        background-attachment: fixed;
    }
    
    /* Glassmorphism Card */
    .glass-card {
        background: rgba(15, 15, 40, 0.6);
        backdrop-filter: blur(12px);
        border-radius: 24px;
        border: 1px solid rgba(139, 92, 246, 0.3);
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    /* Cosmic Title */
    .cosmic-title {
        font-family: 'Orbitron', monospace;
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #8b5cf6, #ec4899, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 10px;
    }
    
    .cosmic-subtitle {
        text-align: center;
        color: #a78bfa;
        font-family: 'Space Grotesk', monospace;
        font-size: 0.9rem;
        letter-spacing: 2px;
    }
    
    /* Stats Card */
    .stat-card {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(236, 72, 153, 0.1));
        border-radius: 20px;
        padding: 15px;
        text-align: center;
        border: 1px solid rgba(139, 92, 246, 0.3);
        height: 100%;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .stat-number {
        font-family: 'Orbitron', monospace;
        font-size: 2.2rem;
        font-weight: 700;
        color: #a78bfa;
        line-height: 1.2;
    }
    
    .stat-label {
        font-family: 'Space Grotesk', monospace;
        font-size: 0.8rem;
        color: #c4b5fd;
        letter-spacing: 1px;
        margin-top: 8px;
    }
    
    /* Breakdown Card */
    .breakdown-card {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 16px;
        padding: 16px;
        margin: 12px 0;
        border: 1px solid rgba(139, 92, 246, 0.2);
    }
    
    .breakdown-title {
        color: #a78bfa;
        font-size: 0.9rem;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .breakdown-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0;
        border-bottom: 1px solid rgba(139, 92, 246, 0.1);
    }
    
    .breakdown-label {
        color: #c4b5fd;
        font-size: 0.85rem;
    }
    
    .breakdown-value {
        color: #34d399;
        font-weight: bold;
        font-size: 0.9rem;
    }
    
    .breakdown-total {
        margin-top: 10px;
        padding-top: 10px;
        border-top: 2px solid rgba(139, 92, 246, 0.3);
        display: flex;
        justify-content: space-between;
        font-weight: bold;
    }
    
    /* AI Decision Log */
    .ai-log-entry {
        background: rgba(139, 92, 246, 0.1);
        border-radius: 12px;
        padding: 12px;
        margin: 8px 0;
        border-left: 3px solid #8b5cf6;
    }
    
    /* Live Processing Card */
    .live-card {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(236, 72, 153, 0.1));
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        border: 2px solid #8b5cf6;
        box-shadow: 0 0 30px rgba(139, 92, 246, 0.3);
        animation: glowPulse 2s infinite;
    }
    @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.spinning-icon {
    animation: spin 1s linear infinite;
    display: inline-block;
    font-size: 2rem;
    text-align: center;
}
    @keyframes glowPulse {
        0%, 100% { box-shadow: 0 0 20px rgba(139, 92, 246, 0.3); border-color: #8b5cf6; }
        50% { box-shadow: 0 0 50px rgba(236, 72, 153, 0.4); border-color: #ec4899; }
    }
    
    .live-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
        flex-wrap: wrap;
        gap: 10px;
    }
    
    .live-badge {
        background: #8b5cf6;
        color: white;
        padding: 4px 16px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .live-step {
        color: #c4b5fd;
        font-size: 0.85rem;
    }
    
    .live-subject {
        font-size: 1.1rem;
        font-weight: bold;
        color: white;
        margin: 15px 0;
        word-wrap: break-word;
    }
    
    .live-decision {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 12px;
        padding: 12px;
        margin: 15px 0;
    }
    
    .live-decision-badge {
        background: #10b981;
        color: white;
        padding: 4px 16px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
        display: inline-block;
    }
    
    .live-reward {
        color: #34d399;
        font-weight: bold;
        font-size: 1rem;
        margin-left: 15px;
    }
    
    .live-message {
        color: #a78bfa;
        margin-top: 12px;
        font-size: 0.85rem;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Progress bar styling */
    .stProgress > div > div {
        background: linear-gradient(90deg, #8b5cf6, #ec4899);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .stat-number {
            font-size: 1.5rem;
        }
        .cosmic-title {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SUCCESS SOUND
# ============================================

# Add audio element for success sound
success_sound = """
<audio id="successSound" preload="auto">
    <source src="https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3" type="audio/mpeg">
</audio>
<script>
function playSuccessSound() {
    var audio = document.getElementById('successSound');
    if (audio) {
        audio.play().catch(e => console.log('Audio play failed:', e));
    }
}
</script>
"""

# Display the hidden audio element
st.markdown(success_sound, unsafe_allow_html=True)
st.markdown('<div class="hidden-audio"></div>', unsafe_allow_html=True)

# ============================================
# INITIALIZE SESSION STATE
# ============================================

if 'current_task' not in st.session_state:
    st.session_state.current_task = "easy_classification"
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'tasks_results' not in st.session_state:
    st.session_state.tasks_results = {}
if 'tasks_breakdown' not in st.session_state:
    st.session_state.tasks_breakdown = {}

# Initialize AI Client
AI_AVAILABLE = False
try:
    from openai import OpenAI
    API_KEY = os.getenv("OPENAI_API_KEY")
    API_BASE_URL = os.getenv("API_BASE_URL", "https://openrouter.ai/api/v1")
    MODEL_NAME = os.getenv("MODEL_NAME", "openai/gpt-3.5-turbo")
    
    if API_KEY:
        client = OpenAI(api_key=API_KEY, base_url=API_BASE_URL)
        AI_AVAILABLE = True
except:
    AI_AVAILABLE = False

# ============================================
# CUSTOM GRADER WITH BREAKDOWN
# ============================================

def grade_task_with_breakdown(task_id: str, actions: List[EmailAction], inbox: List[Email]) -> tuple:
    """Grade task and return both score and detailed breakdown"""
    from tasks import get_grader
    
    grader = get_grader(task_id)
    
    if task_id == "easy_classification":
        correct_map = {email.id: email.correct_category for email in inbox}
        correct_count = 0
        for action in actions:
            if action.email_id in correct_map:
                if action.action.value == correct_map[action.email_id]:
                    correct_count += 1
        score = correct_count / len(inbox) if inbox else 0
        breakdown = {
            "Accuracy": f"{correct_count}/{len(inbox)} correct",
            "Score Calculation": f"{correct_count} / {len(inbox)} = {score:.3f}"
        }
        
    elif task_id == "medium_prioritization":
        correct_map = {email.id: email.correct_category for email in inbox}
        correct_count = 0
        for action in actions:
            if action.email_id in correct_map:
                if action.action.value == correct_map[action.email_id]:
                    correct_count += 1
        base_score = correct_count / len(inbox)
        
        # Urgent bonus
        urgent_emails = [e for e in inbox if e.correct_category == "urgent"]
        urgent_bonus = 0
        for email in urgent_emails:
            for action in actions:
                if action.email_id == email.id and action.action.value == "urgent":
                    urgent_bonus += 0.1 / len(inbox)
        score = min(1.0, base_score + urgent_bonus)
        
        breakdown = {
            "Accuracy": f"{correct_count}/{len(inbox)} correct = {base_score:.3f}",
            "Urgent Bonus": f"+{urgent_bonus:.3f} (correctly handled urgent emails)",
            "Final Score": f"{base_score:.3f} + {urgent_bonus:.3f} = {score:.3f}"
        }
        
    else:  # hard_evolving
        correct_map = {email.id: email.correct_category for email in inbox}
        
        # Accuracy (70%)
        correct_count = 0
        for action in actions:
            if action.email_id in correct_map:
                if action.action.value == correct_map[action.email_id]:
                    correct_count += 1
        accuracy_score = correct_count / len(inbox)
        accuracy_contribution = accuracy_score * 0.7
        
        # Efficiency (20%)
        optimal_steps = len(inbox)
        actual_steps = len(actions)
        if actual_steps <= optimal_steps:
            efficiency_score = 1.0
        else:
            efficiency_score = max(0.0, 1.0 - (actual_steps - optimal_steps) / optimal_steps)
        efficiency_contribution = efficiency_score * 0.2
        
        # Priority (10%)
        urgent_emails = [e.id for e in inbox if e.correct_category == "urgent"]
        non_urgent_emails = [e.id for e in inbox if e.correct_category != "urgent"]
        
        urgent_positions = [i for i, a in enumerate(actions) if a.email_id in urgent_emails]
        non_urgent_positions = [i for i, a in enumerate(actions) if a.email_id in non_urgent_emails]
        
        if urgent_positions and non_urgent_positions:
            if max(urgent_positions) < min(non_urgent_positions):
                priority_score = 1.0
            else:
                urgent_before = sum(1 for u in urgent_positions if u < min(non_urgent_positions))
                priority_score = urgent_before / len(urgent_positions)
        else:
            priority_score = 1.0
        priority_contribution = priority_score * 0.1
        
        score = accuracy_contribution + efficiency_contribution + priority_contribution
        
        breakdown = {
            "📧 Accuracy (70%)": f"{correct_count}/{len(inbox)} correct = {accuracy_score:.3f} → {accuracy_contribution:.3f} pts",
            "⚡ Efficiency (20%)": f"Steps: {actual_steps}/{optimal_steps} optimal = {efficiency_score:.3f} → {efficiency_contribution:.3f} pts",
            "🎯 Priority (10%)": f"Urgent emails processed first = {priority_score:.3f} → {priority_contribution:.3f} pts",
            "─" * 30: "",
            "🏆 TOTAL": f"{accuracy_contribution:.3f} + {efficiency_contribution:.3f} + {priority_contribution:.3f} = {score:.3f}"
        }
    
    return score, breakdown

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_ai_action(email):
    """Get AI decision with fake urgency detection"""
    if not AI_AVAILABLE:
        return "normal"
    
    system_prompt = """You are an AI email security assistant. Your job is to detect fake urgency and scams.

RULES:
1. "urgent" - ONLY for REAL emergencies from legitimate company domains (company.com, official emails)
2. "spam" - Mark as spam if:
   - Fake urgency tactics ("URGENT", "IMMEDIATE", "FINAL WARNING") from suspicious senders
   - Requests for money or wire transfers
   - Threats of account closure or legal action
   - Emotional manipulation ("family emergency", "help me")
   - Too-good-to-be-true offers
3. "normal" - Regular work emails

Respond with ONLY the action word: urgent, normal, or spam"""

    user_prompt = f"""From: {email.sender}
Subject: {email.subject}
Body: {email.body[:300]}

Analyze for fake urgency tactics. Action:"""
    
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=20,
        )
        response = completion.choices[0].message.content or ""
        response = response.lower().strip().strip('"').strip("'")
        
        if "urgent" in response:
            return "urgent"
        elif "spam" in response:
            return "spam"
        else:
            return "normal"
    except:
        return "normal"
    
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=20,
        )
        response = completion.choices[0].message.content or ""
        response = response.lower().strip().strip('"').strip("'")
        
        if "urgent" in response:
            return "urgent"
        elif "spam" in response:
            return "spam"
        else:
            return "normal"
    except:
        return "normal"

def update_progress_timeline(decision, timeline_placeholder):
    """Update the progress timeline with latest decision"""
    with timeline_placeholder.container():
        st.markdown("### 📜 Processing Timeline")
        
        # Get existing timeline from session state
        if 'timeline_entries' not in st.session_state:
            st.session_state.timeline_entries = []
        
        # Add new entry
        emoji = "🟢" if decision['reward'] > 0 else "🔴"
        st.session_state.timeline_entries.append({
            'step': decision['step'],
            'email': decision['subject'][:30],
            'action': decision['action'],
            'reward': decision['reward'],
            'emoji': emoji
        })
        
        # Show last 10 entries (most recent first)
        for entry in reversed(st.session_state.timeline_entries[-10:]):
            reward_color = "#00cc66" if entry['reward'] > 0 else "#ff4b4b"
            st.markdown(f"""
            <div style="font-family: monospace; font-size: 0.8rem; margin: 4px 0;">
                {entry['emoji']} Step {entry['step']}: {entry['email']}... 
                → <span style="color: #a78bfa;">{entry['action'].upper()}</span> 
                → <span style="color: {reward_color};">{entry['reward']:+.2f}</span>
            </div>
            """, unsafe_allow_html=True)

def run_single_task(task_id, task_name, progress_bar, status_text, live_placeholder, timeline_placeholder):
    """Run a single task and return results with LIVE email display"""
    env = EmailTriageEnvironment(task_id=task_id)
    observation = env.reset()
    actions = []
    rewards = []
    decisions = []
    total_emails = len(env.inbox)
    
    for step_idx in range(total_emails):
        current_email = observation.current_email
        
        # Clear previous live card first
        live_placeholder.empty()
        
        # Show spinning animation ABOVE the result
        with live_placeholder.container():
            st.markdown('<div style="text-align: center;"><div class="spinning-icon">🤖</div><p style="color: #a78bfa;">AI Analyzing Email...</p></div>', unsafe_allow_html=True)
            time.sleep(0.3)
        
        # Get AI decision
        action = get_ai_action(current_email)
        
        # Take action
        action_obj = EmailAction(email_id=current_email.id, action=ActionType(action))
        observation, reward, done, info = env.step(action_obj)
        
        actions.append(action_obj)
        rewards.append(reward)
        
        decision = {
            'step': step_idx + 1,
            'email_id': current_email.id,
            'subject': current_email.subject[:50],
            'action': action,
            'reward': reward,
            'message': info.get('breakdown', {}).get('message', '')[:80]
        }
        decisions.append(decision)
        
        # Update progress timeline
        update_progress_timeline(decision, timeline_placeholder)
        
        # Now replace spinner with the actual result card
        with live_placeholder.container():
            action_color = "#10b981" if action == "urgent" else "#3b82f6" if action == "normal" else "#8b5cf6"
            st.markdown(f"""
            <div class="live-card">
                <div class="live-header">
                    <span class="live-badge">🔴 PROCESSING</span>
                    <span class="live-step">Email {step_idx + 1} of {total_emails}</span>
                </div>
                <div class="live-subject">📧 {current_email.subject[:100]}</div>
                <div style="color: #94a3b8; font-size: 0.85rem;">From: {current_email.sender}</div>
                <div class="live-decision">
                    <span class="live-decision-badge" style="background: {action_color};">🎯 AI DECIDED: {action.upper()}</span>
                    <span class="live-reward">Reward: {reward:+.2f}</span>
                </div>
                <div class="live-message">💡 {info.get('breakdown', {}).get('message', '')}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Update progress
        progress = (step_idx + 1) / total_emails
        progress_bar.progress(progress)
        status_text.info(f"✨ Processing {task_name} - Email {step_idx + 1} of {total_emails}")
        time.sleep(0.2)
    
    live_placeholder.empty()
    
    # Calculate score with breakdown
    if task_id == "hard_evolving":
        score, boss_feedback = grade_task_with_breakdown(task_id, actions, env.inbox)
        if boss_feedback:
            st.success(f"📢 BOSS FEEDBACK: {boss_feedback}")
        # For hard task, also get the breakdown from the function
        # Since your function returns breakdown as well, let's capture it
        score, breakdown = grade_task_with_breakdown(task_id, actions, env.inbox)
    else:
        score, breakdown = grade_task_with_breakdown(task_id, actions, env.inbox)
    env.close()
    
    return {
        'task_name': task_name,
        'score': score,
        'breakdown': breakdown,
        'total_reward': sum(rewards),
        'steps': len(actions),
        'decisions': decisions,
        'color': '#00cc66' if score >= 0.8 else '#ffaa00' if score >= 0.5 else '#ff4b4b'
    }

def generate_results_json():
    """Generate JSON data for download"""
    results = st.session_state.tasks_results
    if not results:
        return None
    
    # Prepare data structure
    export_data = {
        "export_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "model_used": MODEL_NAME.replace('openai/', '') if AI_AVAILABLE else "Unknown",
        "tasks_results": {},
        "average_score": 0.0,
        "summary": {
            "total_emails_processed": 0,
            "total_steps_taken": 0,
            "total_reward_earned": 0.0
        }
    }
    
    total_score = 0
    total_emails = 0
    total_steps = 0
    total_reward_sum = 0
    
    task_display_names = {
        "easy_classification": "🔵 EASY: 3 Simple Emails",
        "medium_prioritization": "🟡 MEDIUM: 5 Subtle Emails",
        "hard_evolving": "🔴 HARD: Evolving Inbox"
    }
    
    for task_id, result in results.items():
        export_data["tasks_results"][task_id] = {
            "task_name": task_display_names.get(task_id, task_id),
            "score": result.get('score', 0),
            "total_reward": result.get('total_reward', 0),
            "steps": result.get('steps', 0),
            "decisions": result.get('decisions', []),
            "breakdown": result.get('breakdown', {})
        }
        total_score += result.get('score', 0)
        total_emails += len(result.get('decisions', []))
        total_steps += result.get('steps', 0)
        total_reward_sum += result.get('total_reward', 0)
    
    export_data["average_score"] = total_score / len(results) if results else 0
    export_data["summary"] = {
        "total_emails_processed": total_emails,
        "total_steps_taken": total_steps,
        "total_reward_earned": round(total_reward_sum, 2)
    }
    
    return export_data

def run_all_tasks():
    """Run all three tasks"""
    st.session_state.is_running = True
    st.session_state.tasks_results = {}
    st.session_state.tasks_breakdown = {}
    
    tasks = [
        ("easy_classification", "🔵 EASY", "3 Simple Emails"),
        ("medium_prioritization", "🟡 MEDIUM", "5 Subtle Emails"),
        ("hard_evolving", "🔴 HARD", "Evolving Inbox"),
    ]
    
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    live_placeholder = st.empty()
    results_placeholder = st.empty()
    timeline_placeholder = st.empty()
    
    for task_id, difficulty, task_name in tasks:
        status_text = status_placeholder.empty()
        progress_bar = progress_placeholder.progress(0)
        
        result = run_single_task(task_id, f"{difficulty}: {task_name}", progress_bar, status_text, live_placeholder, timeline_placeholder)
        st.session_state.tasks_results[task_id] = result
        
        with results_placeholder.container():
            st.markdown("---")
            cols = st.columns(len(st.session_state.tasks_results))
            for idx, (tid, res) in enumerate(st.session_state.tasks_results.items()):
                with cols[idx]:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-number">{res['score']:.3f}</div>
                        <div class="stat-label">{res['task_name'].split(':')[0]}</div>
                    </div>
                    """, unsafe_allow_html=True)
    
    status_placeholder.success("🎉 All tasks completed successfully!")
    progress_placeholder.empty()
    
    # Play success sound
    st.markdown('<script>playSuccessSound();</script>', unsafe_allow_html=True)
    
    st.session_state.is_running = False
    st.rerun()

# ============================================
# MAIN UI
# ============================================

st.markdown('<div class="cosmic-title">⚡ EMAIL TRIAGE AI ⚡</div>', unsafe_allow_html=True)
st.markdown('<div class="cosmic-subtitle">🌌 AUTONOMOUS EMAIL PROCESSING • OPENENV COMPATIBLE 🌌</div>', unsafe_allow_html=True)
st.markdown("---")

col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    st.markdown("""
    <div class="glass-card" style="text-align: center;">
        <div style="font-size: 2rem;">🤖</div>
        <h3 style="color: #a78bfa; margin: 10px 0 5px 0;">Autonomous AI Agent</h3>
        <p style="color: #c4b5fd;">Powered by GPT-3.5 • Real-time decisions • Multi-task evaluation</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.is_running:
        if st.button("🚀 LAUNCH FULL DEMO", use_container_width=True, type="primary"):
            run_all_tasks()
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #8b5cf6, #ec4899); border-radius: 50px; padding: 12px; text-align: center;">
            <span style="color: white; font-weight: bold;">✨ AI PROCESSING ✨</span>
        </div>
        """, unsafe_allow_html=True)
    
    if AI_AVAILABLE:
        st.caption(f"✅ AI Ready: {MODEL_NAME.replace('openai/', '')}")


st.markdown("---")

# Results Dashboard
if st.session_state.tasks_results:
    st.markdown("### 📊 MISSION RESULTS")
    
    scores = [r['score'] for r in st.session_state.tasks_results.values()]
    avg_score = sum(scores) / len(scores)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        easy_score = st.session_state.tasks_results.get('easy_classification', {}).get('score', 0)
        easy_color = st.session_state.tasks_results.get('easy_classification', {}).get('color', '#888')
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number" style="color: {easy_color};">{easy_score:.3f}</div>
            <div class="stat-label">📧 EASY</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        medium_score = st.session_state.tasks_results.get('medium_prioritization', {}).get('score', 0)
        medium_color = st.session_state.tasks_results.get('medium_prioritization', {}).get('color', '#888')
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number" style="color: {medium_color};">{medium_score:.3f}</div>
            <div class="stat-label">⚡ MEDIUM</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        hard_score = st.session_state.tasks_results.get('hard_evolving', {}).get('score', 0)
        hard_color = st.session_state.tasks_results.get('hard_evolving', {}).get('color', '#888')
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number" style="color: {hard_color};">{hard_score:.3f}</div>
            <div class="stat-label">🌌 HARD</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card" style="border-color: #ec4899;">
            <div class="stat-number" style="color: #ec4899;">{avg_score:.3f}</div>
            <div class="stat-label">🏆 AVERAGE</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Grader Breakdown Section
    st.markdown("### 📋 GRADER BREAKDOWN")
    st.markdown("*How each task was scored — transparent grading for reproducible evaluation*")
    
    breakdown_cols = st.columns(3)
    
    for idx, (task_id, result) in enumerate(st.session_state.tasks_results.items()):
        with breakdown_cols[idx]:
            task_icons = {
                'easy_classification': '📧 EASY TASK',
                'medium_prioritization': '⚡ MEDIUM TASK',
                'hard_evolving': '🌌 HARD TASK'
            }
            st.markdown(f"""
            <div class="breakdown-card">
                <div class="breakdown-title">{task_icons.get(task_id, task_id)}</div>
            """, unsafe_allow_html=True)
            
            breakdown = result.get('breakdown', {})
            for key, value in breakdown.items():
                if key == "─" * 30:
                    st.markdown("<hr style='margin: 8px 0; border-color: rgba(139,92,246,0.2);'>", unsafe_allow_html=True)
                elif key == "🏆 TOTAL":
                    st.markdown(f"""
                    <div class="breakdown-total">
                        <span>{key}</span>
                        <span style="color: #34d399;">{value}</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="breakdown-item">
                        <span class="breakdown-label">{key}</span>
                        <span class="breakdown-value">{value}</span>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # AI Decision Log
    st.markdown("### 🤖 AI DECISION LOG")
    
    tabs = st.tabs(["📧 EASY TASK", "⚡ MEDIUM TASK", "🌌 HARD TASK"])
    
    for idx, (task_id, result) in enumerate(st.session_state.tasks_results.items()):
        with tabs[idx]:
            for decision in result['decisions']:
                reward_color = "#00cc66" if decision['reward'] > 0 else "#ff4b4b"
                st.markdown(f"""
                <div class="ai-log-entry">
                    <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                        <span style="color: #a78bfa;"><b>Step {decision['step']}</b> | Email #{decision['email_id']}</span>
                        <span style="color: {reward_color}; font-weight: bold;">{decision['reward']:+.2f}</span>
                    </div>
                    <div style="color: white; margin: 8px 0;">📧 {decision['subject']}...</div>
                    <div style="display: flex; flex-wrap: wrap; gap: 10px; align-items: center;">
                        <span style="background: rgba(139,92,246,0.3); padding: 4px 12px; border-radius: 20px;">🎯 {decision['action'].upper()}</span>
                        <span style="color: #c4b5fd; font-size: 0.8rem;">{decision['message']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Reset and Download Buttons
    col_r1, col_r2, col_r3 = st.columns([1, 2, 1])
    with col_r2:
        # Download button
        export_data = generate_results_json()
        if export_data:
            json_str = json.dumps(export_data, indent=2, default=str)
            st.download_button(
                label="📥 DOWNLOAD RESULTS (JSON)",
                data=json_str,
                file_name=f"email_triage_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        if st.button("🔄 RESET & RUN AGAIN", use_container_width=True):
            st.session_state.tasks_results = {}
            st.rerun()

else:
    col_w1, col_w2, col_w3 = st.columns([1, 2, 1])
    with col_w2:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 4rem;">🌌</div>
            <h3 style="color: #a78bfa;">Ready to Launch?</h3>
            <p style="color: #c4b5fd;">Click the <strong style="color: #ec4899;">LAUNCH FULL DEMO</strong> button to see the AI agent in action.</p>
            <hr style="border-color: rgba(139,92,246,0.3);">
            <div style="text-align: left;">
                <p style="color: #a78bfa;">📋 <strong>How scoring works:</strong></p>
                <ul style="color: #c4b5fd;">
                    <li><strong>EASY:</strong> Simple accuracy — correct/total emails</li>
                    <li><strong>MEDIUM:</strong> Accuracy + urgent email bonus</li>
                    <li><strong>HARD:</strong> 70% Accuracy + 20% Efficiency + 10% Priority</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #4a4a7a; font-size: 0.8rem; padding: 20px;">
    🚀 Built with OpenEnv • Powered by GPT-3.5 • Transparent Grading
</div>
""", unsafe_allow_html=True)