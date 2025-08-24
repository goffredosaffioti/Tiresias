SHELL := /bin/bash

KIND_CLUSTER := tiresias
KIND_CONFIG  := infra/kind/cluster-config.yaml
HELMFILE     := infra/helmfile/helmfile.yaml

.PHONY: cluster-up cluster-down deploy destroy refresh demo-fedlearn demo-compute

cluster-up:
	kind create cluster --name $(KIND_CLUSTER) --config $(KIND_CONFIG)
	kubectl cluster-info

cluster-down:
	kind delete cluster --name $(KIND_CLUSTER)

deploy:
	helmfile -f $(HELMFILE) apply

destroy:
	helmfile -f $(HELMFILE) destroy || true

refresh: destroy cluster-down cluster-up deploy

demo-fedlearn:
	python3 demos/federated-learning/run_local.py

demo-compute:
	@echo "TODO: vedi demos/compute-to-data/README.md"
