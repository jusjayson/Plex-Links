import os
from pathlib import Path

from plex_links.hard_link import hard_link_dir


def backup(new_file_dir: str, backup_dir: str):
    if not (new_files := Path(new_file_dir)).exists():
        raise Exception(f"{new_files} DNE")
    if not (backups := Path(backup_dir)).exists():
        raise Exception(f"{backups} DNE")

    if new_files.is_file():
        print(f'ln "{Path(new_files)}" to "{Path(backups, new_files.name)}"')
        Path(backups, new_files.name).hardlink_to(new_files)
    else:
        if not Path(new_file_dir, "hard_links_links").exists():
            hard_link_dir(new_files)
        print(
            f"mv \"{Path(new_files, 'hard_links_links')}\" to \"{Path(backups, new_files.name)}\""
        )
        os.system(
            f"mv \"{Path(new_files, 'hard_links_links')}\" \"{Path(backups, new_files.name)}\""
        )
