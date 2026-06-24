import pandas as pd
from pathlib import Path
from src.utils.logger import get_logger

logger = get_logger(__name__)

def generate_student_report(student_id: str, metrics: pd.DataFrame, output_dir: Path) -> None:
    """
    Gera um relatório em PDF individual para o aluno.
    
    Args:
        student_id (str): Identificador do aluno.
        metrics (pd.DataFrame): DataFrame com as métricas já calculadas.
        output_dir (Path): Diretório onde o PDF será salvo.
    """
    logger.info(f"Gerando relatório PDF para o aluno {student_id}")
    # TODO: Implementar integração com biblioteca de PDF (ex: ReportLab, FPDF ou WeasyPrint)
    pass