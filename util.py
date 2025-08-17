"""Utilities."""
import os
import json

from PIL import Image

from hashes import get_algorithm


def get_hashes(root_dir, algorithm):
    """Walk directory and get hashes."""
    hashes = {}
    cls = get_algorithm(algorithm)
    for dir_name, _, file_list in os.walk(root_dir):
        for fname in file_list:
            full_path = dir_name + "/" + fname
            print(f"Hashing: {full_path}")
            if is_image_file(full_path):
                h = cls.hash_file(full_path)
                hashes[full_path] = h.encode()
    return {"algorithm": algorithm, "hashes": hashes}


def is_image_file(path: str) -> bool:
    """Return True if file at `path` is an image file."""
    # pylint: disable=broad-exception-caught
    try:
        with Image.open(path) as img:
            img.verify()
        return True
    except Exception:
        return False


def get_clusters(hashes, threshold):
    """Cluster images by similarity."""
    algorithm = hashes["algorithm"]
    hashes = hashes["hashes"]
    files = list(hashes.keys())
    clusters = []
    for key in hashes:
        hashes[key] = get_algorithm(algorithm).decode(hashes[key])
    for i, f in enumerate(files):
        similar = {}
        file_i = f
        h_i = hashes[file_i]
        for j in range(i, len(files)):
            file_j = files[j]
            h_j = hashes[file_j]
            d = h_i - h_j
            if d <= threshold:
                similar[file_j] = d
        if len(similar.keys()) > 1:
            clusters.append(similar)
    return clusters


def read_json(file):
    """Read JSON file."""
    with open(file, 'r', encoding='utf8') as f:
        return json.load(f)


def write_json(file, data):
    """Write JSON file."""
    with open(file, 'w', encoding='utf8') as f:
        json.dump(data, f)
