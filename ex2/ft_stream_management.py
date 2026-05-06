import sys
from typing import IO


def main() -> None:
    if not len(sys.argv) == 2:
        print("[STDERR] Usage: ft_ancient_text.py <file>", file=sys.stderr)
        return
    
    else:
        f = None
        try:
            print("=== Cyber Archives Recovery ===")
            print(f"Accessing file '{sys.argv[1]}'...")
            print("---\n")
            f = open(sys.argv[1])
            file_content = f.read()
            print(file_content)
        except FileNotFoundError as e:
            print(f"[STDERR] Error opening file '{sys.argv[1]}': {e}", file=sys.stderr)
        except PermissionError as e:
            print(f"[STDERR] Error opening file '{sys.argv[1]}': {e}", file=sys.stderr)
        except IsADirectoryError as e:
            print(f"[STDERR] Error opening file '{sys.argv[1]}': {e}", file=sys.stderr)
        except UnicodeDecodeError as e:
            print(f"[STDERR] Error opening file '{sys.argv[1]}': {e}", file=sys.stderr)
        except OSError as e:
            print(f"[STDERR] Error opening file '{sys.argv[1]}': {e}", file=sys.stderr)
        finally:
            if f:
                f.close()
                print("\n---")
                print(f"File '{sys.argv[1]}' closed.\n")


        print("Transforming data...")
        print("---\n")
        line = ""
        modified_content = ""
        for c in file_content:
            if c == "\n":
                if line:
                    print(line + "#")
                    modified_content += line + "#" + "\n"
                line = ""
            else:
                line += c
        if line:
            print(line + "#")
            modified_content += line + "#" + "\n"
        print("\n---")


if __name__ == "__main__":
    main()
