"""Conversation buffer for maintaining context."""

import json
from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4

from jarvis.models import ConversationTurn, Message


class ConversationBuffer:
    """Manages conversation history with automatic turn eviction."""
    
    def __init__(self, max_turns: int = 10):
        """Initialize conversation buffer.
        
        Args:
            max_turns: Maximum number of turns to maintain in buffer
        """
        self.max_turns = max_turns
        self.turns: List[ConversationTurn] = []
        self.session_id = str(uuid4())
        self.started_at = datetime.now()
    
    def add_turn(self, user_message: Message, assistant_message: Message) -> None:
        """Add a conversation turn to the buffer.
        
        Automatically evicts oldest turn if buffer exceeds max_turns.
        
        Args:
            user_message: User's message
            assistant_message: Assistant's response
        """
        turn = ConversationTurn(
            user_message=user_message,
            assistant_message=assistant_message
        )
        self.turns.append(turn)
        
        # Evict oldest turn if we exceed the limit
        if len(self.turns) > self.max_turns:
            self.turns.pop(0)
    
    def get_context_for_llm(self) -> List[Dict[str, str]]:
        """Format conversation history for LLM prompt.
        
        Returns:
            List of message dictionaries with role and content
        """
        messages = []
        for turn in self.turns:
            messages.append({
                "role": turn.user_message.role,
                "content": turn.user_message.content
            })
            messages.append({
                "role": turn.assistant_message.role,
                "content": turn.assistant_message.content
            })
        return messages
    
    def export_to_json(self) -> str:
        """Export conversation buffer to JSON format.
        
        Returns:
            JSON string representation of the conversation buffer
        """
        data = {
            "session_id": self.session_id,
            "started_at": self.started_at.isoformat(),
            "max_turns": self.max_turns,
            "turns": [
                {
                    "user_message": {
                        "role": turn.user_message.role,
                        "content": turn.user_message.content,
                        "timestamp": turn.user_message.timestamp.isoformat(),
                        "metadata": turn.user_message.metadata
                    },
                    "assistant_message": {
                        "role": turn.assistant_message.role,
                        "content": turn.assistant_message.content,
                        "timestamp": turn.assistant_message.timestamp.isoformat(),
                        "metadata": turn.assistant_message.metadata
                    }
                }
                for turn in self.turns
            ]
        }
        return json.dumps(data, indent=2)
    
    def clear(self) -> None:
        """Clear all conversation history from the buffer."""
        self.turns.clear()
        self.session_id = str(uuid4())
        self.started_at = datetime.now()
    
    def __len__(self) -> int:
        """Return the number of turns in the buffer."""
        return len(self.turns)
