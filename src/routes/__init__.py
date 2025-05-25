"""
Routes initialization
"""
from src.routes.conversation import conversation_bp
from src.routes.advisor import advisor_bp
from src.routes.financial import financial_bp

__all__ = ['conversation_bp', 'advisor_bp', 'financial_bp']
