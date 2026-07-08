import pandas as pd
from pathlib import Path
from src.utils.logger import get_logger

logger = get_logger(__name__)

def load_raw_xls(file_path: Path) -> pd.DataFrame:
    """
    Lê o arquivo XLS bruto gerado pelo sistema da escola.
    Ignora as linhas iniciais de cabeçalho do relatório e lê a tabela real.
    
    Args:
        file_path (Path): Caminho para o arquivo XLS/CSV.
        
    Returns:
        pd.DataFrame: DataFrame contendo os dados brutos.
    """
    logger.info(f"Iniciando leitura do arquivo: {file_path}")
    
    try:
        # Pula as 3 primeiras linhas (0, 1 e 2). O cabeçalho passa a ser a linha 4.
        # Caso seja arquivo .xls real, usamos read_excel. 
        # (Adicionei o fallback para CSV caso você esteja testando com a amostra)
        if str(file_path).endswith('.csv'):
            df = pd.read_csv(file_path, skiprows=3)
        else:
            df = pd.read_excel(file_path, skiprows=3)
            
        logger.info(f"Arquivo lido com sucesso. Shape inicial: {df.shape}")
        return df
        
    except Exception as e:
        logger.error(f"Erro ao ler o arquivo {file_path}: {e}")
        raise