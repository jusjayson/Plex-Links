import os
from pathlib import Path

from plex_links.hard_link import hard_link_dir


def backup(new_file_dir: str, backup_dir: str):
    new_files = Path(new_file_dir)
    backups = Path(backup_dir)

    for path in (new_files, backups):
        if not path.exists():
            raise Exception(f"{path} DNE")

    for file_or_folder in new_files.iterdir():
        if file_or_folder.is_file():
            Path(backups, file_or_folder.name).hardlink_to(file_or_folder)
        else:
            hard_link_dir(file_or_folder)
            os.system(
                f"mv {file_or_folder}/hard_link_links {backups}/{file_or_folder.name}"
            )
