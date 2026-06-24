import logging
import sys

def get_logger(name: str) -> logging.Logger:
    """
    Retorna uma instância de logger configurada.
    
    Args:
        name (str): Nome do módulo chamador.
        
    Returns:
        logging.Logger: Instância do logger.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger