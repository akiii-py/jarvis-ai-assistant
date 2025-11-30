"""LLM Engine wrapper for Ollama integration."""

from typing import List, Dict, Optional
import requests

from jarvis.models import Message, PersonalityConfig


class LLMConfig:
    """Configuration for LLM Engine."""
    
    def __init__(
        self,
        model: str = "mistral:7b",
        endpoint: str = "http://localhost:11434",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ):
        self.model = model
        self.endpoint = endpoint
        self.temperature = temperature
        self.max_tokens = max_tokens


class LLMEngine:
    """Wrapper for Ollama API with prompt management."""
    
    def __init__(self, config: Optional[LLMConfig] = None):
        """Initialize LLM Engine.
        
        Args:
            config: LLM configuration. Uses defaults if not provided.
        """
        self.config = config or LLMConfig()
    
    def format_prompt(
        self,
        user_input: str,
        context: List[Dict[str, str]],
        personality: Optional[PersonalityConfig] = None
    ) -> List[Dict[str, str]]:
        """Format prompt with context and personality.
        
        Args:
            user_input: Current user input
            context: Previous conversation messages
            personality: Personality configuration
            
        Returns:
            List of formatted messages for the LLM
        """
        messages = []
        
        # Add system message with personality if provided
        if personality:
            system_prompt = self._build_system_prompt(personality)
            messages.append({"role": "system", "content": system_prompt})
        
        # Add conversation context
        messages.extend(context)
        
        # Add current user input
        messages.append({"role": "user", "content": user_input})
        
        return messages
    
    def _build_system_prompt(self, personality: PersonalityConfig) -> str:
        """Build system prompt based on personality configuration.
        
        Args:
            personality: Personality configuration
            
        Returns:
            System prompt string
        """
        tone_descriptions = {
            "mentor": "You are a patient and encouraging mentor who explains concepts clearly.",
            "sarcastic": "You are witty and sarcastic, but still helpful.",
            "neutral": "You are a helpful and professional assistant.",
            "enthusiastic": "You are energetic and enthusiastic about helping!"
        }
        
        verbosity_descriptions = {
            "concise": "Keep your responses brief and to the point.",
            "detailed": "Provide thorough and detailed explanations.",
            "balanced": "Balance brevity with necessary detail."
        }
        
        tone_desc = tone_descriptions.get(personality.tone, tone_descriptions["neutral"])
        verbosity_desc = verbosity_descriptions.get(personality.verbosity, verbosity_descriptions["balanced"])
        
        return f"{tone_desc} {verbosity_desc} {personality.response_style}"
    
    def generate(
        self,
        prompt: str,
        context: List[Dict[str, str]],
        personality: Optional[PersonalityConfig] = None
    ) -> str:
        """Generate response using Ollama API.
        
        Args:
            prompt: User input prompt
            context: Conversation context
            personality: Personality configuration
            
        Returns:
            Generated response text
            
        Raises:
            ConnectionError: If Ollama service is not available
            RuntimeError: If generation fails
        """
        messages = self.format_prompt(prompt, context, personality)
        
        try:
            response = requests.post(
                f"{self.config.endpoint}/api/chat",
                json={
                    "model": self.config.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": self.config.temperature,
                        "num_predict": self.config.max_tokens
                    }
                },
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("message", {}).get("content", "")
            
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                "Cannot connect to Ollama. Make sure Ollama is running "
                "(install from https://ollama.ai and run 'ollama serve')"
            )
        except requests.exceptions.Timeout:
            raise RuntimeError("LLM request timed out. Try again.")
        except Exception as e:
            raise RuntimeError(f"LLM generation failed: {str(e)}")
    
    def check_availability(self) -> bool:
        """Check if Ollama service is available.
        
        Returns:
            True if service is available, False otherwise
        """
        try:
            response = requests.get(f"{self.config.endpoint}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
