"""
Main module to run entire program. Run:

python src/main.py

to start.
"""

from log_utils import setup_logging
from core import App

def main():
    """
    Main function to run entire program. Run:

    python src/main.py

    to start.
    """
    setup_logging(debug = True)
    app = App()
    app.run()

if __name__ == "__main__":
    main()
