Technologies Used
* FastAPI
* UviCorn
* Postgresql
* pydantic
* docker 
* dockerhub & Github

Pipeline Design

The CI/CD pipeline was designed using **GitHub Actions** to automate the entire software delivery process. It consists of five key stages, ensuring reliability, security, and automation throughout the lifecycle.

1. Build & Install
   This stage sets up the environment, installs dependencies, and prepares the FastAPI application for further validation.

2. Lint / Security Scan
   Code quality and security are verified using linting tools and vulnerability scanners. This ensures that the codebase adheres to best practices and remains secure.

3. Test (with Database)
   The pipeline runs automated tests using **pytest**, with a temporary PostgreSQL service spun up in the CI environment. This validates both the API logic and the database connection.

4. Build Docker Image
   Once tests pass, a production-ready Docker image is built using a multi-stage Dockerfile. This image encapsulates the application and its dependencies for consistent deployment.

5. Deploy
   Deployment is triggered only if the branch is `main` and all previous stages succeed. The Docker image is pushed to **Docker Hub** using GitHub Secrets for authentication, ensuring secure and automated delivery.

Secret Management Strategy
We used docker username and docker personal access token as secrets. 

Testing Process
Tested database connection and health, using pytest. 

Lessons Learned 
* Using Containerization and interacting with docker. 
* Integrating yml files to automate complex tasks
* in the ci/cd devops pipeline, interacting with database was a key learning. 
* Using latest versions of dependencies to avoid cross-technology issues. 
