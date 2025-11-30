"""Agent Orchestrator - Central coordinator for all agent operations."""

from typing import Optional
from datetime import datetime

from jarvis.llm_engine import LLMEngine, LLMConfig
from jarvis.conversation_buffer import ConversationBuffer
from jarvis.preference_manager import PreferenceManager
from jarvis.models import Message


class AgentOrchestrator:
    """Central coordinator for all agent operations."""
    
    def __init__(self, llm_config: Optional[LLMConfig] = None):
        """Initialize Agent Orchestrator.
        
        Args:
            llm_config: LLM configuration. Uses defaults if not provided.
        """
        self.llm_engine = LLMEngine(llm_config)
        self.conversation_buffer = ConversationBuffer(max_turns=10)
        self.preference_manager = PreferenceManager()
        self.personality = self.preference_manager.get_personality_config()
    
    def process_input(self, user_input: str) -> str:
        """Process user input and generate response.
        
        Args:
            user_input: User's input text
            
        Returns:
            Assistant's response
        """
        # Get conversation context
        context = self.conversation_buffer.get_context_for_llm()
        
        # Generate response using LLM
        try:
            response = self.llm_engine.generate(
                prompt=user_input,
                context=context,
                personality=self.personality
            )
        except Exception as e:
            response = f"I encountered an error: {str(e)}"
        
        # Add turn to conversation buffer
        user_message = Message(role="user", content=user_input)
        assistant_message = Message(role="assistant", content=response)
        self.conversation_buffer.add_turn(user_message, assistant_message)
        
        return response
    
    def export_conversation(self) -> str:
        """Export conversation history to JSON.
        
        Returns:
            JSON string of conversation history
        """
        return self.conversation_buffer.export_to_json()
    
    def clear_conversation(self) -> str:
        """Clear conversation history.
        
        Returns:
            Confirmation message
        """
        self.conversation_buffer.clear()
        return "Conversation history cleared."
    
    def update_personality(self, **kwargs) -> None:
        """Update personality configuration.
        
        Args:
            **kwargs: Personality attributes to update (tone, verbosity, etc.)
        """
        # Load current personality
        personality = self.preference_manager.get_personality_config()
        
        # Update attributes
        for key, value in kwargs.items():
            if hasattr(personality, key):
                setattr(personality, key, value)
        
        # Save updated personality
        self.preference_manager.set_personality_config(personality)
        self.personality = personality
