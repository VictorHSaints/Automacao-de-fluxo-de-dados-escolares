import pandas as pd
from src.utils.logger import get_logger

logger = get_logger(__name__)

def clean_data(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica regras de limpeza nos dados brutos: remove vazios, 
    resolve células mescladas e padroniza colunas.
    
    Args:
        df_raw (pd.DataFrame): Dados brutos.
        
    Returns:
        pd.DataFrame: Dados limpos e padronizados.
    """
    logger.info("Iniciando processo de limpeza de dados")
    
    # Fazemos uma cópia para não alterar o dataframe original em memória
    df = df_raw.copy()
    
    # 1. Remover colunas inteiramente vazias (criadas por colunas mescladas/espaços no Excel)
    df = df.dropna(axis=1, how='all')
    
    # 2. Padronizar nomes das colunas (minúsculas, sem espaços laterais, trocando espaços internos por _)
    df.columns = df.columns.astype(str).str.strip().str.lower().str.replace(' ', '_')
    # Remove também caracteres especiais se houver
    df.columns = df.columns.str.replace('ó', 'o').str.replace('í', 'i').str.replace('ã', 'a')
    
    # 2.1 NOVO: Remover colunas "unnamed" (fantasmas geradas por formatação do Excel)
    df = df.loc[:, ~df.columns.str.contains('unnamed', case=False)]
    
    # 3. Remover linhas inteiramente vazias
    df = df.dropna(axis=0, how='all')
    
    # 4. Tratar células mescladas (Preenchimento para frente/trás)
    # No Excel, células mescladas viram um valor válido seguido de NaNs.
    # Usamos ffill() para copiar o valor válido para as linhas de baixo.
    cols_identificadores = ['codigo', 'aluno', 'turma']
    for col in cols_identificadores:
        if col in df.columns:
            df[col] = df[col].ffill().bfill()
            
    # 5. Filtrar apenas as linhas que realmente possuem notas
    # As linhas extras geradas pelas células mescladas ficarão sem 'total' ou 'class', podemos dropá-las
    if 'total' in df.columns:
        df = df.dropna(subset=['total'])
        
    # 6. Limpeza de Tipos
    if 'codigo' in df.columns:
        # Garante que o código do aluno seja string limpa (removendo .0)
        df['codigo'] = df['codigo'].astype(str).str.replace(r'\.0$', '', regex=True)
        
    # Colunas de notas conhecidas para converter para Float
    notas_cols = ['bio', 'ing', 'mat', 'port', 'total', 'class']
    for col in notas_cols:
        if col in df.columns:
            # Transforma em numérico. Se houver texto indevido, vira NaN. Em seguida, preenche NaN com 0.
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
            
    logger.info(f"Limpeza concluída. Shape final: {df.shape}")
    return df.reset_index(drop=True)