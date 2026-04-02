"""
environment.py - The main Email Triage Environment

This is the brain of your environment. It handles:
- reset(): Start a new email inbox with tasks
- step(): Process AI actions and return rewards
- state(): Return current environment state
"""

from typing import Optional, Tuple, List, Dict
from models import (
    Email, EmailAction, EmailObservation, EmailReward, ActionType, EmailView
)


class EmailTriageEnvironment:
    """
    Email Triage Environment for AI agents.
    
    The AI must process emails by classifying them correctly:
    - urgent: High priority, needs immediate attention
    - normal: Regular email, can wait
    - spam: Junk email, should be filtered out
    
    The environment gives partial rewards as the AI works through the inbox.
    """
    
    def __init__(self, task_id: str = "easy_classification"):
        """
        Initialize the environment.
        
        Args:
            task_id: Which task to run ("easy_classification", 
                     "medium_prioritization", or "hard_evolving")
        """
        self.task_id = task_id
        self.inbox: List[Email] = []      # All emails in current session
        self.processed: List[Email] = []   # Emails already handled
        self.current_index: int = 0        # Which email we're on
        self.step_count: int = 0           # Number of steps taken
        self.max_steps: int = 50           # Limit to prevent infinite loops
        self.done: bool = False            # Whether task is complete
        
        # Populate inbox based on selected task
        self._setup_task()
    
    def _setup_task(self):
        """
        Create emails for the selected task.
        Each task has different difficulty levels.
        """
        if self.task_id == "easy_classification":
            self._setup_easy_task()
        elif self.task_id == "medium_prioritization":
            self._setup_medium_task()
        elif self.task_id == "hard_evolving":
            self._setup_hard_task()
        else:
            # Default to easy task if unknown
            self._setup_easy_task()
    
    def _setup_easy_task(self):
        """
        EASY TASK: 3 emails with clear signals.
        
        These emails are obvious:
        - Email 1: Clear urgent (server down)
        - Email 2: Clear normal (team meeting)
        - Email 3: Clear spam (lottery winner)
        """
        self.inbox = [
            Email(
                id=1,
                subject="URGENT: Production Server Down",
                body="The main server is not responding. Customer facing issues!",
                sender="alert@company.com",
                correct_category="urgent",
                urgency=3
            ),
            Email(
                id=2,
                subject="Weekly Team Meeting",
                body="Reminder: Team sync at 2 PM tomorrow",
                sender="manager@company.com",
                correct_category="normal",
                urgency=1
            ),
            Email(
                id=3,
                subject="YOU WON $1,000,000!!!",
                body="Click here to claim your prize!",
                sender="lottery@spam.com",
                correct_category="spam",
                urgency=1
            ),
        ]
    
    def _setup_medium_task(self):
        """
        MEDIUM TASK: 5 emails with subtle differences.
        
        These emails require careful reading:
        - Some emails look urgent but aren't
        - Some look normal but are actually important
        """
        self.inbox = [
            Email(
                id=1,
                subject="RE: Project Deadline",
                body="Can we extend by one day? Almost done.",
                sender="junior@company.com",
                correct_category="normal",
                urgency=1
            ),
            Email(
                id=2,
                subject="IMPORTANT: Client Review",
                body="The client meeting is at 3 PM today. Please attend.",
                sender="client@bigcompany.com",
                correct_category="urgent",
                urgency=3
            ),
            Email(
                id=3,
                subject="Free Gift Card Inside",
                body="You've been selected for a free $50 gift card!",
                sender="promo@retail.com",
                correct_category="spam",
                urgency=1
            ),
            Email(
                id=4,
                subject="Your Payroll Update",
                body="Please verify your information for next month's payroll",
                sender="hr@company.com",
                correct_category="urgent",
                urgency=2
            ),
            Email(
                id=5,
                subject="Newsletter: Weekly Updates",
                body="Here's what happened this week...",
                sender="updates@newsletter.com",
                correct_category="normal",
                urgency=1
            ),
        ]
    
    def _setup_hard_task(self):
        """
        SOPHISTICATED HARD TASK: 20+ emails with fake urgency, time pressure
        
        Features:
        - 20 emails to process
        - Fake urgency detection (spoofed "URGENT" from non-urgent senders)
        - Emotional manipulation emails
        - Time-sensitive emails that "expire"
        - Priority scoring system
        """
        self.inbox = []
        
        # Email 1: Real urgent - system failure
        self.inbox.append(Email(
            id=1, subject="🚨 CRITICAL: Database Migration Failed", 
            body="The database migration has failed. Customer data may be at risk. Immediate action required.",
            sender="tech-alerts@company.com", correct_category="urgent", urgency=3,
            time_sensitive=True, expires_in=3
        ))
        
        # Email 2: Fake urgency - sales spam disguised as urgent
        self.inbox.append(Email(
            id=2, subject="URGENT: Your account will be closed", 
            body="This is your FINAL WARNING. Your account will be permanently closed if you don't click this link within 24 hours!",
            sender="security@fake-scam.com", correct_category="spam", urgency=1,
            is_fake_urgent=True, fake_reason="Scam tactic - creates false urgency"
        ))
        
        # Email 3: Real normal - team update
        self.inbox.append(Email(
            id=3, subject="Weekly Development Update", 
            body="Here's what the team worked on this week. No blockers currently.",
            sender="tech-lead@company.com", correct_category="normal", urgency=1
        ))
        
        # Email 4: Fake urgent - spoofed CEO email
        self.inbox.append(Email(
            id=4, subject="IMMEDIATE: Wire transfer needed", 
            body="I need you to process a wire transfer of $50,000 immediately. Don't tell anyone.",
            sender="ceo@company.com", correct_category="spam", urgency=1,
            is_fake_urgent=True, fake_reason="Spoofed CEO email - common phishing tactic"
        ))
        
        # Email 5: Real urgent - client escalation
        self.inbox.append(Email(
            id=5, subject="ESCALATION: Client threatening to leave", 
            body="Major client is unhappy with response time. Please call them back within 1 hour.",
            sender="account-manager@company.com", correct_category="urgent", urgency=3,
            time_sensitive=True, expires_in=2
        ))
        
        # Email 6: Normal - meeting invite
        self.inbox.append(Email(
            id=6, subject="Team Sync: Friday 2 PM", 
            body="Let's sync on project progress. Agenda attached.",
            sender="project-manager@company.com", correct_category="normal", urgency=1
        ))
        
        # Email 7: Spam - lottery scam
        self.inbox.append(Email(
            id=7, subject="YOU WON $10,000,000!!!", 
            body="CONGRATULATIONS! You have won our grand prize. Send $500 to claim.",
            sender="lottery-winner@scam.net", correct_category="spam", urgency=1
        ))
        
        # Email 8: Fake urgent - fake invoice
        self.inbox.append(Email(
            id=8, subject="PAST DUE: Invoice #INV-2024-001", 
            body="Your payment is 30 days overdue. Immediate action required to avoid penalties.",
            sender="billing@fake-vendor.com", correct_category="spam", urgency=1,
            is_fake_urgent=True, fake_reason="Fake invoice phishing scam"
        ))
        
        # Email 9: Real urgent - security breach
        self.inbox.append(Email(
            id=9, subject="SECURITY ALERT: Unauthorized access detected", 
            body="Someone accessed sensitive files from unknown IP. Investigate immediately.",
            sender="security@company.com", correct_category="urgent", urgency=3,
            time_sensitive=True, expires_in=1
        ))
        
        # Email 10: Normal - newsletter
        self.inbox.append(Email(
            id=10, subject="Monthly Product Newsletter", 
            body="Check out our new features and updates for this month.",
            sender="product@company.com", correct_category="normal", urgency=1
        ))
        
        # Email 11: Fake urgent - emotional manipulation
        self.inbox.append(Email(
            id=11, subject="HELP: Family emergency", 
            body="I'm stuck abroad and need money urgently. Please send $2000 to this account.",
            sender="friend@compromised.com", correct_category="spam", urgency=1,
            is_fake_urgent=True, fake_reason="Emotional manipulation - fake family emergency"
        ))
        
        # Email 12: Real normal - HR update
        self.inbox.append(Email(
            id=12, subject="Benefits Enrollment Period", 
            body="Open enrollment for benefits starts next week. Review your options.",
            sender="hr@company.com", correct_category="normal", urgency=1
        ))
        
        # Email 13: Real urgent - server down
        self.inbox.append(Email(
            id=13, subject="🔴 PRODUCTION SERVER DOWN", 
            body="Main production server is unresponsive. Customers cannot access the platform.",
            sender="monitoring@company.com", correct_category="urgent", urgency=3,
            time_sensitive=True, expires_in=2
        ))
        
        # Email 14: Spam - fake refund
        self.inbox.append(Email(
            id=14, subject="Your refund of $499 is pending", 
            body="Click here to claim your refund. Limited time offer.",
            sender="refund-center@spam.com", correct_category="spam", urgency=1
        ))
        
        # Email 15: Normal - code review request
        self.inbox.append(Email(
            id=15, subject="Code Review: Feature Branch", 
            body="Please review my pull request when you have time.",
            sender="developer@company.com", correct_category="normal", urgency=2
        ))
        
        # Email 16: Fake urgent - fake legal notice
        self.inbox.append(Email(
            id=16, subject="LEGAL NOTICE: Lawsuit pending", 
            body="You are being sued. Click here to view the court documents immediately.",
            sender="legal-court@scam.com", correct_category="spam", urgency=1,
            is_fake_urgent=True, fake_reason="Fake legal notice - intimidation tactic"
        ))
        
        # Email 17: Real urgent - client complaint
        self.inbox.append(Email(
            id=17, subject="COMPLAINT: Product not working", 
            body="VIP client reported critical bug in production. Needs immediate fix.",
            sender="support@company.com", correct_category="urgent", urgency=3,
            time_sensitive=True, expires_in=3
        ))
        
        # Email 18: Normal - team lunch
        self.inbox.append(Email(
            id=18, subject="Team Lunch - Friday", 
            body="We're ordering pizza at noon. Let me know dietary restrictions.",
            sender="office@company.com", correct_category="normal", urgency=1
        ))
        
        # Email 19: Spam - fake job offer
        self.inbox.append(Email(
            id=19, subject="JOB OFFER: $200k/year remote", 
            body="We're impressed with your profile. Send your resume to apply.",
            sender="recruiter@fake-job.com", correct_category="spam", urgency=1
        ))
        
        # Email 20: Real urgent - data breach
        self.inbox.append(Email(
            id=20, subject="DATA BREACH: Customer info exposed", 
            body="Customer database may have been compromised. Security team needs your help.",
            sender="security@company.com", correct_category="urgent", urgency=3,
            time_sensitive=True, expires_in=1
        ))
    
    def reset(self) -> EmailObservation:
        """
        Start a new session.
        
        This clears all state and gives the AI a fresh inbox.
        
        Returns:
            EmailObservation: The first email the AI sees
        """
        # Reset all state variables
        self.processed = []
        self.current_index = 0
        self.step_count = 0
        self.done = False
        
        # Re-initialize inbox based on task
        if self.task_id == "easy_classification":
            self._setup_easy_task()
        elif self.task_id == "medium_prioritization":
            self._setup_medium_task()
        elif self.task_id == "hard_evolving":
            self._setup_hard_task()
        
        # Return the first email observation
        return self._get_current_observation()
    
    def step(self, action: EmailAction) -> Tuple[EmailObservation, float, bool, dict]:
        """
        Process one AI action.
        
        This is called every time the AI takes an action.
        
        Args:
            action: The AI's decision (which email, what action)
            
        Returns:
            observation: What the AI sees next
            reward: Score for this action
            done: Whether the task is complete
            info: Additional debug information
        """
        # Prevent actions if task is already done
        if self.done:
            return self._get_current_observation(), 0.0, True, {"error": "Episode already done"}
        
        # Increment step counter
        self.step_count += 1
        
        # Check if we've exceeded max steps
        if self.step_count >= self.max_steps:
            self.done = True
            return self._get_current_observation(), -1.0, True, {"error": "Max steps exceeded"}
        
        # Get the current email
        current_email = self.inbox[self.current_index]
        
        # Calculate reward based on action correctness
        reward, breakdown = self._calculate_reward(action, current_email)
        
        # Process the action (mark as processed, move to next)
        self._process_action(action, current_email)
        
        # For hard task: add new emails periodically (every 3 steps)
        if self.task_id == "hard_evolving" and hasattr(self, 'pending_emails'):
            if self.step_count % 3 == 0 and self.step_count < 15 and self.pending_emails:
                new_email = self.pending_emails.pop(0)
                self.inbox.append(new_email)
        
        # Move to next email
        self.current_index += 1
        
        # Check if we're done (all emails processed)
        if self.current_index >= len(self.inbox):
            self.done = True
        
        # Get next observation
        observation = self._get_current_observation()
        
        # Add last action result to observation
        observation.last_action_result = breakdown.get("message", "")
        
        return observation, reward, self.done, {"breakdown": breakdown}
    
    def _calculate_reward(self, action: EmailAction, email: Email) -> Tuple[float, dict]:
        """
        Calculate reward for an action.
        
        Positive rewards for correct actions.
        Negative rewards for mistakes.
        Small penalties for inefficient actions.
        
        Returns:
            reward: Float score
            breakdown: Dictionary explaining how reward was calculated
        """
        breakdown = {}
        reward = 0.0
        
        # Check if action is on wrong email
        if action.email_id != email.id:
            reward = -0.5
            breakdown["message"] = f"Wrong email! Acted on {action.email_id}, current is {email.id}"
            return reward, breakdown
        
        # Compare action to correct category
        action_str = action.action.value
        correct = email.correct_category
        
        if action_str == correct:
            # Perfect match!
            if correct == "urgent":
                reward = 0.5
                breakdown["message"] = f"✓ Correctly marked urgent! (+0.5)"
            elif correct == "normal":
                reward = 0.3
                breakdown["message"] = f"✓ Correctly marked normal (+0.3)"
            else:  # spam
                reward = 0.4
                breakdown["message"] = f"✓ Correctly marked spam (+0.4)"
        else:
            # Wrong classification - penalize based on severity
            if correct == "urgent" and action_str != "urgent":
                # Missing urgent email is a big mistake
                reward = -0.8
                breakdown["message"] = f"✗ MISSED URGENT EMAIL! (-0.8)"
            elif correct == "spam" and action_str != "spam":
                # Keeping spam is a medium mistake
                reward = -0.4
                breakdown["message"] = f"✗ Failed to mark spam (-0.4)"
            elif correct == "normal" and action_str == "spam":
                # Marking normal as spam is medium mistake
                reward = -0.3
                breakdown["message"] = f"✗ Marked normal as spam (-0.3)"
            elif correct == "normal" and action_str == "urgent":
                # Over-urgenting is small mistake
                reward = -0.2
                breakdown["message"] = f"✗ Marked normal as urgent (-0.2)"
            else:
                reward = -0.2
                breakdown["message"] = f"✗ Wrong: {action_str} should be {correct} (-0.2)"
        
        # Add small penalty for delete/archive if not appropriate
        if action.action in [ActionType.DELETE, ActionType.ARCHIVE] and correct != "spam":
            reward -= 0.1
            breakdown["message"] += f", deleted legitimate email (-0.1)"
        
        return reward, breakdown
    
    def _process_action(self, action: EmailAction, email: Email):
        """
        Record that an email has been processed.
        In a real system, this might also perform the action.
        """
        self.processed.append(email)
        # In a full implementation, we'd actually perform the action here
    
    def _get_current_observation(self) -> EmailObservation:
        """
        Build the observation object for the current state.
        
        This is what the AI "sees" at each step.
        IMPORTANT: We hide correct_category and urgency from the AI!
        """
        if self.current_index >= len(self.inbox):
            # No more emails, return empty observation
            return EmailObservation(
                current_email=EmailView(id=-1, subject="", body="", sender=""),
                remaining_count=0,
                step_number=self.step_count,
                last_action_result="All emails processed"
            )
        
        current = self.inbox[self.current_index]
        remaining = len(self.inbox) - self.current_index
        
        # Create a VIEW for the AI (hides correct_category and urgency)
        email_view = EmailView(
            id=current.id,
            subject=current.subject,
            body=current.body,
            sender=current.sender
        )
        
        return EmailObservation(
            current_email=email_view,
            remaining_count=remaining,
            step_number=self.step_count,
            last_action_result=None
        )
    
    def state(self) -> dict:
        """
        Return current internal state.
        
        Used for debugging and monitoring.
        """
        return {
            "task_id": self.task_id,
            "inbox_size": len(self.inbox),
            "processed_count": len(self.processed),
            "current_index": self.current_index,
            "step_count": self.step_count,
            "done": self.done,
            "current_email": self.inbox[self.current_index].id if self.current_index < len(self.inbox) else None
        }
    
    def close(self):
        """
        Clean up resources.
        
        Called when the environment is no longer needed.
        """
        # Nothing to clean up for this simple environment
        pass