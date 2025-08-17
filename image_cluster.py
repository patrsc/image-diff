"""Create clusters.json file containing similar image clusters."""
import sys
from util import read_json, write_json, get_clusters


def main():
    """Cluster images."""
    threshold = float(sys.argv[1])
    in_file = "hashes.json"
    out_file = "clusters.json"
    hashes = read_json(in_file)
    clusters = get_clusters(hashes, threshold)
    write_json(out_file, clusters)


if __name__ == "__main__":
    main()
