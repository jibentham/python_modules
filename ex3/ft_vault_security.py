def secure_archive(file_name: str, operation: int, add_text: str) -> tuple(bool, str):
    if operation not in (0, 1):
        return(False, f"Error: Invalid operation '{operation}': must use '0' (read) or '1' (write).")
    if operation == 0 and not add_text:
        return(False, f"Error: no content provided for 'write' operation.")
    try:
        if operation == 0:
            with open(file_name, "r") as f:
                return(True, f.read())
        else:
            with open(file_name, "w") as f:
                f.write(add_text)
                return(True, f"Content successfully written to {file_name}")
    except FileNotFoundError as e:
        return (False, f"File not found: '{file_name}': {e}")
    except PermissionError as e:
        return (False, f"Permission denied for '{file_name}': {e}")
    except IsADirectoryError as e:
        return (False, f"'{file_name}' is a directory, not a file: {e}")
    except UnicodeDecodeError as e:
        return (False, f"Could not decode file '{file_name}': {e}")
    except OSError as e:
        return (False, f"OS error accessing '{file_name}': {e}")

