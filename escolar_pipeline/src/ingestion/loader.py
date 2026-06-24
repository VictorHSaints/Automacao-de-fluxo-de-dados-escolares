import pandas as pd
from pathlib import Path
from src.utils.logger import get_logger

logger = get_logger(__name__)

def load_raw_xls(file_path: Path) -> pd.DataFrame:
    """
    Lê o arquivo XLS bruto gerado pelo sistema da escola.
    
    Args:
        file_path (Path): Caminho para o arquivo XLS.
        
    Returns:
        pd.DataFrame: DataFrame contendo os dados brutos.
    """
    logger.info(f"Iniciando leitura do arquivo: {file_path}")
    # TODO: Implementar leitura do XLS com pandas (tratar engine, pular linhas irrelevantes, etc)
    pass