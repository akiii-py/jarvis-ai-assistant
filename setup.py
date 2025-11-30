"""Setup script for Jarvis AI Assistant."""

from setuptools import setup, find_packages

setup(
    name="jarvis-ai-assistant",
    version="0.1.0",
    description="Local-first AI assistant for MacBook M1",
    author="Your Name",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.31.0",
        "aiohttp>=3.9.0",
        "ollama>=0.1.0",
        "openai-whisper>=20231117",
        "pyaudio>=0.2.14",
        "pvporcupine>=2.2.0",
        "pyobjc-core>=10.0",
        "pyobjc-framework-Cocoa>=10.0",
        "pypdf>=3.17.0",
        "pdfplumber>=0.10.0",
        "pytest>=7.4.0",
        "pytest-asyncio>=0.21.0",
        "hypothesis>=6.92.0",
        "python-dotenv>=1.0.0",
        "rich>=13.7.0",
        "watchdog>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "jarvis=jarvis.main:main",
        ],
    },
)
