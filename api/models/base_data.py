
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

num_samples = 10_000

# Helper function to generate persistent changes for certain variables
def generate_persistent_changes(n, change_prob=0.01):
    changes = [False] * n  # Assume no change to start with
    for i in range(1, n):
        if np.random.rand() < change_prob:
            changes[i] = not changes[i-1]  # Change state
        else:
            changes[i] = changes[i-1]  # Remain in the same state
    return changes

# Triggers
triggers = pd.DataFrame({
    'sleep quality': np.random.choice([i for i in range(6, 11)] + [i for i in range(5)], p=[0.15]*5 + [0.05]*5, size=num_samples),
    'sleep duration': np.random.normal(7, 1.5, num_samples).clip(0, 12),
    'stress level': np.random.choice([i for i in range(4, 11)] + [i for i in range(4)], p=[0.12]*7 + [0.04]*4, size=num_samples),
    'alcohol consumption today': np.random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], p=[0.4, 0.15, 0.1, 0.1, 0.05, 0.05, 0.05, 0.025, 0.025, 0.025, 0.025], size=num_samples),
    'caffeine consumption today': np.random.choice(range(5), p=[0.2, 0.3, 0.25, 0.15, 0.1], size=num_samples),
    'drugs consumption today': np.random.choice([True, False], p=[0.05, 0.95], size=num_samples),
    'smoking': np.random.choice(range(21), p=[0.4] + [0.03]*20, size=num_samples),
    'missing a meal': np.random.choice([True, False], p=[0.1, 0.9], size=num_samples),
    'fevers': np.random.choice([True, False], p=[0.02, 0.98], size=num_samples),
    'Steps': np.random.normal(5000, 2500, num_samples).clip(0),
    'High intensity minutes': np.random.normal(30, 15, num_samples).clip(0, 150),
    'flashing light': np.random.choice([True, False], p=[0.1, 0.9], size=num_samples),
    'Monthly periods': np.random.randint(1, 29, num_samples), 
    'Adherence to prescribed medication regimen': generate_persistent_changes(num_samples, 0.02),
    'Changes in medication dosage or type': generate_persistent_changes(num_samples, 0.03),
})

# Prodromes
prodromes = pd.DataFrame({
    'headache': np.random.choice([i for i in range(6, 11)] + [i for i in range(6)], p=[0.14]*5 + [0.05]*6, size=num_samples),
    'numbness or tingling': np.random.choice(range(11), p=[0.7] + [0.03]*10, size=num_samples),
    'tremor': np.random.choice(range(11), p=[0.85] + [0.015]*10, size=num_samples),
    'dizziness': np.random.choice(range(11), p=[0.75] + [0.025]*10, size=num_samples),
    'nausea': np.random.choice(range(11), p=[0.8] + [0.02]*10, size=num_samples),
    'anxiety': np.random.choice([i for i in range(4, 11)] + [i for i in range(4)], p=[0.12]*7 + [(1 - (7 * 0.12))/4]*4, size=num_samples),
    'Mood changes':  np.random.choice([i for i in range(4, 11)] + [i for i in range(4)], p=[0.12]*7 + [(1 - (7 * 0.12))/4]*4, size=num_samples),
    'Insomnia':  np.random.choice([i for i in range(4, 11)] + [i for i in range(4)], p=[0.12]*7 + [(1 - (7 * 0.12))/4]*4, size=num_samples),
    'Difficulty focusing':  np.random.choice([i for i in range(4, 11)] + [i for i in range(4)], p=[0.12]*7 + [(1 - (7 * 0.12))/4]*4, size=num_samples),
    'gastrointestinal disturbances': np.random.choice(range(11), p=[0.85] + [0.015]*10, size=num_samples),
})

# Episodes Occurrences - Assuming episodic occurrence, not daily
episodes_occurrences = pd.DataFrame({
    'Episodes Occurrences': np.random.choice([True, False], p=[0.05, 0.95], size=num_samples),
})

# Combine all datasets into one
fake_dataset = pd.concat([triggers, prodromes, episodes_occurrences], axis=1)

fake_dataset.head()

def get_fake_dataset():
    #fundtion to export the dataset from the file
    return fake_dataset
