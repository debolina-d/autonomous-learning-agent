from typing import TypedDict, List

class LearningState(TypedDict):
    topic: str
    objectives: str
    gathered_context: str
    relevance_score: int
    questions: List[str]     
    learner_answers: str     
    understanding_score: int 
    search_retry_count: int  