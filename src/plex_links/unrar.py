import os
from pathlib import Path

# cd South.Park.S${SEASON}E${EPISODE}*/ && rar e *.rar && mv *.mkv ../hard_links_links/South.Park.S${SEASON}E${EPISODE}*/ && rm ../hard_links_links/South.Park.S${SEASON}E${EPISODE}*/*.r* && cd ..
# mv South.Park.S16E${EPISODE}*/*.mkv hard_links_links/South.Park.S16E${EPISODE}*/ && rm hard_links_links/South.Park.S16E${EPISODE}*/*.r*for EPISODE in $(seq 13 14); do cd South.Park.S${SEASON}E${EPISODE}*/ && rar e *.rar && mv *.mkv ../hard_links_links/South.Park.S${SEASON}E${EPISODE}*/ && rm ../hard_links_links/South.Park.S${SEASON}E${EPISODE}*/*.r* && cd ..; done
# for EPISODE in $(seq 13 14); do cd South.Park.S${SEASON}E${EPISODE}*/ && rar e *.rar && mv *.mkv ../hard_links_links/South.Park.S${SEASON}E${EPISODE}*/ && rm ../hard_links_links/South.Park.S${SEASON}E${EPISODE}*/*.r* && cd ..; done


def unrar(dir: Path):
    for file_or_folder in dir.iterdir():
        if file_or_folder.is_dir():
            unrar(file_or_folder)
        elif "rar" in file_or_folder.suffix:
            os.system(f"rar e {file_or_folder}")
