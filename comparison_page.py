"""
comparison_page.py - AI vs Random Agent Comparison
Shows side-by-side performance of AI agent vs random baseline
"""

import streamlit as st
import time
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import webbrowser
# Import your environment
from environment import EmailTriageEnvironment
from models import EmailAction, ActionType
from random_agent import RandomAgent
from tasks import grade_task

# Page configuration
st.set_page_config(
    page_title="AI vs Random | Email Triage",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a2a 0%, #1a1a3e 50%, #0d0d2b 100%);
        background-attachment: fixed;
    }
    .comparison-header {
        text-align: center;
        padding: 20px;
        background: rgba(15, 15, 40, 0.6);
        border-radius: 20px;
        margin-bottom: 20px;
    }
    .comparison-header h1 {
        background: linear-gradient(135deg, #8b5cf6, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2rem;
    }
    .agent-card {
        background: rgba(15, 15, 40, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(139, 92, 246, 0.3);
        height: 100%;
    }
    .ai-title {
        color: #8b5cf6;
        text-align: center;
        font-size: 1.5rem;
        margin-bottom: 15px;
    }
    .random-title {
        color: #ec4899;
        text-align: center;
        font-size: 1.5rem;
        margin-bottom: 15px;
    }
    .live-email {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
    }
    .decision-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
    }
    .urgent-badge { background: #ef4444; color: white; }
    .normal-badge { background: #3b82f6; color: white; }
    .spam-badge { background: #8b5cf6; color: white; }
    .timeline-entry {
        font-family: monospace;
        font-size: 0.75rem;
        padding: 4px;
        border-bottom: 1px solid rgba(139,92,246,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'comparison_results' not in st.session_state:
    st.session_state.comparison_results = None
if 'is_running' not in st.session_state:
    st.session_state.is_running = False

# Initialize AI Client
AI_AVAILABLE = False
try:
    from openai import OpenAI
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    API_KEY = os.getenv("OPENAI_API_KEY")
    API_BASE_URL = os.getenv("API_BASE_URL", "https://api.groq.com/openai/v1")
    MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
    
    if API_KEY:
        client = OpenAI(api_key=API_KEY, base_url=API_BASE_URL)
        AI_AVAILABLE = True
except:
    AI_AVAILABLE = False


def get_ai_action(email):
    """Get AI decision using Groq/OpenAI"""
    if not AI_AVAILABLE:
        return "normal", 0.5
    
    system_prompt = """You are an AI email assistant. Classify email as "urgent", "normal", or "spam". 
    Respond with ONLY the action word."""
    
    user_prompt = f"""From: {email.sender}
Subject: {email.subject}
Body: {email.body[:200]}

Action:"""
    
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
            return "urgent", 0.9
        elif "spam" in response:
            return "spam", 0.9
        else:
            return "normal", 0.8
    except:
        return "normal", 0.5


def run_single_agent(env, agent_type, agent, task_name, progress_placeholder, email_placeholder, timeline_placeholder):
    """
    Run a single agent (AI or Random) on a task
    
    agent_type: "ai" or "random"
    agent: function that returns action
    """
    observation = env.reset()
    actions = []
    rewards = []
    timeline = []
    total_emails = len(env.inbox)
    
    for step_idx in range(total_emails):
        current_email = observation.current_email
        
        # Show current email
        with email_placeholder.container():
            st.markdown(f"""
            <div class="live-email">
                <div style="font-weight: bold;">📧 {current_email.subject[:80]}</div>
                <div style="color: #94a3b8; font-size: 0.8rem;">From: {current_email.sender}</div>
                <div style="font-size: 0.8rem; margin-top: 8px;">{current_email.body[:100]}...</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Get action from agent
        if agent_type == "ai":
            action, confidence = get_ai_action(current_email)
        else:
            action = agent.get_action(current_email)
        
        # Take action
        action_obj = EmailAction(email_id=current_email.id, action=ActionType(action))
        observation, reward, done, info = env.step(action_obj)
        
        actions.append(action_obj)
        rewards.append(reward)
        
        # Update timeline
        emoji = "🟢" if reward > 0 else "🔴"
        timeline.append({
            'step': step_idx + 1,
            'action': action,
            'reward': reward,
            'emoji': emoji
        })
        
        # Show timeline (last 10)
        with timeline_placeholder.container():
            st.markdown("**📜 Timeline (last 10):**")
            for entry in timeline[-10:]:
                reward_color = "#00cc66" if entry['reward'] > 0 else "#ff4b4b"
                st.markdown(f"""
                <div class="timeline-entry">
                    {entry['emoji']} Step {entry['step']}: 
                    <span class="{entry['action']}-badge decision-badge">{entry['action'].upper()}</span>
                    → <span style="color: {reward_color};">{entry['reward']:+.2f}</span>
                </div>
                """, unsafe_allow_html=True)
        
        # Update progress
        progress = (step_idx + 1) / total_emails
        progress_placeholder.progress(progress, text=f"Processing {step_idx + 1}/{total_emails}")
        time.sleep(0.1)
    
    # Calculate score
    score = grade_task(env.task_id, actions, env.inbox)
    total_reward = sum(rewards)
    
    return {
        'score': score,
        'total_reward': total_reward,
        'steps': len(actions),
        'timeline': timeline
    }


def run_comparison():
    """Run comparison between AI and Random agent on all tasks"""
    st.session_state.is_running = True
    st.session_state.comparison_results = {
        'ai': {},
        'random': {}
    }
    
    tasks = [
        ("easy_classification", "EASY", 12),
        ("medium_prioritization", "MEDIUM", 15),
        ("hard_evolving", "HARD", 40),
    ]
    
    random_agent = RandomAgent()
    
    # Create placeholders for both sides
    col_left, col_right = st.columns(2)
    
    ai_results_placeholder = {}
    random_results_placeholder = {}
    
    for task_id, task_name, email_count in tasks:
        # Left side (AI)
        with col_left:
            st.markdown(f"#### 📧 {task_name} TASK")
            ai_progress = st.empty()
            ai_email = st.empty()
            ai_timeline = st.empty()
            
            env_ai = EmailTriageEnvironment(task_id=task_id)
            ai_result = run_single_agent(env_ai, "ai", None, task_name, ai_progress, ai_email, ai_timeline)
            st.session_state.comparison_results['ai'][task_id] = ai_result
            st.markdown(f"**Score:** {ai_result['score']:.3f}/1.0 | **Total Reward:** {ai_result['total_reward']:.2f}")
            st.markdown("---")
        
        # Right side (Random)
        with col_right:
            st.markdown(f"#### 🎲 {task_name} TASK (Random)")
            random_progress = st.empty()
            random_email = st.empty()
            random_timeline = st.empty()
            
            env_random = EmailTriageEnvironment(task_id=task_id)
            random_result = run_single_agent(env_random, "random", random_agent, task_name, random_progress, random_email, random_timeline)
            st.session_state.comparison_results['random'][task_id] = random_result
            st.markdown(f"**Score:** {random_result['score']:.3f}/1.0 | **Total Reward:** {random_result['total_reward']:.2f}")
            st.markdown("---")
    
    st.session_state.is_running = False
    st.rerun()


# ============================================
# MAIN UI
# ============================================

st.markdown("""
<div class="comparison-header">
    <h1>🎲 AI vs RANDOM AGENT</h1>
    <p>Comparing intelligent AI decisions against random baseline</p>
</div>
""", unsafe_allow_html=True)

# Back button
col_back, col_spacer = st.columns([1, 5])
with col_back:
    if st.button("← BACK TO MAIN DASHBOARD"):
        import webbrowser
        webbrowser.open_new_tab("http://localhost:8501")
        st.info("Main dashboard opened in new tab. Close this tab to return.")

st.markdown("---")

# Run comparison button
if not st.session_state.is_running:
    if st.button("🚀 RUN COMPARISON", use_container_width=True, type="primary"):
        run_comparison()
else:
    st.info("🔄 Running comparison... Please wait.")

st.markdown("---")

# Display Results
if st.session_state.comparison_results:
    st.markdown("## 📊 FINAL COMPARISON")
    
    # Prepare data for chart
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
    
    # Add value labels on bars
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
    
    # Summary stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🤖 AI Average Score", f"{avg_ai:.3f}")
    with col2:
        st.metric("🎲 Random Average Score", f"{avg_random:.3f}")
    with col3:
        st.metric("📈 AI Improvement", f"+{improvement:.0f}%", delta=f"{improvement:.0f}% better than random")
    
    # Reset button
    if st.button("🔄 RUN COMPARISON AGAIN", use_container_width=True):
        st.session_state.comparison_results = None
        st.rerun()

else:
    st.info("👆 Click 'RUN COMPARISON' to see AI vs Random agent performance!")