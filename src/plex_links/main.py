import sys
from plex_links.hard_link import hard_link_dir
if sys.argv[1] == "hard_link_dir":
    hard_link_dir(sys.argv[2])

elif sys.argv[1] == "hard_link_mkvs":
    hard_link_dir(sys.argv[2])

hard_link_dir(sys.argv[0])
