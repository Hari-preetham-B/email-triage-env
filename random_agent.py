"""
random_agent.py - Random decision maker for baseline comparison
Makes random choices without using any AI API
"""

import random
from models import EmailAction, ActionType
from typing import List


class RandomAgent:
    """
    Random agent that makes random decisions for baseline comparison.
    This shows how much better the AI agent performs.
    """
    
    def __init__(self):
        self.possible_actions = ["urgent", "normal", "spam"]
    
    def get_action(self, email) -> str:
        """
        Randomly choose an action without looking at email content.
        
        Returns:
            "urgent", "normal", or "spam" with equal probability (33.3% each)
        """
        return random.choice(self.possible_actions)
    
    def get_action_with_info(self, email) -> tuple:
        """
        Returns action and a simple message for display.
        """
        action = self.get_action(email)
        return action, f"Random choice: {action}"