"""Configurazione globale dell'applicazione"""
import os
from pathlib import Path

# Percorsi base
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "app" / "data"
STATIC_DIR = BASE_DIR / "app" / "static"
AUDIO_DIR = STATIC_DIR / "audio"

# Configurazione Flask
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 5000))

# Configurazione scoring
DEFAULT_TOP_N = 5
MAX_RESULTS = 20
DIVERSITY_THRESHOLD = 0.15  # Soglia similarità per diversity filtering

# Configurazione budget
BUDGET_SOFT_MARGIN = 0.10  # +10% per suggerimenti soft

# Configurazione audio
AUDIO_SAMPLE_DURATION = 3  # secondi
AUDIO_NORMALIZATION_LUFS = -18.0

# Regioni supportate
SUPPORTED_REGIONS = ["EU", "US", "UK", "ASIA"]
DEFAULT_REGION = "EU"

# Lingue supportate
SUPPORTED_LANGUAGES = ["IT", "EN"]
DEFAULT_LANGUAGE = "IT"
