# On part d'une image officielle Microsoft optimisée pour Python dans Codespaces
FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

# On s'assure que le système est à jour
RUN apt-get update && apt-get install -y \
    curl \
    git \
    htop \
    && rm -rf /var/lib/apt/lists/*