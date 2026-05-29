"""
Translating module using Argos Translate for offline translation.
"""

import argostranslate.package
import argostranslate.translate
from log_utils import get_logger, log_calls

class Translator:
    """
    Translate text between 2 set languages offline.

    This class provides an interface to use Argos Translate to translate text between 2 languages.

    Downloading language packs requires internet connection.    
    """

    logger = get_logger(__name__)

    @log_calls
    def __init__(self, lang_a: str, lang_b: str = "en") -> None:
        """
        Initialize the translator. 
        
        Upon first run with a language pair, will download language packs.

        Language codes include (ISO 639): 
            en - English
            it - Italian
            es - Spanish
            fr - French
            de - German
            zh - Chinese
            ja - Japanese
            ko - Korean
            ar - Arabic

        Args:
            lang_a: ISO 639 code for the first language.
            lang_b: ISO 639 code for the second language.
                Defaults to "en".
        """
        self.lang_a = lang_a
        self.lang_b = lang_b

        # Install language pair packages if necessary
        installed = argostranslate.package.get_installed_packages()
        installed_pairs = {(p.from_code, p.to_code) for p in installed}

        if (lang_a, lang_b) not in installed_pairs:
            self.logger.info("Installing %s -> %s package...", lang_a, lang_b)
            argostranslate.package.install_package_for_language_pair(lang_a, lang_b)
            self.logger.info("Installed package")
        if (lang_b, lang_a) not in installed_pairs:
            self.logger.info("Installing %s -> %s package...", lang_b, lang_a)
            argostranslate.package.install_package_for_language_pair(lang_b, lang_a)
            self.logger.info("Installed package")

    @log_calls
    def translate_ab(
        self,
        text: str,
        save: bool = True,
        filename: str = "outputs/translation_ab.txt",
    ) -> str:
        """
        Translate and return text from lang_a -> lang_b.
        Also, optionally save translation.

        Args:
            text (str): Text you want translated.
            save (bool): Whether to save translation to files.
                Defaults to True.
            filename (str): Destination to save transcribed text.
                Defaults to "outputs/translation_ab.txt".

        Returns:
            str: Translated text.
        """
        translated = argostranslate.translate.translate(text, self.lang_a, self.lang_b)

        if save:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(translated)

            self.logger.debug("Translation saved to %s", filename)

        return translated

    @log_calls
    def translate_ba(
        self,
        text: str,
        save: bool = True,
        filename: str = "outputs/translation_ba.txt",
    ) -> str:
        """
        Translate and return text from lang_b -> lang_a. Also, optionally save translation.

        Args:
            text (str): Text you want translated.
            save (bool): Whether to save translation to files.
                Defaults to True.
            filename (str): Destination to save transcribed text.
                Defaults to "outputs/translation_ba.txt".

        Returns:
            str: Translated text.
        """
        translated = argostranslate.translate.translate(text, self.lang_b, self.lang_a)

        if save:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(translated)

            self.logger.debug("Translation saved to %s", filename)

        return translated
