"""
tasks.py - Task graders for Email Triage Environment

Each task has a grader that returns a score from 0.0 to 1.0.
The AI is evaluated on how well it performs each task.
"""

from typing import List, Dict
from models import Email, EmailAction, ActionType


class TaskGrader:
    """
    Base class for all task graders.
    Each grader evaluates AI performance and returns a score.
    """
    
    def grade(self, actions: List[EmailAction], inbox: List[Email]) -> float:
        """
        Grade AI performance on a task.
        
        Args:
            actions: List of actions the AI took (in order)
            inbox: Original inbox emails
            
        Returns:
            Score from 0.0 to 1.0
        """
        raise NotImplementedError


class EasyTaskGrader(TaskGrader):
    """
    Grader for Easy Task (3 emails).
    
    Scoring:
    - 100% = All 3 emails classified correctly
    - Partial credit for correct classifications
    """
    
    def grade(self, actions: List[EmailAction], inbox: List[Email]) -> float:
        """
        Grade easy task performance.
        
        Returns:
            Score 0.0 - 1.0
        """
        if len(actions) == 0:
            return 0.0
        
        correct_count = 0
        total_emails = len(inbox)
        
        # Create a map of email_id to correct category
        correct_map = {email.id: email.correct_category for email in inbox}
        
        # Check each action
        for action in actions:
            if action.email_id in correct_map:
                expected = correct_map[action.email_id]
                actual = action.action.value
                
                if actual == expected:
                    correct_count += 1
        
        # Score = number correct / total emails
        score = correct_count / total_emails
        
        return min(1.0, max(0.0, score))


class MediumTaskGrader(TaskGrader):
    """
    Grader for Medium Task (5 emails with subtle differences).
    
    Scoring:
    - Each correct classification: +0.2 points
    - Wrong classification: 0 points
    - Total = sum / 5
    """
    
    def grade(self, actions: List[EmailAction], inbox: List[Email]) -> float:
        """
        Grade medium task performance.
        
        Returns:
            Score 0.0 - 1.0
        """
        if len(actions) == 0:
            return 0.0
        
        correct_map = {email.id: email.correct_category for email in inbox}
        
        correct_count = 0
        for action in actions:
            if action.email_id in correct_map:
                expected = correct_map[action.email_id]
                actual = action.action.value
                
                if actual == expected:
                    correct_count += 1
        
        # Weight each email equally
        score = correct_count / len(inbox)
        
        # Bonus for handling urgent emails correctly (if applicable)
        urgent_emails = [e for e in inbox if e.correct_category == "urgent"]
        for email in urgent_emails:
            for action in actions:
                if action.email_id == email.id and action.action.value == "urgent":
                    # Bonus: +0.1 for correctly handling urgent
                    score = min(1.0, score + 0.1 / len(inbox))
                    break
        
        return min(1.0, max(0.0, score))


class HardTaskGrader(TaskGrader):
    """
    Enhanced Grader for Sophisticated Hard Task (20+ emails with fake urgency).
    
    Scoring considers:
    - Accuracy (50%) - Correct classification
    - Fake Urgency Detection (20%) - Identifying spoofed/manipulative emails
    - Time Sensitivity (15%) - Processing urgent/time-sensitive emails first
    - Efficiency (15%) - Steps taken vs optimal
    """
    
    def grade(self, actions: List[EmailAction], inbox: List[Email]) -> float:
        if len(actions) == 0:
            return 0.0
        
        correct_map = {email.id: email.correct_category for email in inbox}
        
        # Part 1: Accuracy (70%)
        correct_count = 0
        for action in actions:
            if action.email_id in correct_map:
                if action.action.value == correct_map[action.email_id]:
                    correct_count += 1
        accuracy_score = correct_count / len(inbox) if len(inbox) > 0 else 0.0
        accuracy_contribution = accuracy_score * 0.7
        
        # Part 2: Efficiency (20%)
        optimal_steps = len(inbox)
        actual_steps = len(actions)
        if actual_steps <= optimal_steps:
            efficiency_score = 1.0
        else:
            extra_ratio = (actual_steps - optimal_steps) / optimal_steps
            efficiency_score = max(0.0, 1.0 - extra_ratio)
        efficiency_contribution = efficiency_score * 0.2
        
        # Part 3: Priority (10%)
        urgent_ids = [email.id for email in inbox if email.correct_category == "urgent"]
        non_urgent_ids = [email.id for email in inbox if email.correct_category != "urgent"]
        
        urgent_positions = [i for i, a in enumerate(actions) if a.email_id in urgent_ids]
        non_urgent_positions = [i for i, a in enumerate(actions) if a.email_id in non_urgent_ids]
        
        if urgent_positions and non_urgent_positions:
            if max(urgent_positions) < min(non_urgent_positions):
                priority_score = 1.0
            else:
                urgent_before = sum(1 for u in urgent_positions if non_urgent_positions and u < min(non_urgent_positions))
                priority_score = urgent_before / len(urgent_positions) if urgent_positions else 1.0
        else:
            priority_score = 1.0
        priority_contribution = priority_score * 0.1
        
        # Final score
        final_score = accuracy_contribution + efficiency_contribution + priority_contribution
        
        # Boss feedback
        if final_score >= 0.9:
            boss_feedback = "🌟 Outstanding! Perfect handling of the inbox!"
        elif final_score >= 0.75:
            boss_feedback = "👍 Great job! Good detection and prioritization."
        elif final_score >= 0.6:
            boss_feedback = "⚠️ Acceptable, but could improve priority ordering."
        else:
            boss_feedback = "🔴 Needs improvement on prioritization."
        
        self.boss_feedback = boss_feedback
        
        return min(1.0, max(0.0, final_score))


# Dictionary to get grader by task ID
GRADERS = {
    "easy_classification": EasyTaskGrader(),
    "medium_prioritization": MediumTaskGrader(),
    "hard_evolving": HardTaskGrader(),
}


def get_grader(task_id: str) -> TaskGrader:
    """
    Get the grader for a specific task.
    
    Args:
        task_id: The task identifier
        
    Returns:
        TaskGrader instance
    """
    if task_id not in GRADERS:
        raise ValueError(f"Unknown task: {task_id}. Available: {list(GRADERS.keys())}")
    return GRADERS[task_id]


def grade_task(task_id: str, actions: List[EmailAction], inbox: List[Email]) -> float:
    """Grade AI performance on a task."""
    grader = get_grader(task_id)
    score = grader.grade(actions, inbox)
    return score


def grade_task_with_feedback(task_id: str, actions: List[EmailAction], inbox: List[Email]) -> tuple:
    """Grade AI performance and return (score, boss_feedback) for hard task."""
    grader = get_grader(task_id)
    score = grader.grade(actions, inbox)
    
    boss_feedback = None
    if task_id == "hard_evolving" and hasattr(grader, 'boss_feedback'):
        boss_feedback = grader.boss_feedback
    
    return score, boss_feedback