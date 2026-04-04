"""
environment.py - The main Email Triage Environment

This is the brain of your environment. It handles:
- reset(): Start a new email inbox with tasks
- step(): Process AI actions and return rewards
- state(): Return current environment state
"""

from typing import Optional, Tuple, List, Dict
from models import (
    Email, EmailAction, EmailObservation, EmailReward, ActionType, EmailView, SenderProfile
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
        
        # ADD THESE TWO LINES FOR MULTI-USER SIMULATION
        self.sender_profiles: dict = {}
        self._init_sender_profiles()
        # Populate inbox based on selected task
        self._setup_task()
    
    def _init_sender_profiles(self):
        """Initialize sender personalities for multi-user simulation"""
        self.sender_profiles = {
            "alert@company.com": SenderProfile(
                name="System Alerts",
                email="alert@company.com",
                personality="crisis-mode",
                trust_level=9,
                previous_topics=["server", "database", "system"],
                previous_urgency=[3, 3]
            ),
            "manager@company.com": SenderProfile(
                name="Manager",
                email="manager@company.com",
                personality="casual",
                trust_level=8,
                previous_topics=["meetings", "team", "updates"],
                previous_urgency=[1, 2]
            ),
            "lottery@spam.com": SenderProfile(
                name="Lottery Scam",
                email="lottery@spam.com",
                personality="spammy",
                trust_level=1,
                previous_topics=["prize", "winner", "money"],
                previous_urgency=[1]
            ),
            "client@bigcompany.com": SenderProfile(
                name="Big Company Client",
                email="client@bigcompany.com",
                personality="formal",
                trust_level=7,
                previous_topics=["contract", "review", "meeting"],
                previous_urgency=[2, 3]
            ),
            "hr@company.com": SenderProfile(
                name="HR Department",
                email="hr@company.com",
                personality="formal",
                trust_level=9,
                previous_topics=["payroll", "benefits", "policy"],
                previous_urgency=[1]
            ),
            "security@company.com": SenderProfile(
                name="Security Team",
                email="security@company.com",
                personality="crisis-mode",
                trust_level=10,
                previous_topics=["breach", "alert", "unauthorized"],
                previous_urgency=[3, 3]
            ),
            "support@company.com": SenderProfile(
                name="Customer Support",
                email="support@company.com",
                personality="urgent-prone",
                trust_level=8,
                previous_topics=["complaint", "escalation", "client"],
                previous_urgency=[2, 3]
            ),
            "scam@fraud.com": SenderProfile(
                name="Scam Alert",
                email="scam@fraud.com",
                personality="spammy",
                trust_level=1,
                previous_topics=["lottery", "prize", "winner"],
                previous_urgency=[1]
            ),
            "tech-alerts@company.com": SenderProfile(
                name="Technical Alerts",
                email="tech-alerts@company.com",
                personality="crisis-mode",
                trust_level=9,
                previous_topics=["server", "database", "migration"],
                previous_urgency=[3]
            ),
        }
    
    def get_sender_history(self, sender_email: str, limit: int = 3) -> list:
        """Get recent emails from a specific sender"""
        history = []
        for email in reversed(self.processed):
            if email.sender == sender_email and len(history) < limit:
                history.append({
                    'subject': email.subject,
                    'category': email.correct_category,
                    'urgency': email.urgency
                })
        return history

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
        EASY TASK: 10 emails with clear signals
        """
        self.inbox = [
            Email(id=1, subject="URGENT: Production Server Down", 
                body="The main server is not responding. Customer facing issues!",
                sender="alert@company.com", correct_category="urgent", urgency=3),
            Email(id=2, subject="Weekly Team Meeting", 
                body="Reminder: Team sync at 2 PM tomorrow",
                sender="manager@company.com", correct_category="normal", urgency=1),
            Email(id=3, subject="YOU WON $1,000,000!!!", 
                body="Click here to claim your prize!",
                sender="lottery@spam.com", correct_category="spam", urgency=1),
            Email(id=4, subject="Security Alert: Password Change Required", 
                body="Please update your password for security purposes",
                sender="security@company.com", correct_category="urgent", urgency=2),
            Email(id=5, subject="Lunch Menu This Week", 
                body="Here's the cafeteria menu for the week",
                sender="facilities@company.com", correct_category="normal", urgency=1),
            Email(id=6, subject="Your Amazon Order #ORD-12345", 
                body="Your package has been delivered",
                sender="no-reply@amazon.com", correct_category="normal", urgency=1),
            Email(id=7, subject="URGENT: Your subscription expires today", 
                body="Renew now to avoid service interruption",
                sender="billing@fake-service.com", correct_category="spam", urgency=1),
            Email(id=8, subject="Q3 Financial Report Ready", 
                body="The quarterly financial report is available for review",
                sender="finance@company.com", correct_category="normal", urgency=2),
            Email(id=9, subject="CRITICAL: Data Backup Failed", 
                body="The automated backup failed last night. Manual intervention needed.",
                sender="it@company.com", correct_category="urgent", urgency=3),
            Email(id=10, subject="Free Gift Card Inside!", 
                body="Claim your $500 gift card now! Limited time offer.",
                sender="promo@spam-central.com", correct_category="spam", urgency=1),
                    # Security alert examples for learning
            Email(id=11, subject="Security Alert: Multiple Failed Logins", 
                body="We detected 5 failed login attempts to your account from an unknown IP. Please review your recent activity.",
                sender="security@company.com", correct_category="urgent", urgency=3),
            Email(id=12, subject="Password Reset Request", 
                body="A password reset was requested for your account. If this wasn't you, please contact IT immediately.",
                sender="it-security@company.com", correct_category="urgent", urgency=3),
        ]
    
    def _setup_medium_task(self):
        """
        MEDIUM TASK: 15 emails with subtle differences
        """
        self.inbox = [
            Email(id=1, subject="RE: Project Deadline", 
                body="Can we extend by one day? Almost done.",
                sender="junior@company.com", correct_category="normal", urgency=1),
            Email(id=2, subject="IMPORTANT: Client Review", 
                body="The client meeting is at 3 PM today. Please attend.",
                sender="client@bigcompany.com", correct_category="urgent", urgency=3),
            Email(id=3, subject="Free Gift Card Inside", 
                body="You've been selected for a free $50 gift card!",
                sender="promo@retail.com", correct_category="spam", urgency=1),
            Email(id=4, subject="Your Payroll Update", 
                body="Please verify your information for next month's payroll",
                sender="hr@company.com", correct_category="urgent", urgency=2),
            Email(id=5, subject="Newsletter: Weekly Updates", 
                body="Here's what happened this week...",
                sender="updates@newsletter.com", correct_category="normal", urgency=1),
            Email(id=6, subject="Team Building Event", 
                body="Sign up for the team building activity next Friday",
                sender="events@company.com", correct_category="normal", urgency=1),
            Email(id=7, subject="URGENT: Invoice Overdue", 
                body="Your invoice #INV-789 is past due. Immediate payment required.",
                sender="billing@fake-collector.com", correct_category="spam", urgency=1),
            Email(id=8, subject="Server Maintenance Scheduled", 
                body="Planned maintenance this Sunday from 2-4 AM",
                sender="sysadmin@company.com", correct_category="normal", urgency=1),
            Email(id=9, subject="Client Complaint Escalated", 
                body="VIP client is unhappy with response time. Please call immediately.",
                sender="support@company.com", correct_category="urgent", urgency=3),
            Email(id=10, subject="Your Account Will Be Closed", 
                body="Final warning: Your account will be permanently closed.",
                sender="security@fake-alert.com", correct_category="spam", urgency=1),
            Email(id=11, subject="Code Review Request", 
                body="Please review my pull request for the auth module",
                sender="developer@company.com", correct_category="normal", urgency=1),
            Email(id=12, subject="Emergency: Database Connection Lost", 
                body="The database connection pool is exhausted. Immediate action needed.",
                sender="dba@company.com", correct_category="urgent", urgency=3),
            Email(id=13, subject="You've Won a Free iPhone!", 
                body="Click here to claim your prize!",
                sender="winner@spam.com", correct_category="spam", urgency=1),
            Email(id=14, subject="Budget Review Meeting", 
                body="Please review the attached budget before tomorrow's meeting",
                sender="finance@company.com", correct_category="normal", urgency=2),
            Email(id=15, subject="SECURITY BREACH: Action Required", 
                body="Unauthorized access detected. Please reset your password immediately.",
                sender="it-security@company.com", correct_category="urgent", urgency=3),
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

            # Additional emails from SAME senders to show memory accumulation
    
        # Email 21: Second email from client@bigcompany.com
        self.inbox.append(Email(
            id=21, subject="Follow-up: Contract Renewal", 
            body="Following up on our previous discussion about the contract renewal. Need your feedback by Friday.",
            sender="client@bigcompany.com", correct_category="urgent", urgency=2,
            time_sensitive=True, expires_in=5
        ))
        
        # Email 22: Second email from security@company.com
        self.inbox.append(Email(
            id=22, subject="Security Update: Patch Required", 
            body="Please update your system with the latest security patch. This is a routine update.",
            sender="security@company.com", correct_category="normal", urgency=1
        ))
        
        # Email 23: Second email from hr@company.com
        self.inbox.append(Email(
            id=23, subject="Reminder: Benefits Deadline", 
            body="Just a reminder that benefits enrollment ends next week. Don't miss the deadline.",
            sender="hr@company.com", correct_category="normal", urgency=2
        ))
        
        # Email 24: Second fake urgency from scam@fraud.com
        self.inbox.append(Email(
            id=24, subject="FINAL NOTICE: Your account suspended", 
            body="This is your FINAL NOTICE. Your account will be permanently suspended.",
            sender="scam@fraud.com", correct_category="spam", urgency=1,
            is_fake_urgent=True, fake_reason="Fake account suspension scam"
        ))
        
        # Email 25: Second email from tech-alerts@company.com
        self.inbox.append(Email(
            id=25, subject="System Maintenance Scheduled", 
            body="Scheduled maintenance for Sunday at 2 AM. Expected downtime: 2 hours.",
            sender="tech-alerts@company.com", correct_category="normal", urgency=1
        ))
        
        # Email 26: Second email from ceo@company.com
        self.inbox.append(Email(
            id=26, subject="Q2 Strategy Meeting", 
            body="Please prepare your Q2 strategy presentation for next week's board meeting.",
            sender="ceo@company.com", correct_category="normal", urgency=2
        ))
        
        # Email 27: Third email from client@bigcompany.com (shows accumulated memory)
        self.inbox.append(Email(
            id=27, subject="URGENT: Contract Signature Needed", 
            body="The client needs the signed contract by end of day today. Please prioritize.",
            sender="client@bigcompany.com", correct_category="urgent", urgency=3,
            time_sensitive=True, expires_in=1
        ))
        
        # Email 28: Second email from support@company.com
        self.inbox.append(Email(
            id=28, subject="Client Satisfaction Survey Results", 
            body="Our quarterly client satisfaction results are in. Review attached report.",
            sender="support@company.com", correct_category="normal", urgency=1
        ))
        
        # Email 29: Third email from scam@fraud.com
        self.inbox.append(Email(
            id=29, subject="Congratulations! You've been selected", 
            body="You've been selected for our exclusive prize. Click here to claim.",
            sender="scam@fraud.com", correct_category="spam", urgency=1,
            is_fake_urgent=True, fake_reason="Fake prize scam"
        ))
        
        # Email 30: Third email from security@company.com
        self.inbox.append(Email(
            id=30, subject="Security Breach Attempt Detected", 
            body="We detected multiple failed login attempts from an unknown IP. No action needed.",
            sender="security@company.com", correct_category="normal", urgency=2
        ))

                # PENDING EMAILS - These will arrive dynamically while AI processes
        self.pending_emails = [
            Email(id=31, subject="🔥 URGENT: Customer Outage Reported", 
                  body="Multiple customers reporting service interruption. Immediate investigation required.",
                  sender="support@company.com", correct_category="urgent", urgency=3,
                  time_sensitive=True, expires_in=2),
            Email(id=32, subject="Your Amazon Prime Membership", 
                  body="Your membership will renew tomorrow. Click here to cancel.",
                  sender="prime@amazon-scam.com", correct_category="spam", urgency=1,
                  is_fake_urgent=True, fake_reason="Fake Amazon subscription scam"),
            Email(id=33, subject="Weekly Sales Report", 
                  body="Q2 sales figures are attached for review.",
                  sender="sales@company.com", correct_category="normal", urgency=1),
            Email(id=34, subject="⚠️ CRITICAL: SSL Certificate Expiring", 
                  body="Your SSL certificate expires in 24 hours. Website will be inaccessible.",
                  sender="security@company.com", correct_category="urgent", urgency=3,
                  time_sensitive=True, expires_in=2),
            Email(id=35, subject="Congratulations! You're a Winner!", 
                  body="You've been selected for our grand prize. Claim now!",
                  sender="prize@winner-scam.com", correct_category="spam", urgency=1,
                  is_fake_urgent=True, fake_reason="Fake prize scam"),
            Email(id=36, subject="Team Building Feedback", 
                  body="Please fill out the anonymous feedback form for last week's event.",
                  sender="hr@company.com", correct_category="normal", urgency=1),
            Email(id=37, subject="🔴 EMERGENCY: Data Center Fire Alarm", 
                  body="Fire alarm triggered at main data center. Evacuation in progress.",
                  sender="facilities@company.com", correct_category="urgent", urgency=3,
                  time_sensitive=True, expires_in=1),
            Email(id=38, subject="Your Netflix Account Suspended", 
                  body="Payment failed. Update your billing info now!",
                  sender="netflix@fake-billing.com", correct_category="spam", urgency=1,
                  is_fake_urgent=True, fake_reason="Fake Netflix suspension scam"),
            Email(id=39, subject="Product Launch Update", 
                  body="Marketing materials for next week's launch are ready.",
                  sender="marketing@company.com", correct_category="normal", urgency=2),
            Email(id=40, subject="URGENT: Wire Transfer Required", 
                  body="We need to authorize a wire transfer for the vendor payment today.",
                  sender="cfo@company.com", correct_category="urgent", urgency=2,
                  time_sensitive=True, expires_in=4),
        ]
    
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
            if self.step_count % 3 == 0 and self.pending_emails:
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
                # Bonus for security-related emails
                if "security" in email.sender.lower() or any(kw in email.subject.lower() for kw in ["security", "alert", "breach", "password"]):
                    reward += 0.2
                    breakdown["message"] = f"✓ Correctly marked urgent! (+0.5) + Security bonus (+0.2)"
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