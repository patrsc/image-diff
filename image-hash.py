#!/usr/bin/env python3

# pip install ImageHash
from PIL import Image
import imagehash
import sys
import os
import json

def imhash(file):
    try:
        h = imagehash.phash(Image.open(file))
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
                hashes[fullPath] = h
    return hashes

def getClusters(hashes, threshold):
    files = list(hashes.keys())
    clusters = []
    for i, f in enumerate(files):
        similar = {}
        for j in range(i, len(files)):
            d = hashes[files[i]] - hashes[files[j]]
            if (d <= threshold):
                similar[files[j]] = int(d)
        if len(similar.keys()) > 1:
            clusters.append(similar)
    return clusters

def writeJson(file, data):
    with open(file, 'w') as f:
        json.dump(data, f)

def main(rootDir, threshold, outFile):
    hashes = getHashes(rootDir)
    clusters = getClusters(hashes, threshold)
    writeJson(outFile, clusters)

# Main
rootDir = sys.argv[1]
threshold = int(sys.argv[2])
outFile = sys.argv[3]
main(rootDir, threshold, outFile)
