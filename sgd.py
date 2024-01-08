# Implementation of linear regression optimized with
# stochastic gradient descent from scratch.

import numpy as np
import torch


def fit_linear_regression_w_sgd(
    x_train: torch.tensor,
    y_train: torch.tensor,
    w_guess: torch.tensor,
    b_guess: torch.tensor,
    num_iterations: int = 100,
    batch_size: int = 64,
    learning_rate: float = 0.01,
) -> (torch.tensor, torch.tensor):
    w = w_guess
    b = b_guess

    for i in range(num_iterations):
        mask = np.random.choice(x_train.shape[0], batch_size, replace=False)
        x, y = x_train[mask], y_train[mask].unsqueeze(1)
        y_pred = torch.mm(x, w.transpose(0, 1)) + b
        loss = 1 / (2 * len(x)) * sum((y - y_pred) ** 2)

        # calculate gradients for each weight and take a step
        for idx in range(len(w[0])):
            xi = x[:, idx : idx + 1]
            d_xi = 1 / (len(x)) * torch.mm(-xi.transpose(0, 1), y - y_pred)
            w[0][idx] -= learning_rate * d_xi[0][0]

        # calculate gradient for bias and take a step
        b[0][0] -= learning_rate * -sum(y - y_pred)[0]

        print(f"Iteration {i}: loss: {loss[0]} weights: {w}")

    return w, b


if __name__ == "__main__":
    x_train = torch.tensor(
        [
            [3, 2, 1300],
            [4, 3, 2200],
            [4, 4, 2800],
            [2, 2, 1350],
            [1, 2, 950],
            [5, 4, 3600],
        ],
        dtype=torch.float32,
    )

    y_train = torch.tensor(
        [
            1000000,
            1750000,
            2345000,
            800000,
            600000,
            3151111,
        ],
        dtype=torch.float32,
    )

    solver_weights = [49006.3, 53590.4, 857.1]
    solver_bias = [-442077.4]

    learned_weights, learned_bias = fit_linear_regression_w_sgd(
        x_train,
        y_train,
        w_guess=torch.tensor([[25000, 60000, 500]], dtype=torch.float32),
        b_guess=torch.tensor([[-300000]], dtype=torch.float32),
        num_iterations=100000,
        batch_size=6,
        learning_rate=0.00000039,
    )

    print(f"Learned weights & bias: {learned_weights}, {learned_bias}")
    print(f"Solver weights & bias: {solver_weights}, {solver_bias}")
