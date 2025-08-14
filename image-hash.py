import sys
from util import getHashes, writeJson


def main():
    rootDir = sys.argv[1]
    outFile = "hashes.json"
    hashes = getHashes(rootDir)
    writeJson(outFile, hashes)


if __name__ == "__main__":
    main()
