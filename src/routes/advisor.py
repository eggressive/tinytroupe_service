"""
Advisor routes for TinyTroupe Service
"""
from flask import Blueprint, jsonify, request
from src.config import get_config
from src.models import Persona
from src.extensions import db

advisor_bp = Blueprint('advisor', __name__)

@advisor_bp.route('', methods=['GET'])
def get_advisors():
    """Get all available advisors"""
    advisors = Persona.query.all()
    
    # If no advisors exist in the database, initialize with defaults
    if not advisors:
        config = get_config()
        for advisor_data in config.DEFAULT_ADVISORS:
            advisor = Persona(
                id=advisor_data['id'],
                name=advisor_data['name'],
                description=advisor_data['description'],
                personality={
                    'traits': ['analytical', 'thoughtful', 'experienced'],
                    'communication_style': 'clear and methodical'
                },
                expertise=advisor_data['expertise']
            )
            db.session.add(advisor)
        
        db.session.commit()
        advisors = Persona.query.all()
    
    return jsonify([advisor.to_dict() for advisor in advisors])

@advisor_bp.route('/<advisor_id>', methods=['GET'])
def get_advisor(advisor_id):
    """Get a specific advisor"""
    advisor = Persona.query.get_or_404(advisor_id)
    return jsonify(advisor.to_dict())
