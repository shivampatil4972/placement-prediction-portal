"""
Models package initialization
"""

from models.database import init_db, get_db, execute_query
from models.user import User
from models.student import StudentProfile
from models.prediction import Prediction
from models.resume import Resume, SkillGap, Simulation

__all__ = [
    'init_db',
    'get_db',
    'execute_query',
    'User',
    'StudentProfile',
    'Prediction',
    'Resume',
    'SkillGap',
    'Simulation'
]
