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


def test_hardlink_in_root_folder():
    """
    If there is any file in the starting folder, it should be
    hardlinked into the new folder
    """
    test_file = Path(f"{start_dir_str}/test_file.mkv")
    try:
        test_file.touch()
        hard_link_dir(start_dir_str)
        assert Path(f"{hard_links_str}/test_file.mkv").exists()
        Path(f"{hard_links_str}/test_file.mkv").unlink()
    finally:
        Path(hard_links_str).rmdir()
        test_file.unlink()


def test_nested_hardlinks():
    Path(f"{start_dir_str}/nested_folder").mkdir(exist_ok=True)
    Path(f"{start_dir_str}/nested_folder/test_file.mkv").touch(exist_ok=True)
    try:
        hard_link_dir(start_dir_str)
        assert Path(f"{hard_links_str}/nested_folder/test_file.mkv").exists()
        Path(f"{hard_links_str}/nested_folder/test_file.mkv").unlink()
    finally:
        Path(f"{hard_links_str}/nested_folder").rmdir()
        Path(f"{start_dir_str}/nested_folder/test_file.mkv").unlink()
        Path(f"{start_dir_str}/nested_folder").rmdir()
        Path(hard_links_str).rmdir()
