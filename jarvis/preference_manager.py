"""Preference management for user settings."""

import json
import os
from pathlib import Path
from typing import Optional

from jarvis.models import PersonalityConfig


class PreferenceManager:
    """Manages loading and saving user preferences."""
    
    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize preference manager.
        
        Args:
            config_dir: Directory for storing preferences. Defaults to ~/.jarvis/
        """
        if config_dir is None:
            config_dir = Path.home() / ".jarvis"
        
        self.config_dir = config_dir
        self.preferences_file = self.config_dir / "preferences.json"
        self._ensure_config_dir()
    
    def _ensure_config_dir(self) -> None:
        """Create config directory if it doesn't exist."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def load_preferences(self) -> dict:
        """Load user preferences from JSON file.
        
        Returns:
            Dictionary containing user preferences, or default preferences if file doesn't exist
        """
        if not self.preferences_file.exists():
            return self._get_default_preferences()
        
        try:
            with open(self.preferences_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading preferences: {e}. Using defaults.")
            return self._get_default_preferences()
    
    def save_preferences(self, preferences: dict) -> None:
        """Save user preferences to JSON file.
        
        Args:
            preferences: Dictionary containing user preferences
        """
        self._ensure_config_dir()
        with open(self.preferences_file, 'w') as f:
            json.dump(preferences, f, indent=2)
    
    def get_personality_config(self) -> PersonalityConfig:
        """Get personality configuration from preferences.
        
        Returns:
            PersonalityConfig object
        """
        prefs = self.load_preferences()
        personality_data = prefs.get("personality", {})
        
        return PersonalityConfig(
            tone=personality_data.get("tone", "neutral"),
            verbosity=personality_data.get("verbosity", "balanced"),
            response_style=personality_data.get("response_style", "helpful and informative"),
            voice_name=personality_data.get("voice_name", "Samantha"),
            sound_cues_enabled=personality_data.get("sound_cues_enabled", True)
        )
    
    def set_personality_config(self, personality: PersonalityConfig) -> None:
        """Save personality configuration to preferences.
        
        Args:
            personality: PersonalityConfig object to save
        """
        prefs = self.load_preferences()
        prefs["personality"] = {
            "tone": personality.tone,
            "verbosity": personality.verbosity,
            "response_style": personality.response_style,
            "voice_name": personality.voice_name,
            "sound_cues_enabled": personality.sound_cues_enabled
        }
        self.save_preferences(prefs)
    
    def _get_default_preferences(self) -> dict:
        """Get default preferences.
        
        Returns:
            Dictionary with default preference values
        """
        return {
            "personality": {
                "tone": "neutral",
                "verbosity": "balanced",
                "response_style": "helpful and informative",
                "voice_name": "Samantha",
                "sound_cues_enabled": True
            },
            "wake_word": "Hey Jarvis",
            "default_language": "python",
            "project_templates": {},
            "command_whitelist": [],
            "study_topics": {}
        }
