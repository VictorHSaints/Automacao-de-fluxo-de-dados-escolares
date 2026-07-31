import os
import sys
from pathlib import Path
import pandas as pd

# Garante que o Python encontre a pasta 'src' independentemente de onde o script for chamado
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importando as funções dos módulos estruturados
from src.ingestion.loader import load_raw_xls
from src.cleaning.processor import clean_data
from src.modeling.star_schema import build_star_schema
from src.utils.logger import get_logger

logger = get_logger(__name__)

def run_pipeline(caminho_arquivo: str, metadados: dict):
    """
    Função principal que orquestra a execução do pipeline de dados.
    """
    base_dir = Path(__file__).resolve().parent
    input_file = Path(caminho_arquivo)
    output_dir = base_dir / "data" / "processed"
    
    # Garante que a pasta de saída exista
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info("=== INICIANDO PIPELINE DE DADOS ===")
    
    try:
        # Etapa 1: Ingestão (Leitura do arquivo bruto)
        df_bruto = load_raw_xls(input_file)
        
        # Etapa 2: Limpeza (Tratamento de vazios, mesclas e tipos)
        df_limpo = clean_data(df_bruto)
        
        # EXPORTAÇÃO ADICIONAL: Salva o arquivo apenas limpo para análise visual rápida
        nome_arquivo_limpo = f"{input_file.stem}_limpo.csv"
        caminho_limpo = output_dir / nome_arquivo_limpo
        df_limpo.to_csv(caminho_limpo, index=False)
        logger.info(f"Arquivo limpo (para visualização) salvo em: {caminho_limpo}")
        
        # Etapa 3: Modelagem (Transformação para o modelo Star Schema com metadados)
        star_schema = build_star_schema(df_limpo, metadados)
        
        # Etapa 4: Carga (Salva as tabelas dimensionais separadas)
        logger.info("Salvando tabelas do modelo dimensional...")
        for table_name, df in star_schema.items():
            output_path = output_dir / f"{table_name}.csv"
            df.to_csv(output_path, index=False)
            logger.info(f"Arquivo do esquema salvo: {output_path} | Shape: {df.shape}")
            
        logger.info("=== PIPELINE CONCLUÍDO COM SUCESSO ===")
        
    except Exception as e:
        logger.error(f"Erro na execução do pipeline: {e}", exc_info=True)

def coletar_metadados_interativo() -> dict:
    """Coleta os metadados da avaliação diretamente pelo terminal."""
    print("\n" + "="*50)
    print("📝 CADASTRO DE NOVA AVALIAÇÃO")
    print("="*50)
    
    nome = input("1. Nome da Avaliação (ex: SML UFSC): ")
    etapa = input("2. Etapa/Parte (ex: PARTE 01, DIA 02): ")
    foco = input("3. Foco (ex: UFSC, ENEM, ACAFE): ")
    bimestre = input("4. Bimestre (ex: 1º BIMESTRE, 2º BIMESTRE): ")
    ano = input("5. Ano Letivo (ex: 2024): ")
    
    return {
        'nome_avaliacao': nome.strip().upper(),
        'etapa': etapa.strip().upper(),
        'foco': foco.strip().upper(),
        'bimestre': bimestre.strip().upper(),
        'ano_letivo': ano.strip(),
        'data_processamento': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def selecionar_arquivo_interativo(base_dir: Path) -> Path:
    """Lista os arquivos disponíveis na pasta data/raw para escolha."""
    raw_dir = base_dir / "data" / "raw"
    
    # Busca arquivos suportados (.xls, .xlsx, .csv)
    arquivos = list(raw_dir.glob("*.xls*")) + list(raw_dir.glob("*.csv"))
    
    if not arquivos:
        print(f"\n❌ Nenhum arquivo encontrado na pasta: {raw_dir}")
        print("Adicione os arquivos de notas nessa pasta antes de executar.")
        sys.exit(1)
        
    print("\n" + "="*50)
    print("📂 ARQUIVOS DISPONÍVEIS NA PASTA RAW")
    print("="*50)
    
    for i, arq in enumerate(arquivos):
        print(f"[{i+1}] {arq.name}")
        
    while True:
        try:
            escolha = int(input(f"\nDigite o número do arquivo que deseja processar (1 a {len(arquivos)}): "))
            if 1 <= escolha <= len(arquivos):
                return arquivos[escolha - 1]
            else:
                print(f"❌ Opção inválida. Escolha um número entre 1 e {len(arquivos)}.")
        except ValueError:
            print("❌ Entrada inválida. Digite apenas números.")

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    
    # 1. Menu de seleção de arquivos
    arquivo_selecionado = selecionar_arquivo_interativo(base_dir)
    
    # 2. Menu de entrada de metadados
    metadados = coletar_metadados_interativo()
    
    # 3. Execução do fluxo de dados
    print(f"\n🚀 Processando o arquivo: {arquivo_selecionado.name} ...")
    run_pipeline(str(arquivo_selecionado), metadados)