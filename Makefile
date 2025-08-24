SHELL := /bin/bash

# Name of the local kind cluster and configuration
KIND_CLUSTER  := tiresias
KIND_CONFIG   := infra/kind/cluster-config.yaml
HELMFILE      := infra/helmfile/helmfile.yaml

.PHONY: cluster-up cluster-down deploy destroy refresh demo-fedlearn demo-compute

# Create a kind cluster using the provided configuration
cluster-up:
        kind create cluster --name $(KIND_CLUSTER) --config $(KIND_CONFIG)
        kubectl cluster-info

# Delete the kind cluster
cluster-down:
        kind delete cluster --name $(KIND_CLUSTER)

# Deploy charts using helmfile
deploy:
        helmfile -f $(HELMFILE) apply

# Destroy charts and release resources via helmfile
destroy:
        helmfile -f $(HELMFILE) destroy || true

# Recreate the cluster and deploy everything from scratch
refresh: destroy cluster-down cluster-up deploy

# Demonstration: federated learning demo
demo-fedlearn:
        python3 demos/federated-learning/run_local.py

# Demonstration: compute‑to‑data placeholder
demo-compute:
        @echo "TODO: vedi demos/compute-to-data/README.md"

# Shortcut target to clean up the cluster
clean: cluster-down
        @echo "Repository cleaned."
