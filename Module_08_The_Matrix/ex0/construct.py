import sys
import os
import site


def in_venv() -> bool:
    return sys.prefix != sys.base_prefix


def main() -> None:
    venv = os.environ.get("VIRTUAL_ENV")

    if in_venv():
        print("\nMATRIX STATUS: Welcome to the construct\n")
    else:
        print("\nMATRIX STATUS: Still plugged in\n")

    print(f"Current Python: {sys.executable}")
    if in_venv():
        print(f"Virtual environment: {os.path.basename(venv)}")
        print(f"Environment path: {venv}")
    else:
        print("Virtual Environment: None detected")

    if in_venv():
        print("\nSUCCESS: You're in an isolated environment!")
        print("Safe to install packages without affecting the global system.\n")
        print("Package installation path:")
        print(f"{site.getsitepackages()[0]}")
    else:
        print("\nWARNING: You're in the global environment!")
        print("The machines can see everything you install.\n")
        print("To enter the construct, run:")
        print("python -m venv matrix_env")
        print("source matrix_env/bin/activate # On Unix")
        print("matrix_env\\Scripts\\activate # On Windows\n")
        print("Then run this program again.")


if __name__ == "__main__":
    main()
