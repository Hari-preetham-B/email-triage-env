"""
models.py - Defines the data structures for our Email Triage Environment.

This file tells OpenEnv:
- What an "observation" looks like (what the AI sees)
- What an "action" looks like (what the AI can do)
- What "reward" looks like (how we score the AI)
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from enum import Enum

# Sender Profile for Multi-User Simulation
class SenderProfile(BaseModel):
    """Profile for each email sender with personality and history"""
    name: str = Field(description="Sender's name")
    email: str = Field(description="Sender's email address")
    personality: str = Field(description="Personality type: urgent-prone, casual, formal, spammy, crisis-mode")
    trust_level: int = Field(default=5, ge=1, le=10, description="Trust level 1-10")
    previous_topics: List[str] = Field(default_factory=list, description="Topics from past emails")
    previous_urgency: List[int] = Field(default_factory=list, description="Urgency levels from past emails")
# === 1. Define what an EMAIL looks like (FULL version with hidden fields) ===

class Email(BaseModel):
    """
    Represents a single email in the inbox.
    This is the FULL email with hidden grading fields.
    The AI never sees this directly.
    """
    id: int = Field(description="Unique email ID")
    subject: str = Field(description="Email subject line")
    body: str = Field(description="Email content")
    sender: str = Field(description="Sender email address")
    
    # These are "hidden" fields - the AI doesn't see them
    # They're used by the grader to score the AI
    correct_category: str = Field(default="normal", description="Ground truth category")
    urgency: int = Field(default=1, ge=1, le=3, description="Urgency 1=low, 2=medium, 3=high")

    # NEW FIELDS for sophisticated hard task
    time_sensitive: bool = Field(default=False, description="Whether email expires")
    expires_in: int = Field(default=999, description="Steps before email expires")
    is_fake_urgent: bool = Field(default=False, description="Fake urgency detection")
    fake_reason: str = Field(default="", description="Why this is fake urgent")


# === 2. Define what the AI SEES (VIEW version - no hidden fields) ===
# This MUST come before EmailObservation

class EmailView(BaseModel):
    """
    What the AI actually sees — correct_category and urgency are HIDDEN!
    The AI only gets the information a human would see.
    """
    id: int = Field(description="Unique email ID")
    subject: str = Field(description="Email subject line")
    body: str = Field(description="Email content")
    sender: str = Field(description="Sender email address")


# === 3. Define what the AI CAN DO (Actions) ===

class ActionType(str, Enum):
    """All possible actions the AI can take on an email."""
    MARK_URGENT = "urgent"      # Mark as high priority
    MARK_NORMAL = "normal"      # Mark as normal priority
    MARK_SPAM = "spam"          # Mark as spam
    DELETE = "delete"           # Delete email
    ARCHIVE = "archive"         # Archive (done but keep)
    SKIP = "skip"               # Skip for now, come back later


# === 4. Define the ACTION model ===

class EmailAction(BaseModel):
    """
    The action the AI takes.
    
    When the AI wants to do something, it sends an object like:
    {"email_id": 3, "action": "urgent"}
    """
    email_id: int = Field(description="Which email to act on")
    action: ActionType = Field(description="What to do with it")


# === 5. Define what the AI SEES (Observation) ===

class EmailObservation(BaseModel):
    """
    What the AI sees at each step.
    The AI does NOT see correct_category or urgency.
    """
    current_email: EmailView = Field(description="The email currently being processed")
    remaining_count: int = Field(description="How many emails left to process")
    inbox_summary: Optional[str] = Field(
        default=None, 
        description="Brief summary of remaining emails (optional)"
    )
    step_number: int = Field(description="Which step we're on")
    last_action_result: Optional[str] = Field(
        default=None,
        description="Result of last action (success/error message)"
    )


# === 6. Define the REWARD model ===

class EmailReward(BaseModel):
    """
    The reward signal sent back after each action.
    
    Positive values = good, negative = bad.
    We include a breakdown so we can debug.
    """
    score: float = Field(description="Total reward for this step")
    breakdown: dict = Field(
        default_factory=dict,
        description="Detailed breakdown of how score was calculated"
    )
    is_terminal: bool = Field(
        default=False,
        description="Whether this reward ends the episode"
    )