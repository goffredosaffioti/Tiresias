import numpy as np
import flwr as fl

# ----- dataset sintetico condiviso -----
def make_data(n=200, d=5, noise=0.1, seed=42):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, d))
    w_true = rng.normal(size=(d,))
    y = X @ w_true + noise * rng.normal(size=n)
    return X, y, w_true

X, y, w_true = make_data(n=1000, d=8)
NUM_CLIENTS = 5
splits = np.array_split(np.arange(len(X)), NUM_CLIENTS)

# ----- modello lineare + SGD -----
def init_weights(d):
    return np.zeros(d, dtype=np.float64)

def predict(X, w):
    return X @ w

def loss(X, y, w):
    err = predict(X, w) - y
    return 0.5 * np.mean(err**2)

def sgd(X, y, w, lr=0.05, epochs=3, batch=64, seed=0):
    rng = np.random.default_rng(seed)
    n = len(X)
    for _ in range(epochs):
        idx = rng.permutation(n)
        for i in range(0, n, batch):
            j = idx[i:i+batch]
            grad = X[j].T @ (X[j] @ w - y[j]) / len(j)
            w -= lr * grad
    return w

# ----- client FL -----
class NumpyClient(fl.client.NumPyClient):
    def __init__(self, X, y):
        self.X, self.y = X, y
        self.w = init_weights(self.X.shape[1])

    def get_parameters(self, config):
        return [self.w]

    def fit(self, parameters, config):
        (self.w,) = parameters
        self.w = sgd(self.X, self.y, self.w, lr=0.05, epochs=3, batch=64)
        return [self.w], len(self.X), {}

    def evaluate(self, parameters, config):
        (self.w,) = parameters
        l = loss(self.X, self.y, self.w)
        return float(l), len(self.X), {"mse": float(l)}

def client_fn(cid: str):
    idx = splits[int(cid)]
    return NumpyClient(X[idx], y[idx])

# ----- avvio simulazione -----
if __name__ == "__main__":
    strategy = fl.server.strategy.FedAvg(
        fraction_fit=1.0, fraction_evaluate=1.0, min_fit_clients=NUM_CLIENTS,
        min_evaluate_clients=NUM_CLIENTS, min_available_clients=NUM_CLIENTS
    )
    hist = fl.simulation.start_simulation(
        client_fn=client_fn,
        num_clients=NUM_CLIENTS,
        config=fl.server.ServerConfig(num_rounds=10),
        strategy=strategy,
    )
    # Valutazione MSE su tutto il dataset:
    w = hist.metrics_centralized["parameters"][-1][0] if "parameters" in hist.metrics_centralized else None
    if w is not None:
        mse = loss(X, y, w)
        print(f"\nFinal MSE (global model): {mse:.6f}  |  True w L2: {np.linalg.norm(w - w_true):.4f}")
    print("Done.")
