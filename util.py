import os
import json

from PIL import Image
import imagehash
import numpy as np


def imhash(file):
    try:
        h = imagehash.phash(Image.open(file), hash_size=8)
    except:
        h = False
    return h


def getHashes(rootDir):
    # Walk directory and get hashes
    hashes = {}
    for dirName, subdirList, fileList in os.walk(rootDir):
        for fname in fileList:
            fullPath = dirName + "/" + fname
            print("Hashing: %s" % fullPath)
            h = imhash(fullPath)
            if h:
                hashes[fullPath] = encode_hash_json(h)
    return hashes


def encode_hash_json(h):
    e = h.hash.tolist()
    assert h == decode_hash_json(e), "encoded value does not match decoded value"
    return e


def decode_hash_json(e):
    return imagehash.ImageHash(np.array(e, dtype=bool))


def getClusters(hashes, threshold):
    files = list(hashes.keys())
    clusters = []
    for key in hashes:
        hashes[key] = decode_hash_json(hashes[key])
    for i, f in enumerate(files):
        similar = {}
        file_i = files[i]
        h_i = hashes[file_i]
        for j in range(i, len(files)):
            file_j = files[j]
            h_j = hashes[file_j]
            d = abs(int(h_i - h_j))
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
