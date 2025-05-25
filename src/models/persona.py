"""
Database models for personas
"""
import uuid
from src.main import db

class Persona(db.Model):
    """Persona model for storing advisor personalities"""
    __tablename__ = 'personas'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    personality = db.Column(db.JSON, nullable=False)
    expertise = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Relationships
    states = db.relationship('PersonaState', backref='persona', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Persona {self.id}: {self.name}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'personality': self.personality,
            'expertise': self.expertise,
            'created_at': self.created_at.isoformat()
        }
