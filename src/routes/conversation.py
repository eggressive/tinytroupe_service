"""
Conversation routes for TinyTroupe Service
"""
from flask import Blueprint, request, jsonify, current_app
from src.extensions import db
from src.models import Conversation, Message
from src.services.conversation_service import ConversationService

conversation_bp = Blueprint('conversation', __name__)
conversation_service = ConversationService()

@conversation_bp.route('', methods=['GET'])
def get_conversations():
    """Get all conversations"""
    # In a real app, filter by authenticated user
    user_id = request.args.get('user_id', 'default_user')
    conversations = Conversation.query.filter_by(user_id=user_id).order_by(Conversation.updated_at.desc()).all()
    return jsonify([conversation.to_dict() for conversation in conversations])

@conversation_bp.route('', methods=['POST'])
def create_conversation():
    """Create a new conversation"""
    data = request.json
    user_id = data.get('user_id', 'default_user')
    title = data.get('title', 'New Conversation')
    
    conversation = Conversation(user_id=user_id, title=title)
    db.session.add(conversation)
    db.session.commit()
    
    # Initialize advisor personas for this conversation
    conversation_service.initialize_personas(conversation.id)
    
    return jsonify(conversation.to_dict()), 201

@conversation_bp.route('/<conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    """Get a specific conversation"""
    conversation = Conversation.query.get_or_404(conversation_id)
    return jsonify(conversation.to_dict())

@conversation_bp.route('/<conversation_id>/messages', methods=['GET'])
def get_messages(conversation_id):
    """Get all messages in a conversation"""
    messages = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.timestamp).all()
    return jsonify([message.to_dict() for message in messages])

@conversation_bp.route('/<conversation_id>/messages', methods=['POST'])
def add_message(conversation_id):
    """Add a message to a conversation"""
    data = request.json
    content = data.get('content')
    
    if not content:
        return jsonify({'error': 'Content is required'}), 400
    
    # Get the conversation
    conversation = Conversation.query.get_or_404(conversation_id)
    
    # Add user message
    user_message = Message(
        conversation_id=conversation_id,
        role='user',
        content=content
    )
    db.session.add(user_message)
    
    # Update conversation timestamp
    conversation.updated_at = db.func.now()
    db.session.commit()
    
    # Generate advisor responses
    advisor_responses = conversation_service.generate_responses(conversation_id, content)
    
    return jsonify({
        'user_message': user_message.to_dict(),
        'advisor_responses': advisor_responses
    }), 201

@conversation_bp.route('/<conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id):
    """Delete a conversation"""
    conversation = Conversation.query.get_or_404(conversation_id)
    db.session.delete(conversation)
    db.session.commit()
    return '', 204
