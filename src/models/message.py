"""
Database models for messages
"""
from datetime import datetime
import uuid
from src.extensions import db

class Message(db.Model):
    """Message model for storing conversation messages"""
    __tablename__ = 'messages'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = db.Column(db.String(36), db.ForeignKey('conversations.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'user' or 'advisor'
    advisor_id = db.Column(db.String(36), nullable=True)  # NULL for user messages
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Message {self.id}: {self.role}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'role': self.role,
            'advisor_id': self.advisor_id,
            'content': self.content,
            'timestamp': self.timestamp.isoformat()
        }
