import sys
from typing import IO


def main() -> None:
    if not len(sys.argv) == 2:
        print("Usage: ft_ancient_text.py <file>")
    
    else:
        f = None
        try:
            print("=== Cyber Archives Recovery ===")
            print(f"Accessing file '{sys.argv[1]}'...")
            f = open(sys.argv[1], "r")
            file_content = f.read()
            print(file_content)
        except FileNotFoundError as e:
            print(f"Error opening file '{sys.argv[1]}': {e}")
        except PermissionError as e:
            print(f"Error opening file '{sys.argv[1]}': {e}")
        except IsADirectoryError as e:
            print(f"Error opening file '{sys.argv[1]}': {e}")
        except UnicodeDecodeError as e:
            print(f"Error opening file '{sys.argv[1]}': {e}")
        except OSError as e:
            print(f"Error opening file '{sys.argv[1]}': {e}")
        finally:
            if f:
                f.close()
                print(f"File '{sys.argv[1]}' closed.")

if __name__ == "__main__":
    main()