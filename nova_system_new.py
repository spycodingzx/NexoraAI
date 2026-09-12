#!/usr/bin/env python3
"""
Autonomous Business Platform - Main Entry Point

This is now a thin wrapper that delegates to the modular core factory.
The heavy lifting has been moved to core/core/ and core/ui/ plugins.

Version: 2.0 (Refactored)
"""

# Environment setup must happen before any other imports
import os
import sys

# Add core directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "core", "tabs"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "core", "services"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "core", "utils"))
sys.path.insert(0, os.path.dirname(__file__))

# SDL/Pygame configuration (must be before imports)
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Import and run the modular core
from core.core.nv_app_factory import create_app

if __name__ == "__main__":
    create_app()
