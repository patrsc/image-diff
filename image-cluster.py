import sys
from util import readJson, writeJson, getClusters


def main():
    threshold = float(sys.argv[1])
    inFile = "hashes.json"
    outFile = "clusters.json"
    hashes = readJson(inFile)
    clusters = getClusters(hashes, threshold)
    writeJson(outFile, clusters)


if __name__ == "__main__":
    main()
