pipeline {
    agent any
// Define environment variables for consistent configuration

    environment {
        PYTHON_VERSION = '3.x' // Python version to use
        GCP_PROJECT_ID = 'solid-altar-444910-c9' //Google Cloud Project ID
        GCP_REGION = 'us-central1-a' 
        GKE_CLUSTER_NAME = 'gke-cluster-2'
        ARTIFACT_REGISTRY_LOCATION = 'us-central1'
        ARTIFACT_REGISTRY_REPO = 'gabapprepothree'
        ARTIFACT_REGISTRY_HOSTNAME = "${ARTIFACT_REGISTRY_LOCATION}-docker.pkg.dev" //Registry hostname
        TERRAFORM_DIR = 'terraform'  // Directory containing Terraform files
        CREDENTIALS_ID = 'kubernetes'
    }

    stages {
// Stage to checkout source code from version control

        stage('Checkout') {
            steps {
                checkout scm
            }
        }
// Stage to set up Python virtual environment and install dependencies

        stage('Setup Python Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    python3 -m pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest flake8 bandit "safety>=2.3.5"
                '''
            }
        }
//Stage to run automated tests and code quality checks
        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    python3 -m pytest test_app.py
                    python3 -m flake8 . --exclude=venv
                    find . -name "app.py" | xargs bandit || true
                    safety check
                '''
            }
        }
//Terraform infrastructure provisioning stages
        stage('Terraform Init') {
            steps {
                dir('terraform') {
                    sh 'terraform init'
                }
            }
        }
//Plan Terraform infrastructure changes
        stage('Terraform Plan') {
            steps { 
                withCredentials([file(credentialsId: 'gcp-credentials', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    dir('terraform') {
                         sh '''
                               gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                               gcloud config set project ${GCP_PROJECT_ID}
                               terraform plan -out=tfplan
                         '''
                 }
             }
         }
     }
//Apply Terraform infrastructure changes
        stage('Terraform Apply') {
            steps {
                withCredentials([file(credentialsId: 'gcp-credentials', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    dir('terraform') {
                        sh '''
                            gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                            gcloud config set project ${GCP_PROJECT_ID}
                            terraform apply -auto-approve tfplan
                        '''
                }
            }
        }
     }

//Build and push Docker image to Artifact Registry
        stage('Build and Push Docker Image') {
            steps {
                script {
                    sh """
                        # Configure Docker for Artifact Registry
                        gcloud auth configure-docker ${ARTIFACT_REGISTRY_LOCATION}-docker.pkg.dev --quiet
                        
                        # Build Docker image
                        docker build -t ${ARTIFACT_REGISTRY_HOSTNAME}/${GCP_PROJECT_ID}/${ARTIFACT_REGISTRY_REPO}/flask-app:latest .
                        
                        # Push to Artifact Registry
                        docker push ${ARTIFACT_REGISTRY_HOSTNAME}/${GCP_PROJECT_ID}/${ARTIFACT_REGISTRY_REPO}/flask-app:latest
                    """
                }
            }
        }

          stage('Deploy to GKE') {
              steps {
                  withCredentials([file(credentialsId: 'gcp-credentials', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
              sh '''
                  # Authenticate and set project
                  gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                  gcloud config set project ${GCP_PROJECT_ID}

                 # Get cluster credentials with explicit zone
                  gcloud container clusters get-credentials ${GKE_CLUSTER_NAME} --zone us-central1-a --project ${GCP_PROJECT_ID}

                 # Force kubectl configuration
                  echo "export USE_GKE_GCLOUD_AUTH_PLUGIN=True" >> ~/.bashrc
                  source ~/.bashrc

                 # Apply manifests
                  kubectl apply -f kubernetes/deployment.yaml
                  kubectl apply -f kubernetes/service.yaml
                
                 # Verify deployment
                  kubectl get pods
                  kubectl get svc
              '''
            }
        }
    }
    }
//Post-pipeline actions
    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs for details.'
        }
    }
}
