from crewai import Task, Crew, Process
from src.swarm.ceo_agent import CEOAgent
from src.swarm.agent_factory import AgentFactory

class TaskRouter:
    def __init__(self):
        # 1. Recrutement de l'équipe
        self.ceo = CEOAgent.create()
        self.coder = AgentFactory.create_coder_agent()
        self.tester = AgentFactory.create_tester_agent()

    def run_workai_process(self, user_prompt: str) -> str:
        """Lance l'essaim d'agents sur une demande utilisateur."""
        
        # --- Définition des Tâches ---
        
        task_planning = Task(
            description=f"Analyse cette demande du Super Admin : '{user_prompt}'. Rédige un plan d'action technique clair listant les fichiers à créer.",
            expected_output="Un document texte décrivant l'architecture de la solution et les étapes à suivre.",
            agent=self.ceo
        )
        
        task_coding = Task(
            description="En suivant le plan du CEO, écris le code source. Utilise l'outil 'Ecrire_Fichier' pour sauvegarder le code dans le dossier workspace.",
            expected_output="Les fichiers de code ont été créés et enregistrés sur le disque.",
            agent=self.coder
        )
        
        task_testing = Task(
            description="Exécute les fichiers générés dans l'environnement Docker via l'outil 'Tester_Code_Docker'. Si tu trouves une erreur, demande au codeur de la corriger. Ne valide la tâche que si l'exécution réussit sans erreur.",
            expected_output="Un rapport de test confirmant que le code s'exécute parfaitement dans le sandbox Docker.",
            agent=self.tester
        )
        
        task_review = Task(
            description="Vérifie le rapport de test. Si tout est parfait, rédige un message final pour le Super Admin confirmant que le projet est prêt dans son workspace.",
            expected_output="Un message de synthèse pour le Super Admin.",
            agent=self.ceo
        )

        # --- Création de l'Essaim (Crew) ---
        workai_crew = Crew(
            agents=[self.ceo, self.coder, self.tester],
            tasks=[task_planning, task_coding, task_testing, task_review],
            process=Process.sequential, # Les tâches s'exécutent les unes après les autres
            verbose=True
        )

        # --- Lancement du processus ---
        print(f"🚀 WorkAI Swarm activé pour la requête : {user_prompt}")
        result = workai_crew.kickoff()
        
        return result