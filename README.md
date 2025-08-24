# Data Space Platform Skeleton

This repository provides a **skeleton** for building a privacy‑preserving data‑sharing platform that is compliant with the Gaia‑X standards.  It is designed for a two‑person team consisting of a builder/architect and an implementer.  The goal is to make it easy to spin up a local development environment, deploy the core building blocks (identity, catalog, data connectors and orchestration), and run privacy‑preserving analytics such as **compute‑to‑data** and **federated learning**.

## Features

* **Kind‑based Kubernetes cluster:** All components are deployed locally using [kind](https://kind.sigs.k8s.io/), so that you can iterate quickly without a cloud account.
* **Helmfile orchestration:** Helm charts for core services (e.g. Eclipse Dataspace Connector) are managed through a single `helmfile.yaml`.  This allows you to configure versions and values cleanly.
* **Self‑descriptions and policies:** Example JSON artefacts illustrate how to publish resources in a Gaia‑X catalogue and attach usage policies (using ODRL profiles).
* **Demo scripts:** `make demo-compute` and `make demo-fedlearn` provide starting points for experimenting with compute‑to‑data and federated learning flows.  They are currently placeholders—extend them to run your own analytics jobs.

## Getting Started

1. **Install prerequisites:** You need Docker, [`kind`](https://kind.sigs.k8s.io/), [`helm`](https://helm.sh/) and [`helmfile`](https://github.com/helmfile/helmfile) installed locally.
2. **Create the cluster:**

   ```sh
   make cluster-up
   ```

   This creates a three‑node kind cluster using the configuration in `infra/kind/cluster-config.yaml`.

3. **Deploy services:**

   ```sh
   make deploy
   ```

   This uses `helmfile` to install the Eclipse Dataspace Connector (EDC) and its dependencies.  Modify `infra/helmfile/values/edc.yaml` to set image versions, credentials and your wildcard domain (e.g. `*.starktechindistries`).

4. **Publish a dataset:** Edit the JSON file in `self_descriptions/example_dataset.json` to describe your dataset or service.  Use the `policies/example_policy.json` to specify usage conditions.  These artefacts can be ingested by the EDC or other catalogue services.

5. **Run a demonstration job:**

   ```sh
   make demo-compute
   # or
   make demo-fedlearn
   ```

   These targets are placeholders.  They print instructions on how to run a compute‑to‑data job or federated learning job across the connectors.  Extend them with your own scripts (e.g. using [`Flower`](https://flower.dev/) for FL or [Ocean Protocol](https://oceanprotocol.com/) for compute‑to‑data).

## Repository structure

```
template_repo/
├── README.md                # This file
├── Makefile                 # Common tasks for cluster creation, deployment and demos
├── infra/
│   ├── kind/
│   │   └── cluster-config.yaml  # Kind cluster definition (multi‑node)
│   └── helmfile/
│       ├── helmfile.yaml        # Helmfile orchestrating charts
│       └── values/
│           └── edc.yaml         # Values for the EDC chart (domain, credentials, etc.)
├── charts/
│   └── edc/
│       ├── Chart.yaml           # Chart metadata for EDC (simplified)
│       ├── values.yaml          # Default values
│       └── templates/
│           ├── deployment.yaml  # Deployment for EDC control and data planes
│           └── service.yaml     # Service exposing EDC
├── self_descriptions/
│   └── example_dataset.json     # Sample self‑description for a dataset/service
├── policies/
│   └── example_policy.json      # Sample ODRL policy expressing data‑usage conditions
└── contracts/
    └── example_contract.json    # Sample contract for data exchange
```

## Notes

* The charts provided here are **bare‑bones**.  They illustrate how to deploy an EDC instance but do not include production‑ready security settings.  For real deployments you should enable TLS, persistent storage and proper authentication.  See the [Eclipse Dataspace Connector documentation](https://github.com/eclipse-edc/Connector) for full configuration options.
* Gaia‑X compliance requires integration with federation services (identity, catalogue, sovereign data exchange and compliance).  Those services are not included in this skeleton.  You can deploy the official [Gaia‑X Federation Services (GXFS)](https://github.com/Gaia-X-Open-Source-Software/GXFS) charts alongside the EDC.
* The domain `starktechindistries` used in `infra/helmfile/values/edc.yaml` is an example.  Replace it with your own wildcard domain when configuring ingress.
