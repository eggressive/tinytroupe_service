"""
Conversation management service
"""
import logging
from typing import List, Dict, Any
from src.main import db
from src.models import Conversation, Message, Persona, PersonaState
from src.services.tinytroupe_service import TinyTroupeService

class ConversationService:
    """Service for managing conversations with TinyTroupe advisors"""
    
    def __init__(self):
        """Initialize the conversation service"""
        self.logger = logging.getLogger(__name__)
        self.tinytroupe_service = TinyTroupeService()
        
    def initialize_personas(self, conversation_id: str) -> None:
        """Initialize advisor personas for a conversation
        
        Args:
            conversation_id: ID of the conversation to initialize personas for
        """
        self.logger.info(f"Initializing personas for conversation: {conversation_id}")
        
        # Get all advisors
        advisors = Persona.query.all()
        
        # If no advisors exist, we can't initialize personas
        if not advisors:
            self.logger.warning("No advisors found in database")
            return
        
        # Initialize the TinyTroupe service with advisor configurations
        advisor_configs = [advisor.to_dict() for advisor in advisors]
        self.tinytroupe_service.initialize_advisors(advisor_configs)
        
        # Create initial persona states for each advisor
        for advisor in advisors:
            persona_state = PersonaState(
                persona_id=advisor.id,
                conversation_id=conversation_id,
                memory_state={"context": [], "recent_messages": []}
            )
            db.session.add(persona_state)
        
        db.session.commit()
        self.logger.info(f"Initialized {len(advisors)} personas for conversation: {conversation_id}")
    
    def generate_responses(self, conversation_id: str, user_message: str) -> List[Dict[str, Any]]:
        """Generate responses from all advisors for a user message
        
        Args:
            conversation_id: ID of the conversation
            user_message: User message to respond to
            
        Returns:
            List of advisor responses with metadata
        """
        self.logger.info(f"Generating responses for conversation: {conversation_id}")
        
        # Get conversation history
        messages = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.timestamp).all()
        conversation_history = [message.to_dict() for message in messages]
        
        # Get all advisors for this conversation
        persona_states = PersonaState.query.filter_by(conversation_id=conversation_id).all()
        if not persona_states:
            self.logger.warning(f"No persona states found for conversation: {conversation_id}")
            return []
        
        advisor_responses = []
        for persona_state in persona_states:
            advisor_id = persona_state.persona_id
            
            try:
                # Get response from TinyTroupe service
                response_content = self.tinytroupe_service.get_response(
                    advisor_id, 
                    user_message, 
                    conversation_history
                )
                
                # Create message in database
                advisor_message = Message(
                    conversation_id=conversation_id,
                    role='advisor',
                    advisor_id=advisor_id,
                    content=response_content
                )
                db.session.add(advisor_message)
                
                # Update persona state with new message
                memory_state = persona_state.memory_state
                if 'recent_messages' not in memory_state:
                    memory_state['recent_messages'] = []
                
                memory_state['recent_messages'].append({
                    'role': 'user',
                    'content': user_message
                })
                memory_state['recent_messages'].append({
                    'role': 'advisor',
                    'content': response_content
                })
                
                # Keep only the last 10 messages in memory
                if len(memory_state['recent_messages']) > 20:
                    memory_state['recent_messages'] = memory_state['recent_messages'][-20:]
                
                persona_state.memory_state = memory_state
                
                # Add response to result list
                advisor = Persona.query.get(advisor_id)
                advisor_responses.append({
                    'id': advisor_message.id,
                    'advisor_id': advisor_id,
                    'advisor_name': advisor.name if advisor else 'Unknown',
                    'content': response_content,
                    'timestamp': advisor_message.timestamp.isoformat()
                })
                
            except Exception as e:
                self.logger.error(f"Error generating response from advisor {advisor_id}: {str(e)}")
        
        db.session.commit()
        self.logger.info(f"Generated {len(advisor_responses)} responses for conversation: {conversation_id}")
        
        return advisor_responses
