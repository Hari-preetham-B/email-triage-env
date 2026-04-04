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
        fake_urgent_map = {email.id: email.is_fake_urgent for email in inbox}
        time_sensitive_map = {email.id: email.time_sensitive for email in inbox}
        urgency_map = {email.id: email.urgency for email in inbox}
        
        # Part 1: Accuracy (50% of score)
        correct_count = 0
        for action in actions:
            if action.email_id in correct_map:
                expected = correct_map[action.email_id]
                actual = action.action.value
                if actual == expected:
                    correct_count += 1
        accuracy_score = correct_count / len(inbox) if len(inbox) > 0 else 0.0
        accuracy_contribution = accuracy_score * 0.5
        
        # Part 2: Fake Urgency Detection (20% of score)
        fake_urgent_detected = 0
        fake_urgent_total = sum(1 for email in inbox if email.is_fake_urgent)
        
        for action in actions:
            if action.email_id in fake_urgent_map and fake_urgent_map[action.email_id]:
                if action.action.value == "spam":
                    fake_urgent_detected += 1
        
        if fake_urgent_total > 0:
            fake_urgency_score = fake_urgent_detected / fake_urgent_total
        else:
            fake_urgency_score = 1.0
        fake_urgency_contribution = fake_urgency_score * 0.2
        
        # Part 3: Time Sensitivity (15% of score)
        # Check if urgent/time-sensitive emails were processed before non-urgent
        urgent_ids = [email.id for email in inbox if email.urgency == 3 or email.time_sensitive]
        non_urgent_ids = [email.id for email in inbox if email.urgency == 1 and not email.time_sensitive]
        
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
        priority_contribution = priority_score * 0.15
        
        # Part 4: Efficiency (15% of score)
        optimal_steps = len(inbox)
        actual_steps = len(actions)
        if actual_steps <= optimal_steps:
            efficiency_score = 1.0
        else:
            extra_ratio = (actual_steps - optimal_steps) / optimal_steps
            efficiency_score = max(0.0, 1.0 - extra_ratio)
        efficiency_contribution = efficiency_score * 0.15
        
        # Final score
        final_score = accuracy_contribution + fake_urgency_contribution + priority_contribution + efficiency_contribution
        
        # Boss feedback based on performance
        boss_feedback = ""
        if final_score >= 0.9:
            boss_feedback = "🌟 Outstanding! You perfectly handled the inbox, caught all fake urgency emails, and prioritized correctly!"
        elif final_score >= 0.75:
            boss_feedback = "👍 Great job! Good detection of fake urgency, but some urgent emails were delayed."
        elif final_score >= 0.6:
            boss_feedback = "⚠️ Acceptable, but you missed several fake urgency emails. Need to be more skeptical of 'URGENT' claims."
        else:
            boss_feedback = "🔴 Needs improvement. You fell for fake urgency scams and missed critical real emergencies."
        
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