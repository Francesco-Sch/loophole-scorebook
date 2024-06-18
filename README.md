![Graphic – Loophole Scorebook](./.github/header_loophole-scorebook.jpg)

# The Loophole Scorebook

The Loophole Scorebook is designed to assist artists in exploring and expanding upon ideas that reside in the grey areas of a given ruleset. Users can upload a document that outlines specific rules or constraints, and the AI model will analyze these inputs to identify potential loopholes or unconventional interpretations. Based on these findings, the tool generates creative concepts and suggestions that artists can use to develop unique and innovative works of art. This process aims to inspire artists to push boundaries and think outside the box, ultimately enhancing their creative output.

## 📝 Colophon

- Frontend
  - Build with [Nuxt 3](https://nuxt.com/), a meta-framework for [Vue 3](https://vuejs.org/)
  - Made beautiful with [Nuxt UI](https://ui.nuxt.com/) and [Tailwind CSS](https://tailwindcss.com/)
  - Using [Pinia](https://pinia.vuejs.org/) for cross-component memory
- Backend
  - LLM pipeline powered by [🦜️🔗 LangChain](https://python.langchain.com/v0.2/docs/introduction/)
  - Served through [🦜️🏓 LangServe](https://python.langchain.com/v0.2/docs/langserve/)
  - Inference done with [Ollama](https://ollama.com/)
  - Knowledge saved in [Qdrant](https://qdrant.tech/)

## 🚧 Development

Docker must be installed and running to start the development setup. Instructions on how to install Docker for your OS can be found [here](https://docs.docker.com/desktop/install/mac-install/).

### Set environment variables

To be able to start the development environment, you need to set some environment variables first. To do this, copy `.env.example` to `.env` and add the variables as appropriate.

```zsh
cp .env.example .env
```

A good default for the environment variables is:

```env
QDRANT_URL="http://database:6333"
QDRANT_COLLECTION="loophole"

OLLAMA_URL="http://inference:11000"
OLLAMA_MODEL="llama3"
```

### Start the development setup

To start the development setup run:

```zsh
docker compose -f docker-compose.dev.yml up -d
```

This starts

- the frontend (Nuxt) on http://localhost:3000
- the backend (LangChain via Langserve) on http://localhost:8080
- the vector database (Qdrant) on http://localhost:6333
- the inference server (Ollama) on http://localhost:11000

> CAUTION! Pulling the model could take some time. Until the pull of the model is not completed the app is not working.

All containers are running with HMR (Hot Module Replacement). Should a manual rebuild be neccessary use the following command:

```zsh
docker compose -f docker-compose.dev.yml up -d --build
```

To rebuild only a specific container run:

```zsh
docker compose -f docker-compose.dev.yml up -d --build frontend
```

To stop and remove the containers run:

```zsh
docker compose down
```

## 🐳 Deploy with Docker

Starting the app for production is similar to the development setup.
Set up the environment variables as described above and then run the following command:

```zsh
docker compose up -d
```

This will start the containers in a minified, production-ready mode.

To stop and remove the containers run:

```zsh
docker compose down
```
