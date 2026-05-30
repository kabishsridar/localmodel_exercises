import os
import sys

print("--------------------------------------------------")
print(f"Python Version running inside container: {sys.version}")
print(f"Container Environment Variable (APP_ENV): {os.getenv('APP_ENV', 'Not Set')}")
print("--------------------------------------------------")