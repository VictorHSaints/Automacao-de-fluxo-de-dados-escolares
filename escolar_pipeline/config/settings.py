import os
from pathlib import Path

# Definição de caminhos base usando pathlib para compatibilidade de SO
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Caminhos específicos de dados
RAW_DATA_PATH = DATA_DIR / "raw"
PROCESSED_DATA_PATH = DATA_DIR / "processed"
OUTPUTS_PATH = DATA_DIR / "outputs"

# Configurações do App
APP_TITLE = "Dashboard de Desempenho Escolar - Foco Vestibular"