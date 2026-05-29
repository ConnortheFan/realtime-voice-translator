"""
Module for controlling shared runtime state throughout entire pipeline.
"""

from dataclasses import dataclass

@dataclass
class AppState:
    """Dataclass holding global application state flags for pipeline."""
    recording: bool = False
    running: bool = True
    transcribe_to_en: bool = False
