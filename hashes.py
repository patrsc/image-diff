from PIL import Image
import imagehash
import numpy as np
from imagededup.methods import PHash, CNN


class HashImagePerceptualHash:
    def __init__(self, h):
        self.hash = h

    @staticmethod
    def hash_file(file):
        try:
            h = imagehash.phash(Image.open(file), hash_size=8)
            h = HashImagePerceptualHash(h)
        except:
            h = False
        return h

    def encode(self):
        e = self.hash.hash.tolist()
        assert self.hash == self.decode(e).hash, "encoded value does not match decoded value"
        return e

    @staticmethod
    def decode(e):
        h = imagehash.ImageHash(np.array(e, dtype=bool))
        return HashImagePerceptualHash(h)

    def diff(self, other) -> int:
        return abs(int(self.hash - other.hash))


class HashImageDeduplication:
    def __init__(self, h):
        self.hash = h

    @staticmethod
    def hash_file(file):
        try:
            hasher = PHash()
            h = hasher.encode_image(image_file=file)
            if h is None:
                return False
            h = HashImageDeduplication(h)
        except:
            h = False
        return h

    def encode(self):
        return self.hash

    @staticmethod
    def decode(e):
        return HashImageDeduplication(e)

    def diff(self, other) -> int:
        if len(self.hash) != len(other.hash):
            raise ValueError("Hashes must be of the same length")
        # Convert from hex to integers
        n1 = int(self.hash, 16)
        n2 = int(other.hash, 16)

        # XOR and count differing bits
        return bin(n1 ^ n2).count("1")


class HashImageDeduplicationNeural:
    def __init__(self, h):
        self.hash = h

    @staticmethod
    def hash_file(file):
        try:
            encoder = CNN()
            h = encoder.encode_image(file)
            if h is None:
                return False
            h = HashImageDeduplicationNeural(h)
        except Exception as e:
            h = False
        return h

    def encode(self):
        e = self.hash.tolist()
        assert np.array_equal(self.hash, self.decode(e).hash), "encoded value does not match decoded value"
        return e

    @staticmethod
    def decode(e):
        h = np.array(e, dtype=np.float32)
        return HashImageDeduplicationNeural(h)

    def diff(self, other, metric= 'cosine') -> float:
        v1 = self.hash.flatten()
        v2 = other.hash.flatten()
        if metric == 'cosine':
            num = np.dot(v1, v2)
            denom = np.linalg.norm(v1) * np.linalg.norm(v2)
            return 1 - (num / denom)  # cosine distance
        elif metric == 'euclidean':
            return float(np.linalg.norm(v1 - v2))
        else:
            raise ValueError("metric must be 'cosine' or 'euclidean'")
