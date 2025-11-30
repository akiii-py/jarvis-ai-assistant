"""Tests for PreferenceManager."""

import json
import tempfile
from pathlib import Path
from jarvis.preference_manager import PreferenceManager
from jarvis.models import PersonalityConfig


def test_preference_manager_initialization():
    """Test that preference manager initializes correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_dir = Path(tmpdir)
        pm = PreferenceManager(config_dir=config_dir)
        assert pm.config_dir == config_dir
        assert pm.config_dir.exists()


def test_load_default_preferences():
    """Test loading default preferences when file doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        pm = PreferenceManager(config_dir=Path(tmpdir))
        prefs = pm.load_preferences()
        
        assert "personality" in prefs
        assert "wake_word" in prefs
        assert prefs["personality"]["tone"] == "neutral"


def test_save_and_load_preferences():
    """Test saving and loading preferences."""
    with tempfile.TemporaryDirectory() as tmpdir:
        pm = PreferenceManager(config_dir=Path(tmpdir))
        
        # Save preferences
        test_prefs = {
            "personality": {
                "tone": "sarcastic",
                "verbosity": "concise"
            },
            "wake_word": "Hey Computer"
        }
        pm.save_preferences(test_prefs)
        
        # Load and verify
        loaded_prefs = pm.load_preferences()
        assert loaded_prefs["personality"]["tone"] == "sarcastic"
        assert loaded_prefs["wake_word"] == "Hey Computer"


def test_get_personality_config():
    """Test getting personality configuration."""
    with tempfile.TemporaryDirectory() as tmpdir:
        pm = PreferenceManager(config_dir=Path(tmpdir))
        personality = pm.get_personality_config()
        
        assert isinstance(personality, PersonalityConfig)
        assert personality.tone in ["mentor", "sarcastic", "neutral", "enthusiastic"]


def test_set_personality_config():
    """Test setting personality configuration."""
    with tempfile.TemporaryDirectory() as tmpdir:
        pm = PreferenceManager(config_dir=Path(tmpdir))
        
        # Create and save personality
        personality = PersonalityConfig(
            tone="enthusiastic",
            verbosity="detailed",
            response_style="energetic"
        )
        pm.set_personality_config(personality)
        
        # Load and verify
        loaded_personality = pm.get_personality_config()
        assert loaded_personality.tone == "enthusiastic"
        assert loaded_personality.verbosity == "detailed"
        assert loaded_personality.response_style == "energetic"
