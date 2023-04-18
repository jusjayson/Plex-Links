import os
import os.path


def get_project_dir():
    return os.environ.get(
        "PROJECT_DIR", f"{os.path.expanduser('~')}/code/ProgrammingProjects/Plex-Links"
    )


def get_config_folder_path() -> str:
    """
    Acquire HOME-like path for storing project configuration.
    """
    return os.environ.get(
        "CONFIG_FOLDER_PATH",
        f"{get_project_dir()}/config",
    )


def get_log_folder_path() -> str:
    """
    Acquire HOME-like path for storing project logs.
    """
    return os.environ.get(
        "LOG_FOLDER_PATH",
        f"{get_project_dir()}/logs",
    )
