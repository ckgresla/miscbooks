#!/usr/bin/env python

# Quickstart from WanDB for logging a Net Training Run

import wandb
import random # for demo script

# Need have auth token! (can get @ https://wandb.ai/authorize) 
wandb.login()

# Sample Params for this "run"
epochs=10
lr=0.01

# Initialize the WANDB Connection/Project
run = wandb.init(
    # Set the project where this run will be logged
    project="quickstart_demo",
    # Track hyperparameters and run metadata
    config={
        "learning_rate": lr,
        "epochs": epochs,
    })

offset = random.random() / 5
print(f"lr: {lr}")

# simulating a training run
for epoch in range(2, epochs):
    acc = 1 - 2 ** -epoch - random.random() / epoch - offset
    loss = 2 ** -epoch + random.random() / epoch + offset
    print(f"epoch={epoch}, accuracy={acc}, loss={loss}")
    wandb.log({"accuracy": acc, "loss": loss})

run.log_code()
