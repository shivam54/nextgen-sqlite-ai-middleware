#!/usr/bin/env python3
"""
Generate synthetic training data for SQLite cache ML

"""

import random
import csv
import os

print("Generating synthetic training data for SQLite cache ML...")
print()

# Generate synthetic page access data
output_file = "page_log.csv"

with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['access_count', 'time_since', 'is_dirty', 'has_refs'])
    
    # Generate 10,000 samples with realistic patterns
    print("Generating 10,000 samples...")
    for i in range(10000):
        # Realistic access patterns:
        # - Some pages accessed frequently (hot pages) - keep these
        # - Some pages accessed rarely (cold pages) - evict these
        if random.random() < 0.3:  # 30% hot pages (frequently accessed)
            access_count = random.randint(10, 100)
            time_since = random.randint(0, 1000)  # Recently accessed
        else:  # 70% cold pages (rarely accessed)
            access_count = random.randint(1, 10)
            time_since = random.randint(1000, 10000)  # Older access
        
        is_dirty = random.choice([0, 1])
        has_refs = random.choice([0, 1])
        writer.writerow([access_count, time_since, is_dirty, has_refs])
        
        if (i + 1) % 2000 == 0:
            print(f"  Generated {i + 1} samples...")

print()
print(f"✓ Generated 10,000 synthetic training samples")
print(f"  File: {os.path.abspath(output_file)}")
print()
print("Next step: Train the neural network")
print("  python train_simple_nn.py")

