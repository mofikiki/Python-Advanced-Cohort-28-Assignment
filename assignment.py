from datetime import datetime, timedelta
import os


FILENAME = "visitors.txt"
TIMESTAMP_FMT = "%Y-%m-%d %H:%M:%S"
COOLDOWN = timedelta(minutes=5)


class TooSoonError(Exception):
    """Raised when a new visitor arrives within 5 minutes of the last log."""
    pass

class DuplicateVisitorError(Exception):
    """Raised when the same visitor name is entered as the last logged one."""
    pass

def get_last_entry(path: str):
    """
    Return (last_name, last_time) from the file, or (None, None) if not found.
    Safely skips blank/malformed lines and handles non-existent file.
    """
    if not os.path.exists(path):
        return None, None

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for raw in reversed(lines):
        line = raw.strip()
        if not line:
            continue
        try:
            name_part, ts_part = line.split(" - ", 1)
            when = datetime.strptime(ts_part.strip(), TIMESTAMP_FMT)
            return name_part.strip(), when
        except ValueError:
  
            continue

    return None, None

def main():
    visitor_name = input("What is your name: ").strip()
    if not visitor_name:
        print("Name cannot be empty.")
        return

    last_name, last_time = get_last_entry(FILENAME)
    now = datetime.now()


    if last_time is not None:
        elapsed = now - last_time
        if elapsed < COOLDOWN:
            remaining = COOLDOWN - elapsed
            mins = remaining.seconds // 60
            secs = remaining.seconds % 60
            raise TooSoonError(f"Last visitor logged {int(elapsed.total_seconds())}s ago. "
                               f"Please try again in {mins}m {secs}s.")


    if last_name and visitor_name.lower() == last_name.lower():
        raise DuplicateVisitorError("Same visitor as last entry.")


    with open(FILENAME, "a", encoding="utf-8") as f:
        f.write(f"{visitor_name} - {now.strftime(TIMESTAMP_FMT)}\n")

    print("Visitor logged successfully!")

if __name__ == "__main__":
    try:
        main()
    except TooSoonError as e:
        print(f"TooSoonError: {e}")
    except DuplicateVisitorError as e:
        print(f"DuplicateVisitorError: {e}")
    except Exception as e:
        print("Unexpected error:", e)
