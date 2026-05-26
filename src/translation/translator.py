"""
Translating module using Argos Translate for offline translation.
"""

import argostranslate.package
import argostranslate.translate
import time

class Translator:
    """
    Translate text between 2 set languages offline.

    This class provides an interface to use Argos Translate to translate text between 2 languages.

    Downloading language packs requires internet connection.    
    """

    def __init__(self, lang_a: str, lang_b: str = "en") -> None:
        """
        Initialize the translator. Upon first run with a language pair, will download language packs.

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
        start = time.perf_counter()

        self.lang_a = lang_a
        self.lang_b = lang_b
        
        # Install language pair packages if necessary
        installed = argostranslate.package.get_installed_packages()
        installed_pairs = {(p.from_code, p.to_code) for p in installed}

        if (lang_a, lang_b) not in installed_pairs:
            print(f"Installing {lang_a} -> {lang_b} package...")
            argostranslate.package.install_package_for_language_pair(lang_a, lang_b)
            print(f"Installed {lang_a} -> {lang_b} package")
        if (lang_b, lang_a) not in installed_pairs:
            print(f"Installing {lang_b} -> {lang_a} package...")
            argostranslate.package.install_package_for_language_pair(lang_b, lang_a)
            print(f"Installed {lang_b} -> {lang_a} package")

        end = time.perf_counter()
        print(f"\nInitializing translation pair took {end - start:.3f} seconds")

    def translate_ab(self, text: str, save: bool = True, filename: str = "outputs/translation_ab.txt") -> str:
        """
        Translate and return text from lang_a -> lang_b. Also, optionally save translation.

        Args:
            text (str): Text you want translated.
            save (bool): Whether to save translation to files.
                Defaults to True.
            filename (str): Destination to save transcribed text.
                Defaults to "outputs/translation_ab.txt".

        Returns:
            str: Translated text.
        """
        start = time.perf_counter()

        translated = argostranslate.translate.translate(text, self.lang_a, self.lang_b)

        print(f"Translating from {self.lang_a} -> {self.lang_b} took {time.perf_counter() - start:.3f} seconds")
    
        if save:
            start = time.perf_counter()

            with open(filename, "w", encoding="utf-8") as f:
                f.write(translated)
            
            print(f"Translation saved to {filename}")

            end = time.perf_counter()
            print(f"Saving took {end - start:.3f} seconds")

        return translated

    def translate_ba(self, text: str, save: bool = True, filename: str = "outputs/translation_ba.txt") -> str:
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
        start = time.perf_counter()

        translated = argostranslate.translate.translate(text, self.lang_b, self.lang_a)

        print(f"Translating from {self.lang_b} -> {self.lang_a} took {time.perf_counter() - start:.3f} seconds")

        if save:
            start = time.perf_counter()

            with open(filename, "w", encoding="utf-8") as f:
                f.write(translated)
            
            print(f"Translation saved to {filename}")
            print(f"Saving took {time.perf_counter() - start:.3f} seconds")

        return translated    
    
if __name__ == "__main__":
    t = Translator("it")
    translation = t.translate_ba("Hello, how are you? I'm fine thanks for asking. My brain is a bit fried right now, but it will heal in a few days. This is just a check to make sure that this module is working.")
    print(translation)

    translation = t.translate_ab("Ciao. Ecco il mio italiano e devo practicare. Piove, ma c'e il sole. Allora ho il keyboard italiano per fare questa text. Ciao, come stai? Sto bene grazie per averlo chiesto. Il mio cervello è un po' fritto in questo momento, ma guarirà in pochi giorni. Questo è solo un controllo per assicurarsi che questo modulo stia funzionando.")
    print(translation)