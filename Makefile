KIND_CLUSTER_NAME ?= data-space
KIND_CONFIG        ?= infra/kind/cluster-config.yaml
HELMFILE_DIR       ?= infra/helmfile

.PHONY: cluster-up cluster-down deploy demo-compute demo-fedlearn clean

# Create a kind cluster using the provided configuration
cluster-up:
	@echo "Creating kind cluster $(KIND_CLUSTER_NAME)..."
	kind create cluster --name $(KIND_CLUSTER_NAME) --config $(KIND_CONFIG)

# Delete the kind cluster
cluster-down:
	@echo "Deleting kind cluster $(KIND_CLUSTER_NAME)..."
	kind delete cluster --name $(KIND_CLUSTER_NAME)

# Deploy charts using helmfile
deploy:
	@echo "Deploying services via helmfile..."
	cd $(HELMFILE_DIR) && helmfile -e dev apply

# Demonstration: compute-to-data placeholder
demo-compute:
	@echo "\n=== Compute-to-Data Demo ==="
	@echo "This target illustrates how to run a compute‑to‑data job on your data space."
	@echo "1. Ensure your connectors are running (make deploy)."
	@echo "2. Register your dataset via the self‑description (see self_descriptions/example_dataset.json)."
	@echo "3. Register a consumer algorithm and issue a contract based on policies/example_policy.json."
	@echo "4. Use a compute‑to‑data engine (e.g. Ocean Protocol’s provider/consumer CLI) to execute the algorithm near the data."
	@echo "5. Inspect logs and results to verify that the data never leaves the provider."

# Demonstration: federated learning placeholder
demo-fedlearn:
	@echo "\n=== Federated Learning Demo ==="
	@echo "This target illustrates how to orchestrate a federated learning job across your participants."
	@echo "1. Ensure your connectors are running (make deploy)."
	@echo "2. Prepare a Python environment with a federated learning framework (e.g. Flower or FedML)."
	@echo "3. Write a simple model and training script that trains locally on each participant’s data."
	@echo "4. Use the orchestrator to send the training job to each participant via the connectors."
	@echo "5. Aggregate the model updates and evaluate the global model."

clean: cluster-down
	@echo "Repository cleaned."
