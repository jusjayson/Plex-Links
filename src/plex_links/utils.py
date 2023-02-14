import os
import os.path


def get_project_dir():
    return os.environ.get(
        "PROJECT_DIR", f"{os.path.expanduser('~')}/ProgrammingProjects/Plex-Links"
    )
