from pathlib import Path


def hard_link_dir(starting_dir: str):
    def create_file_or_dir(copy_dir: Path, target_dir: Path):
        """
        Hardlink each file in copy_dir to target_dir.

        Notes:
            - Runs recursively, such that root/my_folder/my_file
            will be hardlinked from target/my_folder/my_file
        """
        for file_or_folder in copy_dir.iterdir():
            if file_or_folder.name != target_dir.name:
                if file_or_folder.is_file():
                    Path(f"{target_dir}/{file_or_folder.name}").hardlink_to(
                        str(file_or_folder)
                    )
                else:
                    nested_dir = Path(f"{str(target_dir)}/{file_or_folder.name}")
                    nested_dir.mkdir()
                    create_file_or_dir(file_or_folder, nested_dir)

    starting_dir = Path(starting_dir)
    if not starting_dir.exists():
        raise ValueError(f"Starting dir: {starting_dir} does not exist")
    links_dir = Path(f"{str(starting_dir)}/hard_links_links")
    links_dir.mkdir()
    create_file_or_dir(starting_dir, links_dir)
