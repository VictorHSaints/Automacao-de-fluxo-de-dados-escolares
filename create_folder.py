# create_project.py
import os
from pathlib import Path

def create_structure():
    """Cria a estrutura base de diretórios e arquivos do projeto."""
    
    base_dir = Path("escolar_pipeline")
    
    # Definindo os diretórios
    directories = [
        "config",
        "data/raw",
        "data/processed",
        "data/outputs",
        "src/ingestion",
        "src/cleaning",
        "src/modeling",
        "src/analytics",
        "src/app",
        "src/export",
        "src/utils"
    ]
    
    # Criando os diretórios
    for d in directories:
        dir_path = base_dir / d
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"Diretório criado: {dir_path}")
        
        # Criar __init__.py em pacotes Python
        if d.startswith("src") or d == "config":
            init_file = dir_path / "__init__.py"
            init_file.touch()

    # Criar um .gitignore básico
    gitignore_path = base_dir / ".gitignore"
    with open(gitignore_path, "w") as f:
        f.write("data/\n__pycache__/\n*.pyc\n.env\n.venv/\n")
    print(f"Arquivo criado: {gitignore_path}")

if __name__ == "__main__":
    create_structure()
    print("Estrutura do projeto criada com sucesso!")