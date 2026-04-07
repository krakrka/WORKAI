import os
from pathlib import Path

class Settings:
    # --- Chemins d'accès absolus (Robustesse multi-environnements) ---
    # Le chemin racine du projet (calcule automatiquement où se trouve ce fichier)
    BASE_DIR = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
    
    WORKSPACE_DIR = BASE_DIR / "workspace"
    CHROMA_DB_DIR = BASE_DIR / "chroma_db"
    
    # --- Configuration de l'Intelligence Artificielle (Ollama) ---
    # L'URL par défaut d'Ollama tournant en tâche de fond dans Codespaces
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    # Noms des modèles à utiliser (à télécharger au préalable via ollama run)
    CEO_MODEL_NAME = os.getenv("CEO_MODEL_NAME", "llama3") # Pour le raisonnement
    CODER_MODEL_NAME = os.getenv("CODER_MODEL_NAME", "llama3") # Peut être remplacé par qwen2.5-coder plus tard
    
    # --- Configuration du Sandbox (Docker) ---
    # Limites pour éviter que l'IA ne fasse planter le Codespace lors des tests
    DOCKER_MAX_MEM = "256m"
    DOCKER_CPU_QUOTA = 50000 # Équivaut à 50% d'un coeur de processeur CPU
    
    # --- Configuration de l'API Interne (FastAPI) ---
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))

    def __init__(self):
        # Création automatique des dossiers critiques s'ils n'existent pas
        self.WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
        self.CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)

# Instanciation globale pour tout le projet
config = Settings()