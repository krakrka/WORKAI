import os
from pathlib import Path

# On verrouille l'environnement de travail strictement sur le dossier workspace
WORKSPACE_DIR = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../workspace")))

def _get_safe_path(file_path: str) -> Path:
    """Vérifie que le chemin demandé reste confiné dans le dossier workspace."""
    # Création du dossier workspace s'il n'existe pas encore
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
    
    target_path = (WORKSPACE_DIR / file_path).resolve()
    
    # Vérification de sécurité (Air-gap logiciel)
    if WORKSPACE_DIR not in target_path.parents and target_path != WORKSPACE_DIR:
        raise PermissionError(f"Alerte Sécurité : Tentative d'accès hors du workspace ({file_path})")
    
    return target_path

def write_code_to_file(file_name: str, content: str) -> str:
    """Écrit du code généré par l'IA dans un fichier du workspace."""
    try:
        target_path = _get_safe_path(file_name)
        
        # Crée les sous-dossiers si nécessaire (ex: src/app/main.py)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Succès : Fichier {file_name} créé/modifié avec succès."
    except Exception as e:
        return f"Erreur lors de l'écriture : {str(e)}"

def read_file_content(file_name: str) -> str:
    """Permet à l'IA de relire un fichier existant."""
    try:
        target_path = _get_safe_path(file_name)
        if not target_path.exists():
            return f"Erreur : Le fichier {file_name} n'existe pas."
            
        with open(target_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Erreur lors de la lecture : {str(e)}"

def list_project_files(directory_path: str = ".") -> str:
    """Liste l'arborescence actuelle pour que l'IA sache où elle en est."""
    try:
        target_path = _get_safe_path(directory_path)
        files = []
        for path in target_path.rglob("*"):
            if path.is_file():
                # Retourne le chemin relatif par rapport au workspace
                files.append(str(path.relative_to(WORKSPACE_DIR)))
        
        if not files:
            return "Le dossier de travail est vide."
        return "Fichiers présents :\n" + "\n".join(files)
    except Exception as e:
        return f"Erreur lors du listage : {str(e)}"