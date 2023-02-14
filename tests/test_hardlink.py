import pytest
from pathlib import Path

from plex_links.hard_link import hard_link_dir
from plex_links.utils import get_project_dir

start_dir_str = f"{get_project_dir()}/tests/data/test_folder"
hard_links_str = f"{start_dir_str}/hard_links_links"


def test_hardlink_no_root():
    """
    Complain if root does not exist
    """
    with pytest.raises(ValueError):
        hard_link_dir("data/test_folder_2")
