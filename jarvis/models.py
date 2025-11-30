"""Core data models for Jarvis."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional


@dataclass
class Message:
    """Single conversation message."""
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConversationTurn:
    """Complete conversation turn (user input + assistant response)."""
    user_message: Message
    assistant_message: Message
    tool_calls: List[Any] = field(default_factory=list)


@dataclass
class PersonalityConfig:
    """Agent personality configuration."""
    tone: Literal["mentor", "sarcastic", "neutral", "enthusiastic"] = "neutral"
    verbosity: Literal["concise", "detailed", "balanced"] = "balanced"
    response_style: str = "helpful and informative"
    voice_name: str = "Samantha"
    sound_cues_enabled: bool = True
