"""
Module to handle all keyboard related functions.
"""

from pynput import keyboard
from .state import AppState

class KeyboardHandler:
    """
    Handle all keyboard inputs and project their changes through AppState.
    """

    def __init__(self, state: AppState):
        """
        Use the AppState to create a listener for keyboard inputs.
        """
        self.state = state
        self.listener = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)

    def _on_press(self, key):
        """Determine behavior when certain keys are pressed."""
        if key == keyboard.Key.space:
            self.state.push_to_talk = True
        elif key == keyboard.Key.enter:
            self.state.transcribe_to_en = True
        elif key == keyboard.Key.esc:
            print("\nESC pressed, program exiting")
            self.state.running = False

    def _on_release(self, key):
        """Determine behavior when certain keys are released."""
        if key == keyboard.Key.space:
            self.state.push_to_talk = False
        elif key == keyboard.Key.enter:
            self.state.transcribe_to_en = False

    def start(self):
        """Start the keyboard listener."""
        self.listener.start()

    def stop(self):
        """Stop the keyboard listener."""
        self.listener.stop()
