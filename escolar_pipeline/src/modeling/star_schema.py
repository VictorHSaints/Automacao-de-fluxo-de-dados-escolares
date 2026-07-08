import pandas as pd
import uuid
from typing import Dict, Any
from src.utils.logger import get_logger

logger = get_logger(__name__)

def build_star_schema(df_clean: pd.DataFrame, metadados_avaliacao: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
    """
    Transforma os dados limpos em um modelo Star Schema, aplicando Unpivot (Melt)
    nas notas e separando os dados em Fatos e Dimensões.
    
    Args:
        df_clean (pd.DataFrame): Dados limpos oriundos do processor.py.
        metadados_avaliacao (Dict): Dicionário com o contexto da prova. 
            Ex: {'nome': 'Simulado UFSC', 'etapa': 'Parte 1', 'data': '2023-05-20'}
        
    Returns:
        Dict[str, pd.DataFrame]: Dicionário com as tabelas Fato e Dimensões.
    """
    logger.info(f"Construindo modelo Star Schema para: {metadados_avaliacao.get('nome')} - {metadados_avaliacao.get('etapa')}")
    
    # Gera um ID único para esta avaliação que estamos processando
    id_avaliacao = str(uuid.uuid4())
    
    # -----------------------------------------
    # 1. Dimensão: Avaliação (dim_avaliacao)
    # -----------------------------------------
    metadados_avaliacao['id_avaliacao'] = id_avaliacao
    dim_avaliacao = pd.DataFrame([metadados_avaliacao])
    
    # -----------------------------------------
    # 2. Dimensão: Aluno (dim_aluno)
    # -----------------------------------------
    # Pegamos apenas os dados cadastrais únicos
    cols_aluno = ['codigo', 'aluno', 'turma']
    dim_aluno = df_clean[cols_aluno].drop_duplicates(subset=['codigo']).copy()
    dim_aluno.rename(columns={'codigo': 'id_aluno', 'aluno': 'nome_aluno'}, inplace=True)
    
    # -----------------------------------------
    # 3. Fato: Resultados Gerais (fact_resultados)
    # -----------------------------------------
    # Guarda o total e a classificação do aluno nesta avaliação específica
    cols_resultados = ['codigo', 'total', 'class']
    cols_existentes = [c for c in cols_resultados if c in df_clean.columns]
    
    fact_resultados = df_clean[cols_existentes].copy()
    fact_resultados.rename(columns={'codigo': 'id_aluno', 'class': 'classificacao'}, inplace=True)
    fact_resultados['id_avaliacao'] = id_avaliacao
    
    # -----------------------------------------
    # 4. Fato: Notas por Disciplina (fact_notas)
    # -----------------------------------------
    # Identificamos dinamicamente quais colunas são disciplinas 
    # (Tudo que não for identificador, total ou class)
    colunas_nao_disciplinas = ['codigo', 'aluno', 'turma', 'total', 'class']
    disciplinas = [col for col in df_clean.columns if col not in colunas_nao_disciplinas]
    
    # Melt (Unpivot): Transforma colunas de disciplinas em linhas
    fact_notas = df_clean.melt(
        id_vars=['codigo'], 
        value_vars=disciplinas,
        var_name='id_disciplina', 
        value_name='nota'
    )
    
    fact_notas.rename(columns={'codigo': 'id_aluno'}, inplace=True)
    fact_notas['id_avaliacao'] = id_avaliacao
    
    # Opcional: Remover linhas onde a nota é 0 (caso queira economizar espaço se o aluno faltou)
    # fact_notas = fact_notas[fact_notas['nota'] > 0]
    
    # Reordenando colunas da Fato Notas
    fact_notas = fact_notas[['id_aluno', 'id_avaliacao', 'id_disciplina', 'nota']]
    
    # -----------------------------------------
    # 5. Dimensão: Disciplina (dim_disciplina)
    # -----------------------------------------
    # Cria a dimensão baseada nas disciplinas encontradas neste arquivo
    dim_disciplina = pd.DataFrame({'id_disciplina': disciplinas})
    dim_disciplina['nome_disciplina'] = dim_disciplina['id_disciplina'].str.upper()

    schema = {
        'dim_aluno': dim_aluno,
        'dim_avaliacao': dim_avaliacao,
        'dim_disciplina': dim_disciplina,
        'fact_notas': fact_notas,
        'fact_resultados': fact_resultados
    }
    
    logger.info(f"Star Schema gerado: {len(dim_aluno)} alunos, {len(disciplinas)} disciplinas processadas.")
    
    return schema