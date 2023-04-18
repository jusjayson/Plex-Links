import random
from pathlib import Path

import pytest

from plex_links.hard_link import get_mkv_from_subdir, hard_link_nested_mkvs
from conftest import START_DIR_STR


def test_get_from_single_subdir():
    """
    We should get Path(mkv_file) when calling get_mkv_from_subdir on a subdir
    """
    nested_dir = Path(f"{START_DIR_STR}/subfolder")
    nested_dir.mkdir(exist_ok=True)
    nested_dir_mkv = Path(nested_dir, "my.mkv")
    distraction_files = [
        Path(nested_dir, f"{i}.{random.choice(('gif', 'aac', 'mp3'))}")
        for i in range(4)
    ]
    distraction_folders = [Path(nested_dir, f"subsubdir_{i}") for i in range(2)]
    for to_touch in (nested_dir_mkv, *distraction_files):
        to_touch.touch(exist_ok=True)
    for to_make in distraction_folders:
        to_make.mkdir(exist_ok=True)

    try:
        assert str(get_mkv_from_subdir(nested_dir)) == str(nested_dir_mkv)
    finally:
        for to_unlink in (nested_dir_mkv, *distraction_files):
            to_unlink.unlink()
        for to_remove in distraction_folders:
            to_remove.rmdir()
        nested_dir.rmdir()


def test_create_hardlink_to_nested_mkv():
    nested_dir = Path(f"{START_DIR_STR}/subfolder")
    nested_dir.mkdir(exist_ok=True)
    nested_dir_mkv = Path(nested_dir, "my.mkv")
    nested_dir_mkv.touch(exist_ok=True)

    try:
        hard_link_nested_mkvs(Path(START_DIR_STR))
        assert Path(START_DIR_STR, nested_dir_mkv.name).exists()
        Path(START_DIR_STR, nested_dir_mkv.name).unlink()
    finally:
        nested_dir_mkv.unlink()
        nested_dir.rmdir()


def test_create_hardlink_to_multiple_nested_mkvs():
    """
    So long as they exist at a depth of 1, hardlinks should be created
    to all mkvs
    """
    nested_dirs = []
    nested_mkvs = []
    for i in range(5):
        nested_dirs.append(nested_dir := Path(f"{START_DIR_STR}/subfolder_{i}"))
        nested_dir.mkdir(exist_ok=True)
        nested_mkvs.append(nested_dir_mkv := Path(nested_dir, f"{i}.mkv"))
        nested_dir_mkv.touch(exist_ok=True)

    try:
        hard_link_nested_mkvs(Path(START_DIR_STR))
        for i in range(5):
            assert Path(START_DIR_STR, nested_mkvs[i].name).exists()
            Path(nested_mkvs[i]).unlink()
            Path(START_DIR_STR, nested_mkvs[i].name).unlink()
    finally:
        for nested_dir in nested_dirs:
            nested_dir.rmdir()
