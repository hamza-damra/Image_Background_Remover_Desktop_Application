"""Test rembg import"""
import sys
print("Python version:", sys.version)
print("\n1. Testing basic imports...")

try:
    import numpy as np
    print("✓ numpy imported")
except Exception as e:
    print(f"✗ numpy failed: {e}")

try:
    from PIL import Image
    print("✓ PIL imported")
except Exception as e:
    print(f"✗ PIL failed: {e}")

print("\n2. Testing rembg import...")
try:
    print("Attempting to import rembg...")
    from rembg import remove
    print("✓ rembg imported successfully!")
except Exception as e:
    print(f"✗ rembg failed: {e}")
    import traceback
    traceback.print_exc()

print("\nTest complete.")
