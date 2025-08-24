import numpy as np
import flwr as fl

# Synthetic dataset generation
def make_data(n=1000, d=8, noise=0.1, seed=42):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, d))
    w_true = rng.normal(size=(d,))
    y = X @ w_true + noise * rng.normal(size=n)
    return X, y, w_true

X, y, w_true = make_data()
NUM_CLIENTS = 5
splits = np.array_split(np.arange(len(X)), NUM_CLIENTS)

def init_weights(d):
    return np.zeros(d, dtype=np.float64)

def predict(X, w):
    return X @ w

def loss(X, y, w):
    return 0.5 * np.mean((predict(X, w) - y)**2)

def sgd(X, y, w, lr=0.05, epochs=3, batch=64, seed=0):
    rng, n = np.random.default_rng(seed), len(X)
    for _ in range(epochs):
        idx = rng.permutation(n)
        for i in range(0, n, batch):
            j = idx[i:i+batch]
            grad = X[j].T @ (X[j] @ w - y[j]) / len(j)
            w -= lr * grad
    return w

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

if __name__ == "__main__":
    strategy = fl.server.strategy.FedAvg(
        fraction_fit=1.0,
        fraction_evaluate=1.0,
        min_fit_clients=NUM_CLIENTS,
        min_evaluate_clients=NUM_CLIENTS,
        min_available_clients=NUM_CLIENTS
    )
    fl.simulation.start_simulation(
        client_fn=client_fn,
        num_clients=NUM_CLIENTS,
        config=fl.server.ServerConfig(num_rounds=10),
        strategy=strategy,
    )
    print("Done.")