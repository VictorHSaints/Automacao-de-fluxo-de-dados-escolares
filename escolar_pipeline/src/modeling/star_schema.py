import pandas as pd
from typing import Dict
from src.utils.logger import get_logger

logger = get_logger(__name__)

def build_star_schema(df_clean: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Transforma os dados limpos em um modelo Star Schema.
    
    Args:
        df_clean (pd.DataFrame): Dados limpos.
        
    Returns:
        Dict[str, pd.DataFrame]: Dicionário contendo as tabelas Fato e Dimensões.
            Ex: {'fact_notas': df, 'dim_aluno': df, 'dim_disciplina': df}
    """
    logger.info("Construindo modelo Star Schema")
    # TODO: Separar o DataFrame em tabelas de fatos e dimensões
    pass
