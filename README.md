**Introduction**

In this post, we’ll walk through the process of deploying a simple containerized Flask application to Google Kubernetes Engine (GKE). The deployment pipeline is fully automated using Jenkins CI/CD, and we'll use Docker to containerize the Flask app. Additionally, we'll set up the necessary infrastructure on Google Cloud using Terraform, making the process both efficient and scalable.

**Tech Stack & Tools Used**

**Flask:** Python-based web framework
**Docker:** Containerization for easy deployment
**Terraform:** Infrastructure-as-code for managing GCP resources
**Jenkins:** CI/CD automation for testing, building, and deploying the app
**Google Cloud Platform (GCP):** Hosting and orchestration of services via GKE

**Step 1: Setting Up the Flask Application**
We start by creating a basic Flask app (app.py) that serves a home page and provides a foundation for our Docker container.

**Step 2: Dockerizing the Application**
The next step is to containerize our Flask application using Docker. 

**Step 3: Setting Up Infrastructure with Terraform**
With Terraform, we define the infrastructure required to run our Flask app on GKE. 

**Step 4: Automating the CI/CD Pipeline with Jenkins**
We automate the entire build and deployment process using Jenkins. The pipeline ensures that our app is tested, built, and deployed with every change made. Here's an overview of the stages:

Checkout: Pull the latest code from the repository.
Setup Python Environment: Create a virtual environment and install dependencies.
Run Tests: Ensure the app behaves as expected with tests.
Terraform Init & Plan: Initialize and plan the infrastructure with Terraform.
Build and Push Docker Image: Build the Docker image and push it to Artifact Registry.
Deploy to GKE: Deploy the app to GKE using Kubernetes manifests.

**Step 5: Deploying to GKE**
Once the Docker image is pushed to Artifact Registry, it’s time to deploy to GKE. We use Kubernetes deployment and service files (deployment.yaml and service.yaml) to define how our app should be deployed and accessed.

**Step 6: Accessing the Application**
After deploying the app, it will be accessible through the LoadBalancer service, making it available via a public IP. This allows anyone to access your app via the web.

**Conclusion**
By combining Flask, Docker, Jenkins, Terraform, and GKE, we’ve built an automated, scalable, and efficient deployment pipeline. This workflow can be extended to more complex applications, ensuring that your app is deployed quickly and consistently.
