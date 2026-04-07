from crewai import Agent
from langchain_community.chat_models import ChatOllama
from langchain.tools import tool
from src.config import config
from src.tools.file_manager import write_code_to_file, read_file_content, list_project_files
from src.tools.terminal_docker import run_code_in_sandbox
from src.tools.web_search import search_documentation

# --- 1. Connexion au Modèle Local (Ollama) ---
llm_coder = ChatOllama(
    base_url=config.OLLAMA_BASE_URL,
    model=config.CODER_MODEL_NAME
)

# --- 2. Enrobage des Outils pour CrewAI ---
@tool("Ecrire_Fichier")
def tool_write_file(file_name: str, content: str) -> str:
    """Utilise cet outil pour écrire ou modifier un fichier de code dans le workspace."""
    return write_code_to_file(file_name, content)

@tool("Lire_Fichier")
def tool_read_file(file_name: str) -> str:
    """Utilise cet outil pour lire le contenu d'un fichier existant."""
    return read_file_content(file_name)

@tool("Lister_Fichiers")
def tool_list_files(directory: str = ".") -> str:
    """Utilise cet outil pour voir quels fichiers existent dans le projet."""
    return list_project_files(directory)

@tool("Tester_Code_Docker")
def tool_run_docker(script_name: str, language: str = "python") -> str:
    """Utilise cet outil pour exécuter un script dans un environnement Docker sécurisé et voir s'il y a des erreurs."""
    return run_code_in_sandbox(script_name, language)

@tool("Recherche_Documentation")
def tool_search_docs(query: str) -> str:
    """Utilise cet outil pour chercher de la documentation technique sur internet."""
    return search_documentation(query)

# --- 3. L'Usine à Agents ---
class AgentFactory:
    @staticmethod
    def create_coder_agent() -> Agent:
        return Agent(
            role="Senior Software Engineer",
            goal="Écrire un code propre, optimisé et sans bug selon les spécifications demandées.",
            backstory="Tu es un développeur expert. Tu écris le code dans des fichiers. Si une erreur est détectée, tu relis le code et tu le corriges.",
            verbose=True,
            allow_delegation=False, # Il ne délègue pas, il code.
            tools=[tool_write_file, tool_read_file, tool_list_files, tool_search_docs],
            llm=llm_coder
        )

    @staticmethod
    def create_tester_agent() -> Agent:
        return Agent(
            role="QA Automation Engineer",
            goal="Tester le code généré par l'ingénieur dans l'environnement Docker et rapporter les erreurs.",
            backstory="Tu es impitoyable avec les bugs. Tu lances les scripts dans le Sandbox Docker. Si le terminal renvoie une erreur, tu exiges que le développeur la corrige.",
            verbose=True,
            allow_delegation=True, # Il peut renvoyer la tâche au codeur
            tools=[tool_run_docker, tool_list_files],
            llm=llm_coder
        )