from crewai import Agent
from langchain_community.chat_models import ChatOllama
from src.config import config

class CEOAgent:
    @staticmethod
    def create() -> Agent:
        # On peut potentiellement utiliser un modèle plus "intelligent" pour le CEO
        llm_ceo = ChatOllama(
            base_url=config.OLLAMA_BASE_URL,
            model=config.CEO_MODEL_NAME
        )
        
        return Agent(
            role="Chief Executive Officer (CEO) & Tech Lead",
            goal="Analyser la demande du Super Admin, structurer le projet, et superviser sa réalisation parfaite.",
            backstory="Tu es le chef de WorkAI. Tu reçois les demandes des clients. Tu ne codes pas toi-même. Tu découpes le problème en tâches simples pour tes ingénieurs et tu valides le résultat final.",
            verbose=True,
            allow_delegation=True, # Indispensable, il dirige l'équipe
            llm=llm_ceo
        )