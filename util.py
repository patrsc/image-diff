import os
import json

from hashes import HashImagePerceptualHash, HashImageDeduplication, HashImageDeduplicationNeural
ALGORITHMS = {
    "HashImagePerceptualHash": HashImagePerceptualHash,
    "HashImageDeduplication": HashImageDeduplication,
    "HashImageDeduplicationNeural": HashImageDeduplicationNeural,
}

def getHashes(rootDir, algorithm="HashImageDeduplicationNeural"):
    # Walk directory and get hashes
    hashes = {}
    for dirName, subdirList, fileList in os.walk(rootDir):
        for fname in fileList:
            fullPath = dirName + "/" + fname
            print("Hashing: %s" % fullPath)
            cls = ALGORITHMS[algorithm]
            h = cls.hash_file(fullPath)
            if h:
                hashes[fullPath] = h.encode()
    return {"algorithm": algorithm, "hashes": hashes}


def getClusters(hashes, threshold):
    algorithm = hashes["algorithm"]
    hashes = hashes["hashes"]
    files = list(hashes.keys())
    clusters = []
    for key in hashes:
        hashes[key] = ALGORITHMS[algorithm].decode(hashes[key])
    for i, f in enumerate(files):
        similar = {}
        file_i = files[i]
        h_i = hashes[file_i]
        for j in range(i, len(files)):
            file_j = files[j]
            h_j = hashes[file_j]
            d = h_i.diff(h_j)
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
