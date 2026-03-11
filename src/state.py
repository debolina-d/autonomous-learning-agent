"""Learning State - TypedDict schema for workflow state management"""
from typing import TypedDict, List

class LearningState(TypedDict):
    """State schema for the autonomous learning workflow"""
    topic: str                    # Current learning topic
    objectives: str               # Learning objectives (comma-separated)
    gathered_context: str         # Formatted study material
    relevance_score: int          # Context quality score (1-5)
    questions: List[str]          # Generated MCQs or Feynman content
    learner_answers: str          # User's answers (e.g., "1.A, 2.B, 3.C")
    understanding_score: int      # Assessment score (0-100)
    search_retry_count: int       # Number of context gathering retries  