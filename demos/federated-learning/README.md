# Federated Learning demo (Flower, NumPy only)

Esegue una simulazione Federated Averaging con 5 client NumPy su dati sintetici.
Non richiede PyTorch/TensorFlow. Avvio:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r demos/federated-learning/requirements.txt
make demo-fedlearn
