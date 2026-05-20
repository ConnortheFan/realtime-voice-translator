"""
Download Argos Translate language pairs and Piper TTS voices.
 
Usage:
    python scripts/install_languages.py en it
    python scripts/install_languages.py en fr de ja
 
This will download ALL directional pairs between the given language codes.
For 3 languages (e.g. en es it), that's 6 pairs:
    en->es, es->en, en->it, it->en, es->it, it->es

This will also download the voices associated with each language for Text-to-Speech.
"""

import argparse
import argostranslate.package

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))
from src.tts.download_voice import download_voice_tts

from itertools import permutations

def main():
    # Set parser arguments and helpful documentation for --help
    parser = argparse.ArgumentParser(
        description="Install Argos Translate language pairs for all combinations of the given language codes.",
        epilog="Example: python scripts/install_languages.py en es it"
    )
    parser.add_argument(
        "languages",
        nargs="+",
        metavar="LANG_CODE",
        help="ISO 639-1 language codes (e.g. en es it fr de ja)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-download and reinstall pairs that are already installed."
    )
    args = parser.parse_args()

    # Remove duplicates and keep order
    codes = list(dict.fromkeys(c.lower() for c in args.languages))

    if len(codes) < 2:
        parser.error("Please provide at least 2 different language codes.")

    # Find all pairs of listed languages for downloading
    pairs = list(permutations(codes, 2))
    # print(pairs)

    # Check what is already installed
    installed = list((pkg.from_code, pkg.to_code) for pkg in argostranslate.package.get_installed_packages())
    # print(installed)
    
    pairs_to_install = []
    pairs_to_skip = []
    for pair in pairs:
        if pair in installed:
            pairs_to_skip.append(pair)
        else:
            pairs_to_install.append(pair)

    # Forced install
    if args.force:
        # Uninstall already existing packages
        print(f"Uninstalling {len(pairs_to_skip)} packages...")
        for from_code, to_code in pairs_to_skip:
            print(f"Uninstalling {from_code} -> {to_code}")
            argostranslate.package.uninstall(
                next(
                    pkg for pkg in argostranslate.package.get_installed_packages() if pkg.from_code == from_code and pkg.to_code == to_code
                )
            )

        # Reinstall all packages
        print(f"Installing {len(pairs)} packages...")
        for from_code, to_code in pairs:
            print(f"Installing {from_code} -> {to_code}")
            success = argostranslate.package.install_package_for_language_pair(from_code, to_code)
            if not success:
                print(f"ERROR: Package {from_code} -> {to_code} failed to install")
        print("Finished installing translation pairs")

        # Force install all voices
        print(f"Installing {len(codes)} voices...")
        for code in codes:
            print(f"Installing {code} voice")
            download_voice_tts(code, force=True)
        print("Finished installing voices")
        return


    # Nothing to install
    if not pairs_to_install:
        print("All language pairs are already installed. Use --force to reinstall.")
        return
    

    # Partial/regular installing
    if pairs_to_skip:
        print(f"Already installed {len(pairs_to_skip)} packages (skipping):")
        for from_code, to_code in pairs_to_skip:
            print(f"{from_code} -> {to_code}")
        print()
    if pairs_to_install:
        print(f"Installing {len(pairs_to_install)} packages...")
        for from_code, to_code in pairs_to_install:
            print(f"Installing {from_code} -> {to_code}")
            success = argostranslate.package.install_package_for_language_pair(from_code, to_code)
            if not success:
                print(f"ERROR: Package {from_code} -> {to_code} failed to install")
        print("Finished installing translation pairs")
        
    # Force install all voices
    print(f"Installing {len(codes)} voices...")
    for code in codes:
        print(f"Installing {code} voice")
        download_voice_tts(code)
    print("Finished installing voices")

if __name__ == "__main__":
    main()