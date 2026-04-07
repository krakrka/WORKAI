import streamlit as st
import requests
import os
from pathlib import Path

# Configuration de la page
st.set_page_config(page_title="WorkAI | Super Admin", page_icon="⚡", layout="wide")

# --- Configuration des chemins et API ---
API_URL = "http://localhost:8000"
WORKSPACE_DIR = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "../workspace")))

def get_workspace_files():
    """Parcourt le dossier workspace pour afficher l'arborescence en temps réel."""
    if not WORKSPACE_DIR.exists():
        return []
    files = []
    for path in WORKSPACE_DIR.rglob("*"):
        if path.is_file():
            files.append(str(path.relative_to(WORKSPACE_DIR)))
    return files

# --- Interface Principale ---
st.title("⚡ WorkAI - Centre de Commandement")
st.markdown("Interface Super Admin pour le contrôle de l'essaim autonome.")

# Initialisation de l'historique de chat dans la session Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Barre Latérale (Monitoring) ---
with st.sidebar:
    st.header("📁 Fichiers Clients (Workspace)")
    files = get_workspace_files()
    if files:
        for f in files:
            st.code(f, language="text")
    else:
        st.info("Le workspace est vide. En attente de génération...")
        
    st.divider()
    
    st.header("🛡️ Statut Système")
    # Vérification basique de l'API FastAPI
    try:
        res = requests.get(f"{API_URL}/health", timeout=2)
        if res.status_code == 200:
            st.success("API Core : EN LIGNE")
        else:
            st.error("API Core : ERREUR")
    except requests.exceptions.ConnectionError:
        st.error("API Core : HORS LIGNE (Démarrez uvicorn)")

# --- Zone de Chat (Discussion avec le CEO) ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Barre de saisie des ordres ---
if prompt := st.chat_input("Ex: Développe un script d'analyse pour le Nasdaq 100..."):
    
    # 1. Afficher le message de l'Admin
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Envoyer la tâche à l'API WorkAI
    with st.chat_message("assistant"):
        with st.spinner("Le CEO Agent analyse la demande et déploie l'essaim..."):
            try:
                # Appel à notre backend FastAPI
                response = requests.post(
                    f"{API_URL}/task/submit",
                    json={"prompt": prompt, "context_id": "session_1"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    reply = f"**Statut :** {data['status']}\n\n**Message :** {data['message']}\n\n*(Note POC : Ici s'affichera le rapport complet de l'essaim une fois branché sur tasks_router.py)*"
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                else:
                    st.error(f"Erreur API : {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Impossible de contacter le cœur de WorkAI. Vérifie que FastAPI tourne.")