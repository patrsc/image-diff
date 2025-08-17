"""Create hashes.json database."""
import sys
from util import get_hashes, write_json


def main():
    """Hash images."""
    root_dir = sys.argv[1]
    algorithm = "PerceptualHash"
    if len(sys.argv) > 2:
        algorithm = sys.argv[2]
    print(f"Using algorithm: {algorithm}")
    out_file = "hashes.json"
    hashes = get_hashes(root_dir, algorithm)
    write_json(out_file, hashes)


if __name__ == "__main__":
    main()
