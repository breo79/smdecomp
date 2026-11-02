"""
TTARCH2 Container Parser for Minecraft: Story Mode - Season Two
Corresponds to functions:
  - 0x14016b520: TTArchive2_Load
  - 0x14016ba80: TTArchive2_IsEncrypted
"""

import os
import struct
from dataclasses import dataclass
from typing import List, Optional, Tuple

MAGIC_ECTT = 0x54544345  # "ECTT" / TTCE: Blowfish encrypted + Oodle compressed
MAGIC_ZCTT = 0x5454435A  # "ZCTT" / TTCZ: Zlib compressed
MAGIC_NCTT = 0x5454434E  # "NCTT" / TTCN: Uncompressed raw container
MAGIC_ETCE = 0x54544365  # "eCTT" / TTCe: Alternate encrypted
MAGIC_ZTCZ = 0x5454437A  # "zCTT" / TTCz: Alternate compressed

MAGIC_NAMES = {
    MAGIC_ECTT: ("ECTT", "Blowfish", "Oodle LZ", True),
    MAGIC_ZCTT: ("ZCTT", "None", "Zlib", False),
    MAGIC_NCTT: ("NCTT", "None", "None", False),
    MAGIC_ETCE: ("TTCe", "Blowfish (Variant)", "Oodle LZ", True),
    MAGIC_ZTCZ: ("TTCz", "None", "Zlib (Variant)", False),
}

@dataclass
class TTArchiveInfo:
    filepath: str
    file_size: int
    magic: int
    magic_name: str
    cipher_name: str
    compression_name: str
    is_encrypted: bool
    is_chunked: bool
    chunk_size: int
    chunk_count: int
    chunk_offsets: List[int]
    payload_size: int
    is_valid_size: bool


class TTArchive2:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.file_size = os.path.getsize(filepath)
        self.info = self._parse_header()

    def _parse_header(self) -> TTArchiveInfo:
        if self.file_size < 12:
            raise ValueError(f"File too small ({self.file_size} bytes)")

        with open(self.filepath, "rb") as f:
            magic_bytes = f.read(4)
            magic = struct.unpack("<I", magic_bytes)[0]

            if magic not in MAGIC_NAMES:
                ascii_name = magic_bytes.decode("latin1", errors="replace")
                raise ValueError(f"Unknown TTARCH2 magic: 0x{magic:08X} ('{ascii_name}')")

            magic_name, cipher_name, comp_name, is_encrypted = MAGIC_NAMES[magic]

            if magic == MAGIC_NCTT:
                # NCTT format: 4 bytes magic, 8 bytes uint64 total size
                payload_size = struct.unpack("<Q", f.read(8))[0]
                chunk_size = 0
                chunk_count = 0
                chunk_offsets = [12, self.file_size]
                is_chunked = False
                is_valid = (payload_size == self.file_size or payload_size + 12 == self.file_size)
            else:
                # Chunked container (ECTT / ZCTT / TTCe / TTCz)
                chunk_size, chunk_count = struct.unpack("<II", f.read(8))
                offsets_data = f.read((chunk_count + 1) * 8)
                chunk_offsets = list(struct.unpack(f"<{chunk_count + 1}Q", offsets_data))
                payload_size = 0  # To be determined after decompression
                is_chunked = True
                is_valid = (chunk_offsets[-1] == self.file_size)

        return TTArchiveInfo(
            filepath=self.filepath,
            file_size=self.file_size,
            magic=magic,
            magic_name=magic_name,
            cipher_name=cipher_name,
            compression_name=comp_name,
            is_encrypted=is_encrypted,
            is_chunked=is_chunked,
            chunk_size=chunk_size,
            chunk_count=chunk_count,
            chunk_offsets=chunk_offsets,
            payload_size=payload_size,
            is_valid_size=is_valid
        )

    def read_chunk(self, chunk_index: int) -> bytes:
        if not self.info.is_chunked:
            raise ValueError("Archive is not chunked")
        if chunk_index < 0 or chunk_index >= self.info.chunk_count:
            raise IndexError(f"Chunk index {chunk_index} out of range (total: {self.info.chunk_count})")

        start = self.info.chunk_offsets[chunk_index]
        end = self.info.chunk_offsets[chunk_index + 1]
        length = end - start

        with open(self.filepath, "rb") as f:
            f.seek(start)
            return f.read(length)

    def read_raw_payload(self) -> bytes:
        """Reads raw uncompressed payload for NCTT archives."""
        if self.info.is_chunked:
            raise ValueError("Cannot read raw payload directly from a chunked container")
        with open(self.filepath, "rb") as f:
            f.seek(12)
            return f.read()
