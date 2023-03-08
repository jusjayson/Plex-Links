import sys
from plex_links.backup import backup
from plex_links.hard_link import hard_link_dir
from plex_links.unrar import unrar

if sys.argv[1] == "hard_link_dir":
    print("HARD LINKING DIR")
    hard_link_dir(sys.argv[2])

elif sys.argv[1] == "hard_link_mkvs":
    print("HARD LINKING MKVS")
    hard_link_dir(sys.argv[2])

elif sys.argv[1] == "unrar_dir":
    print("EXTRACTING DIR")
    unrar(sys.argv[2])

elif sys.argv[1] == "backup_dir":
    print("BACKING UP DIR")
    backup(sys.argv[2], sys.argv[3])
