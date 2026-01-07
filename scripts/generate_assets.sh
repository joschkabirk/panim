#!/bin/bash
# Script to run all examples and copy outputs to the assets folder

set -e

echo "Running examples..."
for f in examples/*.py; do
    echo "  Running $f"
    python "$f"
done

echo "Copying outputs to assets folder..."
cp plots/*.gif assets/ 2>/dev/null || true

echo "Done!"
