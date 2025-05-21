from typing import Dict, List
import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import os
from flytekit import task, workflow, Resources
from flytekit.types.file import FlyteFile
from flytekit.types.directory import FlyteDirectory

@task(requests=Resources(cpu="1", mem="1Gi"))
def train_model() -> Dict[str, FlyteFile]:
    """
    Train a simple text classification model using 20 newsgroups dataset.
    Returns the model and vectorizer files.
    """
    # Load data
    categories = ['alt.atheism', 'soc.religion.christian']
    newsgroups = fetch_20newsgroups(subset='train', categories=categories)
    
    # Create TF-IDF features
    vectorizer = TfidfVectorizer(max_features=1000)
    X = vectorizer.fit_transform(newsgroups.data)
    y = newsgroups.target
    
    # Train model
    model = LogisticRegression()
    model.fit(X, y)
    
    # Save model and vectorizer
    model_path = "model.joblib"
    vectorizer_path = "vectorizer.joblib"
    
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    
    return {
        "model": FlyteFile(model_path),
        "vectorizer": FlyteFile(vectorizer_path)
    }

@task(requests=Resources(cpu="1", mem="1Gi"))
def create_kserve_manifest(model_file: FlyteFile, vectorizer_file: FlyteFile) -> FlyteFile:
    """
    Create a KServe inference service manifest for the model.
    """
    manifest = f"""apiVersion: "serving.kserve.io/v1beta1"
kind: "InferenceService"
metadata:
  name: "text-classifier"
spec:
  predictor:
    sklearn:
      storageUri: "s3://your-bucket/models/text-classifier"
      resources:
        requests:
          cpu: "1"
          memory: "1Gi"
        limits:
          cpu: "1"
          memory: "1Gi"
"""
    
    manifest_path = "kserve-manifest.yaml"
    with open(manifest_path, "w") as f:
        f.write(manifest)
    
    return FlyteFile(manifest_path)

@task(requests=Resources(cpu="1", mem="1Gi"))
def deploy_model(manifest: FlyteFile) -> str:
    """
    Deploy the model using KServe.
    In a real scenario, this would use kubectl to apply the manifest.
    """
    # In a real scenario, this would be:
    # subprocess.run(["kubectl", "apply", "-f", manifest.path])
    return "Model deployed successfully to KServe"

@workflow
def model_deployment_wf() -> str:
    """
    Workflow to train and deploy a text classification model using KServe.
    """
    # Train the model
    model_files = train_model()
    
    # Create KServe manifest
    manifest = create_kserve_manifest(
        model_file=model_files["model"],
        vectorizer_file=model_files["vectorizer"]
    )
    
    # Deploy the model
    deployment_status = deploy_model(manifest=manifest)
    
    return deployment_status

if __name__ == "__main__":
    print(model_deployment_wf()) 