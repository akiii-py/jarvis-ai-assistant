# 🤖 Jarvis AI Assistant

> *"Sometimes you gotta run before you can walk."* - Tony Stark

A local-first, privacy-focused AI assistant for MacBook M1/M2/M3, designed specifically for computer science students. Inspired by Iron Man's Jarvis, this assistant runs entirely on your Mac using open-source LLMs - no cloud, no subscriptions, complete privacy.

## ✨ Features

### Current (v0.1.0)
- 🤖 **Local LLM inference** using Ollama (Mistral 7B / Qwen 2 7B)
- 💬 **Smart conversations** with 10-turn context memory
- 🎭 **Customizable personality** (mentor, sarcastic, neutral, enthusiastic)
- 🔒 **Complete privacy** - all data stays on your Mac
- ⚡ **M1/M2/M3 optimized** with Metal acceleration
- 🎯 **Modular architecture** for easy extension

### Coming Soon
- 🎤 Voice interaction with wake word detection
- 💻 Mac system control (apps, settings, commands)
- 📁 Smart file management with project templates
- 👨‍💻 Coding companion (explain code, generate boilerplate, debug)
- 📚 Study sidekick (quiz, flashcards, PDF summaries)

## 🚀 Quick Start

### Prerequisites

- macOS (optimized for M1/M2/M3 Apple Silicon)
- Python 3.9 or higher
- [Ollama](https://ollama.ai) for running local LLMs

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/jarvis-ai-assistant.git
cd jarvis-ai-assistant
```

2. **Set up Python environment:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Install and configure Ollama:**
```bash
# Install Ollama
brew install ollama

# Pull the Mistral 7B model
ollama pull mistral:7b

# Start Ollama service (keep this running in a separate terminal)
ollama serve
```

4. **Run Jarvis:**
```bash
python -m jarvis.main
```

## 💡 Usage

### Interactive Mode

Start chatting with Jarvis:
```bash
python -m jarvis.main
```

Example conversation:
```
You: What is a binary search tree?
Jarvis: A binary search tree (BST) is a data structure where each node has at most two children...

You: Can you explain time complexity?
Jarvis: Time complexity measures how the runtime of an algorithm grows...
```

### Available Commands

| Command | Description |
|---------|-------------|
| `/export` | Export conversation history to JSON |
| `/clear` | Clear conversation history (with confirmation) |
| `/quit` | Exit Jarvis |

### Customizing Personality

Edit `~/.jarvis/preferences.json` to customize:
```json
{
  "personality": {
    "tone": "mentor",           // mentor, sarcastic, neutral, enthusiastic
    "verbosity": "balanced",    // concise, detailed, balanced
    "response_style": "helpful and informative"
  }
}
```

## Project Structure

```
jarvis/
├── __init__.py
├── models.py                 # Core data models
├── conversation_buffer.py    # Conversation context management
├── preference_manager.py     # User preferences and settings
├── llm_engine.py            # Ollama LLM wrapper
├── agent_orchestrator.py    # Central coordinator
└── main.py                  # Entry point
```

## Configuration

Preferences are stored in `~/.jarvis/preferences.json`. You can customize:

- Personality tone (mentor, sarcastic, neutral, enthusiastic)
- Verbosity (concise, detailed, balanced)
- Response style
- Voice settings
- Sound cues

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Voice UI Layer                        │
│  (Wake Word Detection, STT, TTS, Audio I/O)            │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Agent Orchestration Layer                  │
│  (Intent Recognition, Context Management, Tool Routing) │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                 Local LLM Engine                        │
│        (Ollama + Mistral 7B / Qwen 2 7B)               │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  Tool Modules                           │
│  (Mac Control, Files, Coding, Study, System)           │
└─────────────────────────────────────────────────────────┘
```

## 📊 Development Roadmap

### ✅ Phase 1: Foundation (Current)
- [x] Project structure and virtual environment
- [x] Conversation buffer with 10-turn context
- [x] Preference management system
- [x] LLM Engine wrapper with Ollama integration
- [x] Basic conversation loop

### 🚧 Phase 2: Voice Interface (In Progress)
- [ ] Wake word detection (Porcupine)
- [ ] Speech-to-text (Whisper)
- [ ] Text-to-speech (macOS native)
- [ ] Sound cues and audio pipeline

### 📋 Phase 3: Mac Control
- [ ] Application launcher
- [ ] System settings control
- [ ] Command whitelist and security
- [ ] Destructive operation confirmation

### 📋 Phase 4: File Management
- [ ] Project templates (DSA, OS, COA)
- [ ] File operations (create, move, rename, delete)
- [ ] Backup and restore system

### 📋 Phase 5: Coding Companion
- [ ] Code explanation
- [ ] Boilerplate generation
- [ ] Build orchestration
- [ ] Error analysis and debugging

### 📋 Phase 6: Study Sidekick
- [ ] PDF summarization
- [ ] Concept explanations
- [ ] Quiz management (PYQ)
- [ ] Flashcard generation

## 🧪 Testing

Run unit tests:
```bash
source venv/bin/activate
pytest tests/
```

Run property-based tests:
```bash
pytest tests/ -v -k property
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by Iron Man's Jarvis
- Built with [Ollama](https://ollama.ai) for local LLM inference
- Optimized for Apple Silicon (M1/M2/M3)

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Note:** This is an educational project designed for computer science students. It prioritizes privacy, local execution, and learning over cloud-based convenience.
