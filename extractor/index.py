"""
Resource Index & Symbol Hashing Subsystem for Telltale Tool 2017 Gen 5 (TTA4)
Corresponds to functions:
  - 0x14016c4e0: TTArchive2_InitializeIndex
"""

import struct
from dataclasses import dataclass
from typing import List, Dict, Optional

# CRC-64-ECMA polynomial used by Telltale engine
CRC64_POLYNOMIAL = 0x42F0E1EBA9EA3693

def crc64_symbol(name: str) -> int:
    """
    Computes the 64-bit Symbol CRC for a given resource filename.
    Filenames are converted to lowercase ASCII before hashing.
    Algorithm: CRC-64-ECMA (MSB-first, init=0, poly=0x42F0E1EBA9EA3693).
    """
    crc = 0
    for b in name.lower().encode('ascii', errors='ignore'):
        crc ^= (b << 56)
        for _ in range(8):
            if crc & 0x8000000000000000:
                crc = ((crc << 1) ^ CRC64_POLYNOMIAL) & 0xFFFFFFFFFFFFFFFF
            else:
                crc = (crc << 1) & 0xFFFFFFFFFFFFFFFF
    return crc


@dataclass
class ArchiveEntry:
    symbol_hash: int
    data_offset: int
    data_size: int
    flags: int
    name_offset: int
    name: Optional[str] = None


class TTA4Index:
    """
    Represents an inner TTArchive version 4 (TTA4) resource index.
    Header: 12 bytes ('4ATT', string_table_size, entry_count)
    Entries: entry_count * 28 bytes (<QQQHH)
    String Table: string_table_size bytes
    """
    def __init__(self, data: bytes):
        if len(data) < 12:
            raise ValueError("Buffer too small for TTA4 index")

        magic, self.string_table_size, self.entry_count = struct.unpack("<III", data[:12])
        if magic != 0x54544134:  # '4ATT' (0x34, 0x41, 0x54, 0x54 in LE = 0x54544134)
            magic_ascii = data[:4].decode('latin1', errors='replace')
            raise ValueError(f"Invalid TTA4 magic: 0x{magic:08X} ('{magic_ascii}')")

        entries_size = self.entry_count * 28
        header_end = 12 + entries_size
        if len(data) < header_end:
            raise ValueError(f"Buffer truncated while reading {self.entry_count} entries")

        entries_raw = data[12:header_end]
        str_table = data[header_end : header_end + self.string_table_size]
        
        self.data_section_offset = header_end + self.string_table_size

        self.entries: List[ArchiveEntry] = []
        self.entries_by_hash: Dict[int, ArchiveEntry] = {}
        self.entries_by_name: Dict[str, ArchiveEntry] = {}

        for i in range(self.entry_count):
            entry_bytes = entries_raw[i * 28 : (i + 1) * 28]
            h, off, sz, flags, name_off = struct.unpack("<QQQHH", entry_bytes)
            
            # Resolve name from string table
            name = None
            if name_off < len(str_table):
                null_pos = str_table.find(b"\x00", name_off)
                if null_pos != -1:
                    try:
                        name = str_table[name_off:null_pos].decode("ascii")
                    except UnicodeDecodeError:
                        name = None

            entry = ArchiveEntry(
                symbol_hash=h,
                data_offset=off,
                data_size=sz,
                flags=flags,
                name_offset=name_off,
                name=name
            )
            self.entries.append(entry)
            self.entries_by_hash[h] = entry
            if name:
                self.entries_by_name[name.lower()] = entry

    def find_by_name(self, name: str) -> Optional[ArchiveEntry]:
        h = crc64_symbol(name)
        return self.entries_by_hash.get(h)
