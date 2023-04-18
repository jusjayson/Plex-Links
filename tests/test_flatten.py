from pathlib import Path
import pytest

from conftest import START_DIR_STR

from plex_links.flatten import flatten

LOREM_ISPUM = """
Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard
dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen
book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.
It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with
desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
"""


@pytest.fixture
def root_dir():
    path = Path(START_DIR_STR)
    path.parent.mkdir(exist_ok=True)  # This stays after cleanup
    path.mkdir(exist_ok=True)
    yield path
    for file in path.iterdir():
        file.unlink()
    path.rmdir()


@pytest.fixture
def level_1_dir():
    (path := Path(f"{START_DIR_STR}/nested_dir")).mkdir(exist_ok=True)
    yield path
    if path.exists():
        for file in path.iterdir():
            file.unlink()
        path.rmdir()


@pytest.fixture
def level_1_dir_w_files(level_1_dir):
    for i in range(3):
        (file := Path(level_1_dir, f"test_{i}.txt")).touch()
        file.write_text(LOREM_ISPUM)
    yield level_1_dir


@pytest.fixture
def level_2_dir(level_1_dir):
    (path := Path(level_1_dir, "nested_dir")).mkdir(exist_ok=True)
    yield path
    if path.exists():
        for file in path.iterdir():
            file.unlink()
        path.rmdir()


@pytest.fixture
def level_2_dir_w_files(level_2_dir):
    for i in range(3):
        (file := Path(level_2_dir, f"test_{i}.txt")).touch()
        file.write_text(LOREM_ISPUM)
    yield level_2_dir


def test_flatten_folder_files_not_in_dest(root_dir, level_1_dir_w_files):
    expected_files = [
        Path(root_dir, file.name) for file in level_1_dir_w_files.iterdir()
    ]
    for expected_file in expected_files:
        assert not expected_file.exists()
    flatten(level_1_dir_w_files)
    for expected_file in expected_files:
        assert expected_file.exists()


def test_flatten_folder_files_in_dest(root_dir, level_1_dir_w_files):
    expected_files = [
        Path(root_dir, file.name) for file in level_1_dir_w_files.iterdir()
    ]
    for expected_file in expected_files:
        assert not expected_file.exists()
        expected_file.touch()

    flatten(level_1_dir_w_files)
    for expected_file in expected_files:
        assert (
            expected_file.read_text() == LOREM_ISPUM
        )  # Flatten replaces original file with bigger one


def test_flatten_nested_folder_files_not_in_dest(root_dir, level_2_dir_w_files):
    expected_nested_files = [
        Path(root_dir, level_2_dir_w_files.name, file.name)
        for file in level_2_dir_w_files.iterdir()
    ]
    for expected_file in expected_nested_files:
        assert not expected_file.exists()

    flatten(level_2_dir_w_files.parent, root_dir)
    for expected_nested_file in expected_nested_files:
        assert (
            expected_nested_file.exists()
            and expected_nested_file.read_text() == LOREM_ISPUM
        )


def test_flatten_nested_folder_files_in_dest(root_dir, level_2_dir_w_files):
    expected_files = [
        Path(root_dir, file.name) for file in level_2_dir_w_files.iterdir()
    ]
    expected_nested_files = [
        Path(root_dir, level_2_dir_w_files.name, file.name)
        for file in level_2_dir_w_files.iterdir()
    ]
    for expected_nested_file in expected_nested_files:
        expected_nested_file.touch()

    flatten(level_2_dir_w_files.parent, root_dir)
    for expected_file in expected_files:
        assert expected_file.exists() and expected_file.read_text() == ""
    for expected_nested_file in expected_nested_files:
        assert (
            expected_nested_file.exists()
            and expected_nested_file.read_text() == LOREM_ISPUM
        )
