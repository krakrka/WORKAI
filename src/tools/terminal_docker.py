import docker
import os
from pathlib import Path

# Chemin absolu vers le workspace pour le montage du volume Docker
WORKSPACE_DIR = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../workspace")))

# Initialisation du client Docker (se connecte au démon Docker de Codespaces)
try:
    client = docker.from_env()
except Exception as e:
    print(f"Attention : Démon Docker introuvable. {e}")
    client = None

def run_code_in_sandbox(script_name: str, language: str = "python") -> str:
    """
    Lance un conteneur éphémère, monte le workspace, exécute le script et s'auto-détruit.
    """
    if not client:
        return "Erreur Fatale : Docker n'est pas actif sur la machine hôte."

    # Définition de l'image Docker selon le langage
    image_map = {
        "python": "python:3.11-slim",
        "javascript": "node:18-alpine",
        "bash": "ubuntu:22.04"
    }
    
    image = image_map.get(language.lower(), "ubuntu:22.04")
    command_map = {
        "python": f"python /app/{script_name}",
        "javascript": f"node /app/{script_name}",
        "bash": f"bash /app/{script_name}"
    }
    
    command = command_map.get(language.lower(), f"cat /app/{script_name}")

    try:
        # Exécution du conteneur en mode détaché strict avec auto-suppression
        print(f"[Sandbox] Démarrage du test pour {script_name}...")
        
        output = client.containers.run(
            image=image,
            command=command,
            volumes={
                str(WORKSPACE_DIR): {'bind': '/app', 'mode': 'ro'} # ro = Read Only (Sécurité max pendant le test)
            },
            working_dir="/app",
            remove=True,        # Détruit le conteneur dès que le script est fini
            network_disabled=True, # Empêche le script de télécharger des malwares
            mem_limit="256m",   # Empêche l'IA de faire planter la RAM
            cpu_quota=50000,    # Limite l'utilisation CPU à 50% d'un cœur
            stderr=True,
            stdout=True
        )
        return f"Exécution réussie. Sortie terminal :\n{output.decode('utf-8')}"
        
    except docker.errors.ContainerError as e:
        # Capture les erreurs de code (ex: SyntaxError) pour que l'IA puisse les corriger
        error_msg = e.stderr.decode('utf-8') if e.stderr else str(e)
        return f"Échec de l'exécution. Rapport d'erreur :\n{error_msg}"
    except docker.errors.ImageNotFound:
        return f"Erreur : L'image Docker {image} n'est pas disponible."
    except Exception as e:
        return f"Erreur inattendue du Sandbox : {str(e)}"