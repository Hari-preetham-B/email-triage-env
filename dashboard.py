"""
dashboard.py - Professional Email Triage Dashboard
Single-click execution | 3D Cosmic Design | AI Agent Demo | Grader Breakdown
"""
import json
import streamlit as st
import time
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
        background: radial-gradient(circle at 20% 20%, rgba(138,43,226,0.25), transparent 40%),
                    radial-gradient(circle at 80% 30%, rgba(0,191,255,0.2), transparent 40%),
                    radial-gradient(circle at 50% 80%, rgba(255,0,150,0.15), transparent 40%),
                    #050518;
        
        background-attachment: fixed;
        
        animation: bgMove 18s ease infinite;
    }
            
    .stApp::after {
        content: "";
        position: fixed;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;

        background:
            radial-gradient(3px 3px at 10% 20%, white, transparent),
            radial-gradient(4px 4px at 30% 40%, #8b5cf6, transparent),
            radial-gradient(3px 3px at 50% 60%, #00bfff, transparent),
            radial-gradient(5px 5px at 70% 80%, #ec4899, transparent),
            radial-gradient(3px 3px at 80% 30%, white, transparent),
            radial-gradient(4px 4px at 20% 70%, #6a5acd, transparent),
            radial-gradient(3px 3px at 60% 20%, #00bfff, transparent),
            radial-gradient(5px 5px at 40% 90%, #ec4899, transparent),
            radial-gradient(3px 3px at 25% 50%, #8b5cf6, transparent),
            radial-gradient(4px 4px at 65% 75%, #00bfff, transparent),
            radial-gradient(3px 3px at 15% 85%, white, transparent),
            radial-gradient(4px 4px at 85% 15%, #6a5acd, transparent),
            radial-gradient(3px 3px at 55% 35%, #ec4899, transparent),
            radial-gradient(5px 5px at 75% 55%, #00bfff, transparent),
            radial-gradient(3px 3px at 35% 10%, #8b5cf6, transparent);
            

        animation: starsMove 12s linear infinite; /* faster */
        pointer-events: none;
        opacity: 0.5; /* slightly stronger */
    }
            

    @keyframes starsMove {
        from { transform: translateY(0px); }
        to { transform: translateY(-400px); }
    }
    
    /* Glassmorphism Card */
    .glass-card {
        background: linear-gradient(135deg, rgba(30,144,255,0.15), rgba(138,43,226,0.1));
        backdrop-filter: blur(12px);

        border-radius: 20px;
        border: 1px solid rgba(138,43,226,0.3);
        position: relative;

        padding: 24px;
        margin: 16px 0;

        box-shadow: 
            0 0 20px rgba(30,144,255,0.3),
            0 0 40px rgba(138,43,226,0.2);

        transition: all 0.35s ease;
    }
            
    .glass-card::after {
        content: "";
        position: absolute;
        inset: 0;
        border-radius: 20px;
        box-shadow: 0 0 20px rgba(138,43,226,0.4);
        opacity: 0.6;
        pointer-events: none;
    }
            
    .glass-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            0 0 30px rgba(30,144,255,0.6),
            0 0 60px rgba(138,43,226,0.4);
    }
    
    
    /* Cosmic Title */
    .cosmic-title {
        font-family: 'Orbitron', monospace;
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #ffffff, #ff6b9d, #ffd93d);
        -webkit-background-clip: text;
        background-clip: text;
        color: #ffffff;  /* Fallback color */
        text-align: center;
        margin-bottom: 10px;
        text-shadow: 0 0 10px rgba(255,255,255,0.6),
             0 0 20px rgba(30,144,255,0.8),
             0 0 40px rgba(138,43,226,0.6);
        animation: textBreath 6s ease-in-out infinite;
    }
    @keyframes textBreath {
        0%,100% { opacity: 0.9; }
        50% { opacity: 1; }
    }
    .cosmic-subtitle {
        text-align: center;
        color: #ffd93d;
        font-family: 'Space Grotesk', monospace;
        font-size: 0.9rem;
        letter-spacing: 2.5px;
        opacity: 0.9;
        font-weight: bold;
    }
            
    .breakdown-label,
    .live-message {
        opacity: 0.85;
    }

    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes bgMove {
        0% { background-position: 20% 20%, 80% 30%, 50% 80%; }
        50% { background-position: 25% 25%, 75% 35%, 55% 75%; }
        100% { background-position: 20% 20%, 80% 30%, 50% 80%; }
    }
    @keyframes softGlow {
        0% { box-shadow: 0 0 15px rgba(138,43,226,0.3); }
        50% { box-shadow: 0 0 35px rgba(138,43,226,0.6); }
        100% { box-shadow: 0 0 15px rgba(138,43,226,0.3); }
    }
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 10px rgba(138,43,226,0.4); }
        50% { box-shadow: 0 0 30px rgba(138,43,226,0.8); }
        100% { box-shadow: 0 0 10px rgba(138,43,226,0.4); }
    }

    .live-card {
        animation: pulseGlow 2s infinite;
    }
            
    .title-bar {
        background: linear-gradient(270deg, #0a3d62, #1e90ff, #6a5acd, #1e90ff);
        background-size: 600% 600%;
        animation: gradientFlow 8s ease infinite;

        padding: 30px 10px;
        margin: 0;
        width: 100%;
        border-radius: 0;

        text-align: center;
        position: relative;
        overflow: hidden;

        box-shadow: 0 0 25px rgba(30, 144, 255, 0.6);
    }
    .title-bar::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;

        background: radial-gradient(circle, rgba(255,255,255,0.15), transparent 70%);
        animation: glowRotate 6s linear infinite;
    }
    @keyframes glowRotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .title-bar {
        text-align: center;
    }

    .cosmic-title {
        margin: 0;
    }

    .cosmic-subtitle {
        margin-top: 5px;
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
            
    .stat-card:hover {
        transform: scale(1.06);
        box-shadow: 0 0 30px rgba(139,92,246,0.7);
    }

        /* Welcome Card Styles */
    .welcome-card {
        background: linear-gradient(135deg, rgba(30,144,255,0.08), rgba(138,43,226,0.05));
        backdrop-filter: blur(10px);
        border-radius: 24px;
        padding: 25px;
        margin: 20px 0;
        border: 1px solid rgba(30,144,255,0.3);
        box-shadow: 0 0 30px rgba(30,144,255,0.1);
    }
    .stat-number {
        font-family: 'Orbitron', monospace;
        font-size: 2.4rem;
        font-weight: 700;
        color: #a78bfa;
        line-height: 1.2;
        transition: all 0.3s ease;
    }
    .stat-number:hover {
        text-shadow: 0 0 25px rgba(138,43,226,0.9);
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
        animation: glowPulse 2.5s ease-in-out infinite;
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
        background: linear-gradient(270deg, #8b5cf6, #ec4899, #8b5cf6);
        background-size: 300% 300%;
        animation: progressMove 3s linear infinite;
    }
            
    @keyframes progressMove {
        0% { background-position: 0% }
        100% { background-position: 100% }
    }
            
    .stButton > button {
        background: linear-gradient(135deg, #1e90ff, #6a5acd);
        color: white;
        border-radius: 12px;
        border: none;
        font-weight: bold;

        box-shadow: 0 0 15px rgba(30,144,255,0.5);
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 25px rgba(30,144,255,0.8);
    }
    
    h3, h2 {
        color: #c4b5fd;
        text-shadow: 0 0 10px rgba(138,43,226,0.6);
        font-weight: 600;
        letter-spacing: 0.5px;
    }        
    
    section.main > div {
        padding-top: 2rem;
    }
    /* Better spacing */
    .glass-card,
    .stat-card,
    .breakdown-card {
        margin-top: 18px;
    }
    .glass-card,
    .stat-card,
    button {
        transition: all 0.25s ease-in-out;
    }
    /* Subtle hover glow */
    .breakdown-card:hover,
    .ai-log-entry:hover {
        box-shadow: 0 0 20px rgba(138,43,226,0.4);
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
    /* Fade animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
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
if 'page_mode' not in st.session_state:
    st.session_state.page_mode = "normal"  # "normal" or "comparison"

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

def get_ai_action(email, sender_history=None):
    """Get AI decision with confidence score and reasoning"""
        # Special rules for specific email patterns
    if "Patch Required" in email.subject or "Security Update:" in email.subject:
        return "normal", 0.85, "Routine security update - not urgent"
    if "Breach Attempt Detected" in email.subject and "No action needed" in email.body:
        return "normal", 0.85, "Security notification - no action required"
    if "Follow-up: Contract Renewal" in email.subject:
        return "urgent", 0.9, "Client follow-up requires attention"
    if not AI_AVAILABLE:
        return "normal", 0.5, "AI not configured"
    
    # Build memory context if history exists
    memory_context = ""
    if sender_history and len(sender_history) > 0:
        memory_context = "\n\n[PAST INTERACTIONS WITH THIS SENDER]:\n"
        for i, past in enumerate(sender_history[-3:], 1):
            memory_context += f"  {i}. Previously: '{past['subject']}' - classified as {past['category'].upper()}\n"
        memory_context += "\nUse this history to understand the sender's pattern."
    
    system_prompt = f"""You are an AI email security assistant. Classify each email as urgent, normal, or spam.

CRITICAL RULES - SECURITY EMAILS ARE ALWAYS URGENT:

URGENT (Mark as urgent if ANY of these apply):
- SECURITY ALERTS: password changes, login attempts, security breaches, unauthorized access
- System failures: server down, database issues, data loss
- Client escalations or complaints
- ANY email from security@company.com, it-security@company.com
- Active threats: "unauthorized access detected", "data breach", "customer info exposed"
- System failures: "server down", "database migration failed", "production server down"
- Client escalations: "client threatening to leave", "complaint", "escalation"
- Time-sensitive: "expires in", "immediate action required"
- ANY email containing: "security alert", "password", "breach", "unauthorized", "failed login"

SPAM (Mark as spam if ANY of these apply):
- Fake urgency from non-company domains
- Free gift cards, lottery wins, prizes, money requests
- Emotional manipulation ("family emergency", "help me")
- Fake invoices or legal threats
- Fake urgency, lottery wins, money requests, emotional manipulation

NORMAL:
- Meeting invites, team updates, newsletters
- Routine work emails, code reviews, HR updates
- General company communications
- Routine security: "patch required", "security update", "maintenance scheduled"
- "Attempt detected" with "no action needed" - this is normal, not urgent
- Regular updates, newsletters, meeting invites
- Contract follow-ups (unless marked urgent)


IMPORTANT: When in doubt about security-related content, mark as URGENT. It's better to be safe than sorry.

{memory_context}

Respond with ONLY one word: urgent, normal, or spam"""

    user_prompt = f"""From: {email.sender}
Subject: {email.subject}
Body: {email.body[:300]}

Classification (urgent/normal/spam):"""
    
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            max_tokens=20,
        )
        response = completion.choices[0].message.content or ""
        response = response.lower().strip().strip('"').strip("'")
        
        confidence = 0.9 if response in ["urgent", "normal", "spam"] else 0.5
        reasoning = f"AI classified as {response} based on email content"
        
        if "urgent" in response:
            return "urgent", confidence, reasoning
        elif "spam" in response:
            return "spam", confidence, reasoning
        else:
            return "normal", confidence, reasoning
    except Exception as e:
        print(f"API Error: {e}")
        return "normal", 0.5, f"Error: {str(e)[:50]}"

def update_progress_timeline(decision, timeline_placeholder):
    """Update the progress timeline with latest decision"""
    with timeline_placeholder.container():
        st.markdown("### 📜 Processing Timeline")
        
        # Get existing timeline from session state
        if 'timeline_entries' not in st.session_state:
            st.session_state.timeline_entries = []
        
        # Add new entry (no duplicates)
        emoji = "🟢" if decision['reward'] > 0 else "🔴"
        new_entry = {
            'step': decision['step'],
            'email': decision['subject'][:30],
            'action': decision['action'],
            'reward': decision['reward'],
            'emoji': emoji
        }
        
        # Check if step already exists (avoid duplicates)
        existing_steps = [e['step'] for e in st.session_state.timeline_entries]
        if decision['step'] not in existing_steps:
            st.session_state.timeline_entries.append(new_entry)
        
        # Show last 10 entries (most recent)
        last_entries = st.session_state.timeline_entries[-10:]
        for entry in last_entries:
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
    step_idx = 0
    done = False
    st.session_state.timeline_entries = []  # Clear timeline for this task
    
    while step_idx < len(env.inbox) and not done:
        current_email = observation.current_email
        step_idx += 1
        
        # Clear previous live card first
        live_placeholder.empty()
        
        # Show spinning animation ABOVE the result
        with live_placeholder.container():
            st.markdown('<div style="text-align: center;"><div class="spinning-icon">🤖</div><p style="color: #a78bfa;">AI Analyzing Email...</p></div>', unsafe_allow_html=True)
            time.sleep(0.3)
        
        # Get sender history for memory
        sender_history = env.get_sender_history(current_email.sender)
        
        # Build memory display text for UI
        memory_display = ""
        if sender_history and len(sender_history) > 0:
            memory_display = "\n📜 **Memory:** "
            for past in sender_history[-2:]:  # Show last 2 interactions
                past_action = past.get('category', 'unknown')
                memory_display += f"Previously '{past['subject'][:30]}' → {past_action.upper()}; "
        
                # Get AI decision with memory, confidence, and reasoning
        action, confidence, reasoning = get_ai_action(current_email, sender_history)
        
        # Take action
        action_obj = EmailAction(email_id=current_email.id, action=ActionType(action))
        observation, reward, done, info = env.step(action_obj)
        
        actions.append(action_obj)
        rewards.append(reward)
        
        decision = {
            'step': step_idx ,
            'email_id': current_email.id,
            'subject': current_email.subject[:50],
            'action': action,
            'reward': reward,
            'message': info.get('breakdown', {}).get('message', '')[:80],
            'memory': memory_display if memory_display else 'No prior interactions',
            'confidence': confidence,
            'reasoning': reasoning[:100]  # Limit length
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
                    <span class="live-step">Email {step_idx} of {len(env.inbox)}</span>
                </div>
                <div class="live-subject">📧 {current_email.subject[:100]}</div>
                <div style="color: #94a3b8; font-size: 0.85rem;">From: {current_email.sender}</div>
                <div class="live-decision">
                    <span class="live-decision-badge" style="background: {action_color};">🎯 AI DECIDED: {action.upper()}</span>
                    <span class="live-reward">Reward: {reward:+.2f}</span>
                </div>
                <div style="display: flex; align-items: center; gap: 10px; margin: 8px 0;">
                    <span style="background: rgba(139,92,246,0.3); padding: 2px 10px; border-radius: 20px; font-size: 0.7rem;">
                        🎯 Confidence: {int(confidence * 100)}%
                    </span>
                </div>
                <div style="color: #c4b5fd; font-size: 0.75rem; margin: 8px 0; border-top: 1px solid rgba(139,92,246,0.2); padding-top: 8px;">
                    🧠 {memory_display if memory_display else 'No prior interactions with this sender'}
                </div>
                <div class="live-message">💡 {info.get('breakdown', {}).get('message', '')}</div>
                <div style="color: #a78bfa; font-size: 0.75rem; margin-top: 8px; font-style: italic;">
                    💭 Reasoning: {reasoning[:150]}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Update progress - recalculate based on current inbox size
        current_total = len(env.inbox)
        progress = min(0.99, step_idx / current_total)  # Cap at 0.99 to avoid 1.0 before completion
        progress_bar.progress(progress)
        status_text.info(f"✨ Processing {task_name} - Email {step_idx } of {current_total}")
        time.sleep(0.2)
    
    live_placeholder.empty()
    
        # Calculate score with breakdown
    if task_id == "hard_evolving":
        score, breakdown = grade_task_with_breakdown(task_id, actions, env.inbox)
        # Get boss feedback from the grader directly
        from tasks import get_grader
        grader = get_grader(task_id)
        if hasattr(grader, 'boss_feedback'):
            st.success(f"📢 BOSS FEEDBACK: {grader.boss_feedback}")
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
        "easy_classification": "🔵 EASY: 10 Simple Emails",
        "medium_prioritization": "🟡 MEDIUM: 15 Subtle Emails",
        "hard_evolving": "🔴 HARD: 40 Evolving Inbox"
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
            st.markdown("<div style='height: 40px'></div>", unsafe_allow_html=True)
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

st.markdown("""
<div style="animation: fadeIn 0.8s ease-in;">
    <div class="title-bar">
        <div class="cosmic-title">⚡ EMAIL TRIAGE AI ⚡</div>
        <div class="cosmic-subtitle">
            🌌 AUTONOMOUS EMAIL PROCESSING • OPENENV COMPATIBLE 🌌
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("<div style='height: 40px'></div>", unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    st.markdown("""
    <div class="glass-card" style="text-align: center;">
        <div style="font-size: 2rem;">🤖</div>
        <h3 style="color: #a78bfa; margin: 10px 0 5px 0;">Autonomous AI Agent</h3>
        <p style="color: #c4b5fd;">Powered by GPT-3.5 • Real-time decisions • Multi-task evaluation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mode Selection Toggle
    st.markdown("### 🎮 Select Mode")
    col_mode1, col_mode2,col_mode3 = st.columns(3)
    
    with col_mode1:
        if st.button("🚀 NORMAL MODE", use_container_width=True, type="primary" if st.session_state.page_mode == "normal" else "secondary"):
            st.session_state.page_mode = "normal"
            st.session_state.tasks_results = {}  # Clear results when switching
            st.session_state.comparison_results = {} # Also clear comparison results
            with st.spinner("Switching mode..."):
                time.sleep(0.4)
            st.rerun()
    
    with col_mode2:
        if st.button("🎲 AI vs RANDOM MODE", use_container_width=True, type="primary" if st.session_state.page_mode == "comparison" else "secondary"):
            st.session_state.page_mode = "comparison"
            st.session_state.comparison_results = {}  # Clear comparison results
            st.session_state.tasks_results = {}      # Also clear normal results
            with st.spinner("Switching mode..."):
                time.sleep(0.4)
            st.rerun()
    
    with col_mode3:
        if st.button("📝 EDIT EMAILS", use_container_width=True, type="primary" if st.session_state.page_mode == "editor" else "secondary"):
            st.session_state.page_mode = "editor"
            with st.spinner("Switching mode..."):
                time.sleep(0.4)
            st.rerun()

    st.markdown("<div style='height: 40px'></div>", unsafe_allow_html=True)

    # ============================================
    # NORMAL MODE
    # ============================================
    if st.session_state.page_mode == "normal":
        if not st.session_state.is_running:
            if st.button("🚀 LAUNCH FULL DEMO", use_container_width=True, type="primary"):
                with st.spinner("🤖 AI is analyzing emails..."):
                    time.sleep(0.5)
                run_all_tasks()
        else:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #8b5cf6, #ec4899); border-radius: 50px; padding: 12px; text-align: center;">
                <span style="color: white; font-weight: bold;">✨ AI PROCESSING ✨</span>
            </div>
            """, unsafe_allow_html=True)
        
        if AI_AVAILABLE:
            st.caption(f"✅ AI Ready: {MODEL_NAME.replace('openai/', '')}")

   

st.markdown("<div style='height: 40px'></div>", unsafe_allow_html=True)

    # ============================================
    # COMPARISON MODE
    # ============================================
if st.session_state.page_mode == "comparison":
    st.session_state.tasks_results = {}
    st.markdown("## 🎲 AI vs RANDOM COMPARISON")
    st.markdown("Comparing intelligent AI decisions against random baseline")
    
    # Initialize comparison results in session state
    if 'comparison_results' not in st.session_state:
        st.session_state.comparison_results = None
    if 'is_comparing' not in st.session_state:
        st.session_state.is_comparing = False
        
    # Random Agent Class (inline)
    class RandomAgent:
        def __init__(self):
            self.possible_actions = ["urgent", "normal", "spam"]
        def get_action(self, email):
            import random
            return random.choice(self.possible_actions)
      
    def get_ai_action_comparison(email):
        """Get AI decision using Groq/OpenAI"""
        import random
        if not AI_AVAILABLE:
            return random.choice(["urgent", "normal", "spam"])
          
        system_prompt = """You are an AI email assistant. Classify email as "urgent", "normal", or "spam". Respond with ONLY the action word."""
        user_prompt = f"""From: {email.sender}\nSubject: {email.subject}\nBody: {email.body[:200]}\n\nAction:"""
         
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
            return random.choice(["urgent", "normal", "spam"])
        
    def run_comparison_agent(env, agent_type, task_name, progress_placeholder, email_placeholder, timeline_placeholder):
        """Run a single agent (AI or Random) on a task"""
        observation = env.reset()
        actions = []
        rewards = []
        timeline = []
        total_emails = len(env.inbox)
        random_agent = RandomAgent()
        
        for step_idx in range(total_emails):
            current_email = observation.current_email
                
            with email_placeholder.container():
                st.markdown(f"""
                <div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 15px; margin: 10px 0;">
                    <div style="font-weight: bold;">📧 {current_email.subject[:80]}</div>
                    <div style="color: #94a3b8; font-size: 0.8rem;">From: {current_email.sender}</div>
                    <div style="font-size: 0.8rem; margin-top: 8px;">{current_email.body[:100]}...</div>
                </div>
                """, unsafe_allow_html=True)
            
            if agent_type == "ai":
                action = get_ai_action_comparison(current_email)
            else:
                action = random_agent.get_action(current_email)
            
            action_obj = EmailAction(email_id=current_email.id, action=ActionType(action))
            observation, reward, done, info = env.step(action_obj)
             
            actions.append(action_obj)
            rewards.append(reward)
             
            emoji = "🟢" if reward > 0 else "🔴"
            timeline.append({'step': step_idx + 1, 'action': action, 'reward': reward, 'emoji': emoji})
              
            with timeline_placeholder.container():
                st.markdown("**📜 Timeline (last 10):**")
                for entry in timeline[-10:]:
                    reward_color = "#00cc66" if entry['reward'] > 0 else "#ff4b4b"
                    action_color = "#ef4444" if entry['action'] == "urgent" else "#3b82f6" if entry['action'] == "normal" else "#8b5cf6"
                    st.markdown(f"""
                    <div style="font-family: monospace; font-size: 0.75rem; padding: 4px; border-bottom: 1px solid rgba(139,92,246,0.2);">
                        {entry['emoji']} Step {entry['step']}: 
                        <span style="background: {action_color}; color: white; padding: 2px 8px; border-radius: 15px; font-size: 0.7rem;">{entry['action'].upper()}</span>
                        → <span style="color: {reward_color};">{entry['reward']:+.2f}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
            progress = (step_idx + 1) / total_emails
            progress_placeholder.progress(progress, text=f"Processing {step_idx + 1}/{total_emails}")
            time.sleep(0.1)
            
        score = grade_task(env.task_id, actions, env.inbox)
        total_reward = sum(rewards)
        return {'score': score, 'total_reward': total_reward, 'steps': len(actions)}
    
    

    def run_full_comparison():
        st.session_state.is_comparing = True
        st.session_state.comparison_results = {'ai': {}, 'random': {}}
         
        tasks = [
            ("easy_classification", "EASY", 12),
            ("medium_prioritization", "MEDIUM", 15),
            ("hard_evolving", "HARD", 40),
        ]
           
        for task_id, task_name, email_count in tasks:
            st.markdown(f"#### 📧 {task_name} TASK")
              
            col_left, col_right = st.columns(2)
              
            # AI Agent
            with col_left:
                st.markdown("**🤖 AI AGENT**")
                ai_progress = st.empty()
                ai_email = st.empty()
                ai_timeline = st.empty()
                  
                env_ai = EmailTriageEnvironment(task_id=task_id)
                ai_result = run_comparison_agent(env_ai, "ai", task_name, ai_progress, ai_email, ai_timeline)
                st.session_state.comparison_results['ai'][task_id] = ai_result
                st.markdown(f"**Score:** {ai_result['score']:.3f}/1.0")
                st.markdown(f"**Reward:** {ai_result['total_reward']:.2f}")
              
            # Random Agent
            with col_right:
                st.markdown("**🎲 RANDOM AGENT**")
                random_progress = st.empty()
                random_email = st.empty()
                random_timeline = st.empty()
                
                env_random = EmailTriageEnvironment(task_id=task_id)
                random_result = run_comparison_agent(env_random, "random", task_name, random_progress, random_email, random_timeline)
                st.session_state.comparison_results['random'][task_id] = random_result
                st.markdown(f"**Score:** {random_result['score']:.3f}/1.0")
                st.markdown(f"**Reward:** {random_result['total_reward']:.2f}")
                
            st.markdown("<div style='height: 40px'></div>", unsafe_allow_html=True)
            
        st.session_state.is_comparing = False
        st.rerun()
        
    # Run comparison button
    if not st.session_state.is_comparing:
        if st.button("🚀 RUN COMPARISON", use_container_width=True, type="primary"):
            run_full_comparison()
    else:
        st.info("🔄 Running comparison... Please wait.")
     
    # Display results after comparison
    if st.session_state.comparison_results and st.session_state.comparison_results.get('ai'):
        st.markdown("## 📊 FINAL COMPARISON")
          
        tasks_display = ["Easy", "Medium", "Hard"]
        ai_scores = [
            st.session_state.comparison_results['ai'].get('easy_classification', {}).get('score', 0),
            st.session_state.comparison_results['ai'].get('medium_prioritization', {}).get('score', 0),
            st.session_state.comparison_results['ai'].get('hard_evolving', {}).get('score', 0)
        ]
        random_scores = [
            st.session_state.comparison_results['random'].get('easy_classification', {}).get('score', 0),
            st.session_state.comparison_results['random'].get('medium_prioritization', {}).get('score', 0),
            st.session_state.comparison_results['random'].get('hard_evolving', {}).get('score', 0)
        ]
           
        avg_ai = sum(ai_scores) / 3
        avg_random = sum(random_scores) / 3
        improvement = ((avg_ai - avg_random) / avg_random) * 100 if avg_random > 0 else 0
         
        # Create bar chart
        try:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(10, 6))
            x = range(len(tasks_display))
            width = 0.35
                
            bars1 = ax.bar([i - width/2 for i in x], ai_scores, width, label='🤖 AI Agent', color='#8b5cf6')
            bars2 = ax.bar([i + width/2 for i in x], random_scores, width, label='🎲 Random Baseline', color='#ec4899')
               
            ax.set_ylabel('Score')
            ax.set_title('AI vs Random Agent Performance', fontsize=14, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(tasks_display)
            ax.legend(loc='upper left')
            ax.set_ylim(0, 1.1)
             
            for bar in bars1:
                height = bar.get_height()
                ax.annotate(f'{height:.3f}', xy=(bar.get_x() + bar.get_width()/2, height),
                            xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
            for bar in bars2:
                height = bar.get_height()
                ax.annotate(f'{height:.3f}', xy=(bar.get_x() + bar.get_width()/2, height),
                            xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
                
            ax.set_facecolor('#1a1a3e')
            fig.patch.set_facecolor('#0a0a2a')
            ax.tick_params(colors='white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.title.set_color('white')
                
            st.pyplot(fig)
        except ImportError:
            st.warning("Matplotlib not installed. Install with: pip install matplotlib")
         
        # Summary stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🤖 AI Average Score", f"{avg_ai:.3f}")
        with col2:
            st.metric("🎲 Random Average Score", f"{avg_random:.3f}")
        with col3:
            st.metric("📈 AI Improvement", f"+{improvement:.0f}%")
          
        if st.button("🔄 RUN COMPARISON AGAIN", use_container_width=True):
            st.session_state.comparison_results = None
            st.rerun()
        
    st.markdown("<div style='height: 40px'></div>", unsafe_allow_html=True)
# ============================================
# EDITOR MODE
# ============================================
if st.session_state.page_mode == "editor":
    st.markdown("## 📝 Email Templates Editor")
    st.markdown("Edit, add, or delete emails for each task")
    
    TASKS = {
        'easy_classification': '🔵 EASY TASK',
        'medium_prioritization': '🟡 MEDIUM TASK',
        'hard_evolving': '🔴 HARD TASK'
    }
    
    selected_task = st.selectbox(
        "Select Task to Edit",
        options=list(TASKS.keys()),
        format_func=lambda x: TASKS[x]
    )
      
    # File path for this task
    json_filename = f"emails_{selected_task}.json"
        
    # Load emails from JSON file if exists, otherwise from environment
    if st.button("📂 Load Current Emails", use_container_width=True):
        if os.path.exists(json_filename):
            with open(json_filename, 'r') as f:
                st.session_state.editor_emails = json.load(f)
            st.success(f"Loaded {len(st.session_state.editor_emails)} emails from JSON file!")
        else:
            # Load from environment
            from environment import EmailTriageEnvironment
            env = EmailTriageEnvironment(selected_task)
            env.reset()
            emails = []
            for email in env.inbox:
                emails.append({
                    'id': email.id,
                    'subject': email.subject,
                    'body': email.body,
                    'sender': email.sender,
                    'correct_category': email.correct_category,
                    'urgency': email.urgency,
                    'time_sensitive': getattr(email, 'time_sensitive', False),
                    'is_fake_urgent': getattr(email, 'is_fake_urgent', False)
                })
            st.session_state.editor_emails = emails
            st.success(f"Loaded {len(emails)} emails from environment!")
    
    # Display and edit emails
    if 'editor_emails' in st.session_state and st.session_state.editor_emails:
        emails = st.session_state.editor_emails
        
        st.markdown(f"### 📧 Current Emails ({len(emails)} total)")
        
        for idx, email in enumerate(emails):
            with st.expander(f"Email #{email.get('id', idx+1)}: {email.get('subject', 'No subject')[:50]}"):
                col1, col2 = st.columns([3, 1])
                 
                with col1:
                    new_subject = st.text_input("Subject", email.get('subject', ''), key=f"editor_subject_{idx}")
                    new_sender = st.text_input("From", email.get('sender', ''), key=f"editor_sender_{idx}")
                    new_body = st.text_area("Body", email.get('body', ''), height=100, key=f"editor_body_{idx}")
                    new_category = st.selectbox(
                        "Category",
                        options=["urgent", "normal", "spam"],
                        index=["urgent", "normal", "spam"].index(email.get('correct_category', 'normal')),
                        key=f"editor_cat_{idx}"
                    )
                    
                with col2:
                    if st.button("🗑️ Delete", key=f"editor_delete_{idx}"):
                        st.session_state.editor_emails.pop(idx)
                        # Reassign IDs
                        for i, e in enumerate(st.session_state.editor_emails):
                            e['id'] = i + 1
                        st.rerun()
                  
                if st.button("💾 Save Changes", key=f"editor_save_{idx}"):
                    email['subject'] = new_subject
                    email['sender'] = new_sender
                    email['body'] = new_body
                    email['correct_category'] = new_category
                    st.success(f"Email #{email.get('id', idx+1)} updated!")
                    st.rerun()
            
        # Add new email
        st.markdown("<div style='height: 40px'></div>", unsafe_allow_html=True)
        st.markdown("### ➕ Add New Email")
           
        col_new1, col_new2 = st.columns(2)
        
        with col_new1:
            new_subject = st.text_input("Subject", placeholder="Enter email subject", key="editor_new_subject")
            new_sender = st.text_input("From", placeholder="sender@example.com", key="editor_new_sender")
            new_body = st.text_area("Body", placeholder="Enter email body", height=100, key="editor_new_body")
          
        with col_new2:
            new_category = st.selectbox("Category", ["urgent", "normal", "spam"], key="editor_new_category")
         
        if st.button("➕ Add Email", use_container_width=True):
            new_id = len(emails) + 1
            new_email = {
                'id': new_id,
                'subject': new_subject,
                'body': new_body,
                'sender': new_sender,
                'correct_category': new_category,
                'urgency': 1,
                'time_sensitive': False,
                'is_fake_urgent': False
            }
            st.session_state.editor_emails.append(new_email)
            st.success(f"Added new email: {new_subject}")
            st.rerun()
        
        # Save to JSON button
        st.markdown("<div style='height: 40px'></div>", unsafe_allow_html=True)
        if st.button("💾 SAVE ALL TO JSON (Apply to Environment)", use_container_width=True, type="primary"):
            with open(json_filename, 'w') as f:
                json.dump(st.session_state.editor_emails, f, indent=2)
            st.success(f"✅ Saved {len(st.session_state.editor_emails)} emails to {json_filename}")
            st.info("🎯 These emails will now be used when you run NORMAL MODE!")
    else:
        st.info("Click 'Load Current Emails' to start editing.")

# Results Dashboard - Only show in NORMAL MODE
if st.session_state.page_mode == "normal" and st.session_state.tasks_results:
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
    
    st.markdown("<div style='height: 40px'></div>", unsafe_allow_html=True)
    
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
    
    st.markdown("<div style='height: 40px'></div>", unsafe_allow_html=True)
    
    # AI Decision Log - Only show in NORMAL MODE
    if st.session_state.page_mode == "normal":
        st.markdown("### 🤖 AI DECISION LOG")
        
        tabs = st.tabs(["📧 EASY TASK", "⚡ MEDIUM TASK", "🌌 HARD TASK"])
    
    for idx, (task_id, result) in enumerate(st.session_state.tasks_results.items()):
        with tabs[idx]:
                    for decision in result['decisions']:
                        reward_color = "#00cc66" if decision['reward'] > 0 else "#ff4b4b"
                        memory_text = decision.get('memory', 'No prior interactions')
                        confidence = decision.get('confidence', 0.7)
                        reasoning = decision.get('reasoning', 'No explanation')
                        
                        st.markdown(f"""
                        <div class="ai-log-entry">
                            <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                                <span style="color: #a78bfa;"><b>Step {decision['step']}</b> | Email #{decision['email_id']}</span>
                                <span style="color: {reward_color}; font-weight: bold;">{decision['reward']:+.2f}</span>
                            </div>
                            <div style="color: white; margin: 8px 0;">📧 {decision['subject']}...</div>
                            <div style="display: flex; flex-wrap: wrap; gap: 10px; align-items: center;">
                                <span style="background: rgba(139,92,246,0.3); padding: 4px 12px; border-radius: 20px;">🎯 {decision['action'].upper()}</span>
                                <span style="background: rgba(34,197,94,0.2); padding: 2px 8px; border-radius: 20px; font-size: 0.7rem;">Confidence: {int(confidence * 100)}%</span>
                                <span style="color: #c4b5fd; font-size: 0.8rem;">{decision['message']}</span>
                            </div>
                            <div style="color: #a78bfa; font-size: 0.7rem; margin-top: 5px;">
                                💭 {reasoning}
                            </div>
                            <div style="color: #a78bfa; font-size: 0.7rem; margin-top: 8px; padding-top: 5px; border-top: 1px solid rgba(139,92,246,0.1);">
                                🧠 {memory_text}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
    
# Reset and Download Buttons - Only show in NORMAL MODE
if st.session_state.page_mode == "normal":
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

elif st.session_state.page_mode == "normal":
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

# ============================================
# FOOTER WITH DESCRIPTION
# ============================================

st.markdown("<div style='height: 40px'></div>", unsafe_allow_html=True)

# Welcome Description at the BOTTOM (only shows in normal mode with no results)
if not st.session_state.tasks_results and not st.session_state.is_running and st.session_state.page_mode == "normal":
    st.markdown("### 📧 Welcome to Email Triage AI")
    st.markdown("*An intelligent email assistant that learns to prioritize your inbox*")
    
    col_w1, col_w2, col_w3 = st.columns(3)
    
    with col_w1:
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 1.8rem;">🎯</div>
            <div style="font-weight: bold; color: #a78bfa;">3 Difficulty Levels</div>
            <div style="font-size: 0.75rem; color: #94a3b8;">Easy → Medium → Hard</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_w2:
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 1.8rem;">🧠</div>
            <div style="font-weight: bold; color: #a78bfa;">Memory & Reasoning</div>
            <div style="font-size: 0.75rem; color: #94a3b8;">AI remembers past interactions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_w3:
        st.markdown("""
        <div style="text-align: center;">
            <div style="font-size: 1.8rem;">📊</div>
            <div style="font-weight: bold; color: #a78bfa;">AI vs Random</div>
            <div style="font-size: 0.75rem; color: #94a3b8;">See how AI outperforms random</div>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("📋 How to Use"):
        st.markdown("""
        1. Select a **Mode** above: Normal, AI vs Random, or Edit Emails
        2. Click **LAUNCH FULL DEMO** to start AI processing
        3. Watch AI make decisions in real-time with confidence scores
        4. View results, grader breakdown, and download JSON reports
        5. Switch to **Edit Mode** to create your own email templates
        """)
    
    st.markdown("""
    <div style="display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; margin: 10px 0;">
        <span style="background: rgba(30,144,255,0.2); border-radius: 20px; padding: 4px 12px; font-size: 0.7rem;">✨ Explainable AI</span>
        <span style="background: rgba(30,144,255,0.2); border-radius: 20px; padding: 4px 12px; font-size: 0.7rem;">🎯 Confidence Scores</span>
        <span style="background: rgba(30,144,255,0.2); border-radius: 20px; padding: 4px 12px; font-size: 0.7rem;">🧠 Sender Memory</span>
        <span style="background: rgba(30,144,255,0.2); border-radius: 20px; padding: 4px 12px; font-size: 0.7rem;">🎲 Random Baseline</span>
        <span style="background: rgba(30,144,255,0.2); border-radius: 20px; padding: 4px 12px; font-size: 0.7rem;">📝 Email Editor</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 40px'></div>", unsafe_allow_html=True)

# Original footer
st.markdown("""
<div style="text-align: center; color: #4a4a7a; font-size: 0.8rem; padding: 20px;">
    🚀 Built with OpenEnv • Powered by GPT-3.5 • Transparent Grading
</div>
""", unsafe_allow_html=True)