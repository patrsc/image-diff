"""Implementation of different image hash algorithms."""
from abc import ABC, abstractmethod
from typing import Self
import sys

from PIL import Image
import imagehash
import numpy as np
from imagededup.methods import PHash, CNN  # type: ignore


class AbstractHash(ABC):
    """Interface class for all hashing algorithms."""
    def __init__(self, h) -> None:
        self.hash = h

    @classmethod
    @abstractmethod
    def hash_file(cls, file: str) -> Self:
        """Get hash of file."""

    @abstractmethod
    def encode(self) -> str:
        """Encode to JSON."""

    @classmethod
    @abstractmethod
    def decode(cls, e: str) -> Self:
        """Decode from JSON."""

    @abstractmethod
    def __sub__(self, other: Self) -> float:
        """Compare two instances."""


def get_algorithms() -> dict[str, type[AbstractHash]]:
    """Get dict of all available image comparison algorithms."""
    current_module = sys.modules[__name__]
    subclasses = {}
    for name in dir(current_module):
        obj = getattr(current_module, name)
        if isinstance(obj, type) and issubclass(obj, AbstractHash) and obj is not AbstractHash:
            subclasses[name] = obj
    return subclasses


def get_algorithm(name: str) -> type[AbstractHash]:
    """Get image comparison algorithm by class name."""
    return get_algorithms()[name]


class PerceptualHash(AbstractHash):
    """Perceptual hash."""
    @classmethod
    def hash_file(cls, file: str) -> Self:
        return cls(imagehash.phash(Image.open(file), hash_size=8))

    def encode(self):
        e = self.hash.hash.tolist()
        assert self.hash == self.decode(e).hash, "encoded value does not match decoded value"
        return e

    @classmethod
    def decode(cls, e):
        h = imagehash.ImageHash(np.array(e, dtype=bool))
        return cls(h)

    def __sub__(self, other) -> float:
        return abs(float(self.hash - other.hash))


class PerceptualHashDeduplication(AbstractHash):
    """Perceptual hash using imagededup package."""
    @classmethod
    def hash_file(cls, file):
        hasher = PHash()
        h = hasher.encode_image(image_file=file)
        if h is None:
            raise ValueError("hasher returned None")
        return cls(h)

    def encode(self):
        return self.hash

    @classmethod
    def decode(cls, e):
        return cls(e)

    def __sub__(self, other) -> float:
        if len(self.hash) != len(other.hash):
            raise ValueError("Hashes must be of the same length")
        # Convert from hex to integers
        n1 = int(self.hash, 16)
        n2 = int(other.hash, 16)

        # XOR and count differing bits
        return float(bin(n1 ^ n2).count("1"))


class NeuralHash(AbstractHash):
    """Image hash using CNN."""
    @classmethod
    def hash_file(cls, file):
        encoder = CNN()
        h = encoder.encode_image(file)
        if h is None:
            raise ValueError("hasher returned None")
        h = cls(h)

    def encode(self):
        e = self.hash.tolist()
        msg = "encoded value does not match decoded value"
        assert np.array_equal(self.hash, self.decode(e).hash), msg
        return e

    @classmethod
    def decode(cls, e):
        h = np.array(e, dtype=np.float32)
        return cls(h)

    def __sub__(self, other) -> float:
        v1 = self.hash.flatten()
        v2 = other.hash.flatten()
        num = np.dot(v1, v2)
        denom = np.linalg.norm(v1) * np.linalg.norm(v2)
        return 1 - (num / denom)  # cosine distance
