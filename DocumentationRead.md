# Pizza Delivery API — DevOps Pipeline Project

Overview

Our assigned lab mid of the techstack fastapi and postgressql  demonstrates a complete DevOps pipeline implementation on an existing open-source Pizza Delivery API application. 

## Step 1 – Project Setup

The original open-source Pizza Delivery API was cloned from GitHub and configured locally. Downloaded all dependencies from the given requirements.txt file so that the project can be run locally. 

## Step 2 – Containerization (Docker Compose)

We created a `docker-compose.yml` to containerize both FastAPI and PostgreSQL services.

### docker-compose.yml Overview

app: Runs the FastAPI backend.
db: Runs PostgreSQL database.
networking: Both services communicate internally through Docker’s bridge network.
volumes: Persistent storage for the database data.

To start containers:
docker-compose up --build

## Step 3 – CI/CD Pipeline ()

The pipeline (`.github/workflows/ci/cd.yml`) automates the build, test, and deployment process.

### Pipeline Stages

Installs dependencies and sets up environment.

 Test (with Database)
   * Spins up a PostgreSQL service inside the CI environment.
   * Runs API tests via `pytest`.

Build Docker Image
   * Builds the production Docker image using a multi-stage Dockerfile for optimization.

Deploy 
   * Automatically pushes the image to Docker Hub if all tests pass and the branch is `main`.

---
