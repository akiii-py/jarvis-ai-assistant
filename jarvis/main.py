"""Main entry point for Jarvis AI Assistant."""

import sys
from jarvis.agent_orchestrator import AgentOrchestrator
from jarvis.llm_engine import LLMConfig


def main():
    """Run Jarvis in interactive mode."""
    print("=" * 60)
    print("JARVIS - Local AI Assistant")
    print("=" * 60)
    print("\nInitializing...")
    
    # Initialize orchestrator
    orchestrator = AgentOrchestrator()
    
    # Check if Ollama is available
    if not orchestrator.llm_engine.check_availability():
        print("\n⚠️  WARNING: Ollama service not detected!")
        print("Please install Ollama from https://ollama.ai")
        print("Then run: ollama pull mistral:7b")
        print("And start the service: ollama serve")
        print("\nContinuing in demo mode (responses will fail)...\n")
    else:
        print("✓ Ollama service connected")
        print(f"✓ Model: {orchestrator.llm_engine.config.model}")
        print(f"✓ Personality: {orchestrator.personality.tone}, {orchestrator.personality.verbosity}")
    
    print("\nCommands:")
    print("  /export  - Export conversation to JSON")
    print("  /clear   - Clear conversation history")
    print("  /quit    - Exit Jarvis")
    print("\nReady! Start chatting...\n")
    
    # Main conversation loop
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle special commands
            if user_input.lower() == "/quit":
                print("\nGoodbye!")
                break
            
            elif user_input.lower() == "/export":
                json_output = orchestrator.export_conversation()
                print("\n" + json_output + "\n")
                continue
            
            elif user_input.lower() == "/clear":
                confirm = input("Clear conversation history? (yes/no): ").strip().lower()
                if confirm == "yes":
                    message = orchestrator.clear_conversation()
                    print(f"\n{message}\n")
                continue
            
            # Process normal input
            response = orchestrator.process_input(user_input)
            print(f"\nJarvis: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}\n")


if __name__ == "__main__":
    main()
