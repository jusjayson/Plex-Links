from pathlib import Path


def hard_link_dir(starting_dir: str):
    starting_dir = Path(starting_dir)
    if not starting_dir.exists():
        raise ValueError(f"Starting dir: {starting_dir} does not exist")
