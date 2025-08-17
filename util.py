import os
import json

from PIL import Image

from hashes import get_algorithm


def getHashes(rootDir, algorithm="PerceptualHash"):
    # Walk directory and get hashes
    hashes = {}
    cls = get_algorithm(algorithm)
    for dirName, subdirList, fileList in os.walk(rootDir):
        for fname in fileList:
            fullPath = dirName + "/" + fname
            print("Hashing: %s" % fullPath)
            if is_image_file(fullPath):
                h = cls.hash_file(fullPath)
                hashes[fullPath] = h.encode()
    return {"algorithm": algorithm, "hashes": hashes}


def is_image_file(path: str) -> bool:
    """
    Check if the file at `path` is a valid image using Pillow.
    
    Returns True if the file can be opened and verified as an image,
    otherwise False.
    """
    try:
        with Image.open(path) as img:
            img.verify()
        return True
    except Exception:
        return False


def getClusters(hashes, threshold):
    algorithm = hashes["algorithm"]
    hashes = hashes["hashes"]
    files = list(hashes.keys())
    clusters = []
    for key in hashes:
        hashes[key] = get_algorithm(algorithm).decode(hashes[key])
    for i, f in enumerate(files):
        similar = {}
        file_i = files[i]
        h_i = hashes[file_i]
        for j in range(i, len(files)):
            file_j = files[j]
            h_j = hashes[file_j]
            d = h_i - h_j
            if (d <= threshold):
                similar[file_j] = d
        if len(similar.keys()) > 1:
            clusters.append(similar)
    return clusters


def readJson(file):
    with open(file, 'r') as f:
        return json.load(f)


def writeJson(file, data):
    with open(file, 'w') as f:
        json.dump(data, f)
