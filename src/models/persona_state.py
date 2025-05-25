"""
Database models for persona states
"""
import uuid
from datetime import datetime
from src.extensions import db

class PersonaState(db.Model):
    """PersonaState model for storing persona memory states in conversations"""
    __tablename__ = 'persona_states'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    persona_id = db.Column(db.String(36), db.ForeignKey('personas.id'), nullable=False)
    conversation_id = db.Column(db.String(36), db.ForeignKey('conversations.id'), nullable=False)
    memory_state = db.Column(db.JSON, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<PersonaState {self.id}: {self.persona_id} in {self.conversation_id}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'persona_id': self.persona_id,
            'conversation_id': self.conversation_id,
            'memory_state': self.memory_state,
            'updated_at': self.updated_at.isoformat()
        }
