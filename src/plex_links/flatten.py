import logging
from collections import deque
from pathlib import Path

from plex_links.backup import backup

LOGGER = logging.getLogger(__name__)


def flatten(target: str, dest: str = None):
    """
    Flatten target dir into parental dir.

    Notes:
        - On conflict, bigger file is chosen.
        - On conflicting dir, entire dir from dest is hardlinked to
          new dir in dest named "JIC".
    """

    def _flatten(file_or_folder: Path, _dest: Path, create_dir: bool = False):
        """
        Args:
         - create_dir: Whether the current dir should be recreated in _dest.
        """
        if file_or_folder.is_file():
            file = file_or_folder
            should_hardlink = True
            if (pre_existing := Path(_dest, file.name)).exists():
                if file.stat().st_size > pre_existing.stat().st_size:
                    LOGGER.debug(
                        "%s is bigger than %s. Replacing ...",
                        file,
                        pre_existing,
                    )
                    pre_existing.unlink()
                else:
                    should_hardlink = False
            if should_hardlink:
                LOGGER.debug("Hardlink %s to %s", pre_existing, file)
                pre_existing.hardlink_to(file)
            file.unlink()

        elif file_or_folder.is_dir():
            folder = file_or_folder
            sub_folders = deque()
            if create_dir:
                (nested_dest := Path(_dest, folder.name)).mkdir(exist_ok=True)
                LOGGER.debug("Created %s", nested_dest)
            else:
                nested_dest = Path(_dest)
            for nested_file_or_folder in folder.iterdir():
                LOGGER.debug("Checking %s", nested_file_or_folder)
                if nested_file_or_folder.is_dir():
                    sub_folders.append(nested_file_or_folder)
                else:
                    _flatten(nested_file_or_folder, nested_dest, create_dir)

            while sub_folders:
                _flatten(sub_folders.pop(), nested_dest, True)
            if not folder.iterdir():
                folder.rmdir()

    if not (target := Path(target)).exists():
        raise ValueError(f"{target} DNE")
    if not dest:
        dest = target.parent
    else:
        dest = Path(dest)
    if not dest.exists():
        raise ValueError(f"{dest} DNE")
    if target == dest:
        raise ValueError(f"{target} and {dest} must be differnt folders")

    _flatten(target, dest, False)
