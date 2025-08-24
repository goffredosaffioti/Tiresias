# Federated Learning Demo (Flower + NumPy)

This demo illustrates how to run a simple federated averaging (FedAvg) training loop across multiple clients using the [Flower](https://flower.dev/) framework and NumPy.

The script generates a synthetic linear regression dataset and splits it evenly across five clients. Each client performs local stochastic gradient descent (SGD) on its own data. The Flower simulator orchestrates ten rounds of training by averaging model parameters across clients.

## Running the demo

1. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Start the local simulation via the top‑level Makefile:

   ```bash
   make demo-fedlearn
   ```

You should see the global loss decrease over the rounds, demonstrating that federated learning can converge without exchanging raw data.