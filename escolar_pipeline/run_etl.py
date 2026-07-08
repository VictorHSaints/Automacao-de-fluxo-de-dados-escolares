import os
import sys
from pathlib import Path
import pandas as pd

# Garante que o Python ache a pasta 'src' independentemente de onde o script for chamado
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importando as funções dos módulos que criamos
from src.ingestion.loader import load_raw_xls
from src.cleaning.processor import clean_data
from src.modeling.star_schema import build_star_schema
from src.utils.logger import get_logger

logger = get_logger(__name__)

def run_pipeline(caminho_arquivo: str, metadados: dict):
    """
    Função principal que orquestra a execução do pipeline de dados.
    """
    # Usando caminhos absolutos baseados no local deste script
    base_dir = Path(__file__).resolve().parent
    input_file = base_dir / caminho_arquivo
    output_dir = base_dir / "data" / "processed"
    
    # Garante que a pasta de saída exista
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info("=== INICIANDO PIPELINE DE DADOS ===")
    
    try:
        # Etapa 1: Ingestão (Leitura)
        df_bruto = load_raw_xls(input_file)
        
        # Etapa 2: Limpeza (Tratamento de vazios, mesclas e tipos)
        df_limpo = clean_data(df_bruto)
        
        # Etapa 3: Modelagem (Criação do Star Schema com os metadados)
        star_schema = build_star_schema(df_limpo, metadados)
        
        # Etapa 4: Carga / Salvamento (Exportando para CSV na pasta processed)
        logger.info("Salvando tabelas do modelo dimensional...")
        for table_name, df in star_schema.items():
            output_path = output_dir / f"{table_name}.csv"
            
            # Modo 'a' (append) se você quiser ir somando vários simulados no mesmo arquivo no futuro
            # Por enquanto, vamos sobrescrever ('w') para facilitar os testes
            df.to_csv(output_path, index=False)
            logger.info(f"Arquivo salvo: {output_path} | Shape: {df.shape}")
            
        logger.info("=== PIPELINE CONCLUÍDO COM SUCESSO ===")
        
    except Exception as e:
        logger.error(f"Erro na execução do pipeline: {e}", exc_info=True)

if __name__ == "__main__":
    # ---------------------------------------------------------
    # CONFIGURAÇÃO DA RODADA ATUAL
    # ---------------------------------------------------------
    
    # 1. Defina o caminho relativo do arquivo bruto
    ARQUIVO_ATUAL = "data/raw/exemplo.xls"
    
    # 2. Defina os metadados que explicam o que é este arquivo
    METADADOS_ATUAIS = {
        'nome_avaliacao': 'SML UFSC',
        'etapa': 'PARTE 01',
        'foco': 'UFSC',
        'bimestre': '2º BIMESTRE',
        'ano_letivo': 2023,
        'data_processamento': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Executa o pipeline
    run_pipeline(ARQUIVO_ATUAL, METADADOS_ATUAIS)