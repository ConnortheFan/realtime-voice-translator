"""
Download Piper TTS voice models by language code.
"""

from pathlib import Path
from piper.download_voices import download_voice

DOWNLOAD_DIR = Path("./voices")

# All languages in 2 letter code, except en (_GB or _US), es (_AR, _ES, _MX), and nl (_BE, _NL)
BEST_VOICES = {
    "ar": [
        "ar_JO-kareem-medium",
        "ar_JO-kareem-low",
    ],

    "bg": [
        "bg_BG-dimitar-medium",
    ],

    "ca": [
        "ca_ES-upc_ona-medium",
        "ca_ES-upc_ona-x_low",
        "ca_ES-upc_pau-x_low",
    ],

    "cs": [
        "cs_CZ-jirka-medium",
        "cs_CZ-jirka-low",
    ],

    "cy": [
        "cy_GB-bu_tts-medium",
        "cy_GB-gwryw_gogleddol-medium",
    ],

    "da": [
        "da_DK-talesyntese-medium",
    ],

    "de": [
        "de_DE-thorsten-high",
        "de_DE-thorsten_emotional-medium",
        "de_DE-thorsten-medium",
        "de_DE-mls-medium",
        "de_DE-karlsson-low",
    ],

    "el": [
        "el_GR-rapunzelina-medium",
        "el_GR-rapunzelina-low",
    ],

    "en_GB": [
        "en_GB-cori-high",
        "en_GB-cori-medium",
        "en_GB-jenny_dioco-medium",
        "en_GB-alan-medium",
        "en_GB-semaine-medium",
        "en_GB-alba-medium",
    ],

    "en_US": [
        "en_US-lessac-high",
        "en_US-ryan-high",
        "en_US-libritts-high",
        "en_US-lessac-medium",
        "en_US-ljspeech-high",
        "en_US-ryan-medium",
        "en_US-amy-medium",
        "en_US-john-medium",
    ],

    "es_AR": [
        "es_AR-daniela-high",
    ],

    "es_ES": [
        "es_ES-sharvard-medium",
        "es_ES-davefx-medium",
        "es_ES-carlfm-x_low",
    ],

    "es_MX": [
        "es_MX-claude-high",
        "es_MX-ald-medium",
    ],

    "eu": [
        "eu_ES-maider-medium",
        "eu_ES-antton-medium",
    ],

    "fa": [
        "fa_IR-ganji_adabi-medium",
        "fa_IR-ganji-medium",
        "fa_IR-amir-medium",
        "fa_IR-gyro-medium",
    ],

    "fi": [
        "fi_FI-harri-medium",
        "fi_FI-harri-low",
    ],

    "fr": [
        "fr_FR-tom-medium",
        "fr_FR-siwis-medium",
        "fr_FR-upmc-medium",
        "fr_FR-mls-medium",
        "fr_FR-gilles-low",
    ],

    "hi": [
        "hi_IN-priyamvada-medium",
        "hi_IN-pratham-medium",
        "hi_IN-rohan-medium",
    ],

    "hu": [
        "hu_HU-berta-medium",
        "hu_HU-anna-medium",
        "hu_HU-imre-medium",
    ],

    "id": [
        "id_ID-news_tts-medium",
    ],

    "is": [
        "is_IS-salka-medium",
        "is_IS-steinn-medium",
        "is_IS-ugla-medium",
        "is_IS-bui-medium",
    ],

    "it": [
        "it_IT-paola-medium",
        "it_IT-riccardo-x_low",
    ],

    "ka": [
        "ka_GE-natia-medium",
    ],

    "kk": [
        "kk_KZ-issai-high",
        "kk_KZ-iseke-x_low",
        "kk_KZ-raya-x_low",
    ],

    "ku": [
        "ku_TR-berfin_renas-medium",
    ],

    "lb": [
        "lb_LU-marylux-medium",
    ],

    "lv": [
        "lv_LV-aivars-medium",
    ],

    "ml": [
        "ml_IN-meera-medium",
        "ml_IN-arjun-medium",
    ],

    "ne": [
        "ne_NP-google-medium",
        "ne_NP-google-x_low",
        "ne_NP-chitwan-medium",
    ],

    "nl_BE": [
        "nl_BE-nathalie-medium",
        "nl_BE-rdh-medium",
        "nl_BE-nathalie-x_low",
    ],

    "nl_NL": [
        "nl_NL-pim-medium",
        "nl_NL-ronnie-medium",
        "nl_NL-alex-medium",
        "nl_NL-mls-medium",
    ],

    "no": [
        "no_NO-talesyntese-medium",
        "no_NO-nvcc-medium",
    ],

    "pl": [
        "pl_PL-bass-high",
        "pl_PL-darkman-medium",
        "pl_PL-gosia-medium",
    ],

    "pt_BR": [
        "pt_BR-faber-medium",
        "pt_BR-cadu-medium",
        "pt_BR-jeff-medium",
        "pt_BR-edresson-low",
    ],

    "pt_PT": [
        "pt_PT-tugão-medium",
    ],

    "ro": [
        "ro_RO-mihai-medium",
    ],

    "ru": [
        "ru_RU-irina-medium",
        "ru_RU-dmitri-medium",
        "ru_RU-denis-medium",
        "ru_RU-ruslan-medium",
    ],

    "sk": [
        "sk_SK-lili-medium",
    ],

    "sl": [
        "sl_SI-artur-medium",
    ],

    "sq": [
        "sq_AL-edon-medium",
    ],

    "sr": [
        "sr_RS-serbski_institut-medium",
    ],

    "sv": [
        "sv_SE-alma-medium",
        "sv_SE-lisa-medium",
        "sv_SE-nst-medium",
    ],

    "sw": [
        "sw_CD-lanfrica-medium",
    ],

    "te": [
        "te_IN-padmavathi-medium",
        "te_IN-venkatesh-medium",
        "te_IN-maya-medium",
    ],

    "tr": [
        "tr_TR-dfki-medium",
    ],

    "uk": [
        "uk_UA-oleksa-high",
        "uk_UA-mykyta-high",
        "uk_UA-tetiana-high",
        "uk_UA-ukrainian_tts-medium",
    ],

    "ur": [
        "ur_PK-fasih-medium",
    ],

    "vi": [
        "vi_VN-vais1000-medium",
        "vi_VN-25hours_single-low",
        "vi_VN-vivos-x_low",
    ],

    "zh": [
        "zh_CN-huayan-medium",
        "zh_CN-chaowen-medium",
        "zh_CN-xiao_ya-medium",
        "zh_CN-huayan-x_low",
    ],
}

# Change this depending on your preferences
# en _GB _US
# es _AR _ES _MX
# nl _BE _NL
REGION_PRIORITY = {
    "en" : "en_US",
    "es" : "es_ES",
    "nl" : "nl_NL",
}

def download_voice_tts(lang: str, force: bool = False) -> None:
    """
    Download the best voice for a given language.

    Will follow REGION_PRIORITY for dialect preferences for en, es, and nl.

    Will download first voice found in BEST_VOICES for a given language.

    Args:
        lang (str): Language for the voice to download.
        force (bool): Whether to forcefully redownload the voice.
            Defaults to False.
    """
    code = lang

    code = REGION_PRIORITY.get(code, code)
    if code != lang:
        print(f"Code {lang} changed to {code}")

    if code is None:
        raise ValueError("Language code doesn't exist.")

    voices = BEST_VOICES.get(code)

    if voices is None:
        raise ValueError(f"Voice for {code} doesn't exist.")

    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Downloading voice {voices[0]} for {code}")
    download_voice(
        voice=voices[0],
        download_dir=DOWNLOAD_DIR,
        force_redownload=force,
    )
    print("Finished download")
