"""Tests for ConversationBuffer."""

import json
from datetime import datetime
from jarvis.conversation_buffer import ConversationBuffer
from jarvis.models import Message


def test_conversation_buffer_initialization():
    """Test that buffer initializes correctly."""
    buffer = ConversationBuffer(max_turns=10)
    assert len(buffer) == 0
    assert buffer.max_turns == 10
    assert buffer.session_id is not None


def test_add_turn():
    """Test adding a conversation turn."""
    buffer = ConversationBuffer(max_turns=10)
    user_msg = Message(role="user", content="Hello")
    assistant_msg = Message(role="assistant", content="Hi there!")
    
    buffer.add_turn(user_msg, assistant_msg)
    assert len(buffer) == 1


def test_buffer_eviction():
    """Test that oldest turns are evicted when limit is exceeded."""
    buffer = ConversationBuffer(max_turns=3)
    
    # Add 5 turns
    for i in range(5):
        user_msg = Message(role="user", content=f"Message {i}")
        assistant_msg = Message(role="assistant", content=f"Response {i}")
        buffer.add_turn(user_msg, assistant_msg)
    
    # Should only have 3 turns (the last 3)
    assert len(buffer) == 3
    assert buffer.turns[0].user_message.content == "Message 2"
    assert buffer.turns[2].user_message.content == "Message 4"


def test_get_context_for_llm():
    """Test formatting context for LLM."""
    buffer = ConversationBuffer(max_turns=10)
    user_msg = Message(role="user", content="Hello")
    assistant_msg = Message(role="assistant", content="Hi!")
    buffer.add_turn(user_msg, assistant_msg)
    
    context = buffer.get_context_for_llm()
    assert len(context) == 2
    assert context[0]["role"] == "user"
    assert context[0]["content"] == "Hello"
    assert context[1]["role"] == "assistant"
    assert context[1]["content"] == "Hi!"


def test_export_to_json():
    """Test exporting conversation to JSON."""
    buffer = ConversationBuffer(max_turns=10)
    user_msg = Message(role="user", content="Test")
    assistant_msg = Message(role="assistant", content="Response")
    buffer.add_turn(user_msg, assistant_msg)
    
    json_str = buffer.export_to_json()
    data = json.loads(json_str)
    
    assert "session_id" in data
    assert "turns" in data
    assert len(data["turns"]) == 1
    assert data["turns"][0]["user_message"]["content"] == "Test"


def test_clear():
    """Test clearing conversation buffer."""
    buffer = ConversationBuffer(max_turns=10)
    user_msg = Message(role="user", content="Test")
    assistant_msg = Message(role="assistant", content="Response")
    buffer.add_turn(user_msg, assistant_msg)
    
    assert len(buffer) == 1
    
    buffer.clear()
    assert len(buffer) == 0
