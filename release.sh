#!/bin/bash
set -e

echo "Running tests..."
tox -e py

echo "Cleaning previous builds..."
tox -e clean

echo "Building package..."
tox -e build

echo "Build complete. Ready to publish."
