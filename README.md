# Flyte Hello World Example

This repository contains two Flyte workflows:
1. A simple hello world example
2. A model deployment example using KServe

## 1. Run Locally with Flytekit Only

This runs the workflow as a regular Python script, using only Flytekit (no backend).

### Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install flytekit scikit-learn joblib
```

### Run Hello World
```bash
pyflyte run workflows/hello_world.py hello_wf --name="World"
```

### Run Model Deployment
```bash
pyflyte run workflows/model_deployment.py model_deployment_wf
```

---

## 2. Run with Flyte Sandbox (Docker)

This runs a full Flyte backend in a Docker container. **Recommended: use Docker, not Podman.**

### Setup
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Ensure Docker is running
- Use the provided `docker-compose.yml`:

```bash
docker-compose up -d
```

### Register and Run the Workflow
```bash
source venv/bin/activate
pyflyte register workflows
```

- Visit the Flyte Console at [http://localhost:30081](http://localhost:30081)
- Or trigger a run via CLI:
```bash
# Run hello world
pyflyte run --remote workflows/hello_world.py hello_wf --name="World"

# Run model deployment
pyflyte run --remote workflows/model_deployment.py model_deployment_wf
```

### Troubleshooting
- If you see errors about Docker permissions or services not starting, try restarting Docker Desktop.
- Podman is not fully supported for the Flyte sandbox.

---

## 3. Run with Flyte Demo Cluster (`flytectl`)

This is the easiest way to get a local Flyte cluster for development.

### Setup
- Install [flytectl](https://docs.flyte.org/en/latest/getting_started/flytectl_install.html)

### Start the Demo Cluster
```bash
flytectl demo start
```

### Register and Run the Workflow
```bash
source venv/bin/activate
pyflyte register workflows
pyflyte run --remote workflows/hello_world.py hello_wf --name="World"
```

- Visit the Flyte Console at [http://localhost:30081](http://localhost:30081)

### Troubleshooting
- If you see connection errors, ensure the demo cluster is running and ports are not blocked.
- Stop the cluster with:
```bash
flytectl demo stop
```

---

## Model Deployment Workflow

The `model_deployment.py` workflow demonstrates how to:
1. Train a simple text classification model using scikit-learn
2. Create a KServe manifest for model deployment
3. Deploy the model to a KServe cluster

### Prerequisites
- A Kubernetes cluster with KServe installed
- S3 or similar storage for model artifacts
- kubectl configured to access your cluster

### Configuration
Before running the workflow, update the following in `model_deployment.py`:
- S3 bucket path in the KServe manifest
- Resource requirements for model training and serving
- Kubernetes cluster configuration

### Running the Workflow
```bash
# Local execution
pyflyte run workflows/model_deployment.py model_deployment_wf

# Remote execution
pyflyte run --remote workflows/model_deployment.py model_deployment_wf
```

---

## File Structure
- `workflows/hello_world.py`: The hello world workflow definition
- `workflows/model_deployment.py`: The model deployment workflow
- `docker-compose.yml`: For running the Flyte sandbox with Docker
- `flyte.config`: Flyte configuration file

---

## References
- [Flyte Documentation](https://docs.flyte.org/)
- [Flytekit](https://docs.flyte.org/projects/flytekit/en/latest/)
- [Flytectl](https://docs.flyte.org/projects/flytectl/en/latest/)
- [KServe Documentation](https://kserve.github.io/website/)
