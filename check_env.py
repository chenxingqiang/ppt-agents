import sys
import os

def check_virtual_env():
    """Check if running in a virtual environment."""
    in_venv = sys.prefix != sys.base_prefix
    if not in_venv:
        print("Warning: Not running in a virtual environment!")
        print("Please activate your virtual environment:")
        print("  source .venv/bin/activate  # On Unix/Mac")
        print("  .venv\\Scripts\\activate    # On Windows")
        return False
    return True

if __name__ == "__main__":
    check_virtual_env() 