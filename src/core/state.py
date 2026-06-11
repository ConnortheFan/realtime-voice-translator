"""
Module for controlling shared runtime state throughout entire pipeline.
"""

from dataclasses import dataclass

@dataclass
class AppState:
    """Dataclass holding global application state flags for pipeline."""
    running: bool = True

    # _processing acts as a lock to prevent repeat processing
    push_to_talk: bool = False
    push_to_talk_processing: bool = False

    transcribe_to_en: bool = False
    transcribe_to_en_processing: bool = False
