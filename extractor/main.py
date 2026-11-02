"""
Minecraft: Story Mode - Season Two TTARCH2 Extractor & Analyzer CLI
Milestone 1 Implementation
"""

import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from extractor.ttarch2 import TTArchive2
from extractor.index import TTA4Index


def main():
    if len(sys.argv) < 2:
        print("Usage: python extractor/main.py <path_to_archive.ttarch2> [--list]")
        print("Example: python extractor/main.py \"C:\\GOG Games\\Minecraft Story Mode - Season Two\\Archives\\MC2_pc_PC_P2_Menu_compressed.ttarch2\"")
        sys.exit(1)

    archive_path = sys.argv[1]
    list_files = "--list" in sys.argv

    if not os.path.exists(archive_path):
        print(f"Error: File not found: {archive_path}")
        sys.exit(1)

    try:
        archive = TTArchive2(archive_path)
    except Exception as e:
        print(f"Error parsing archive: {e}")
        sys.exit(1)

    info = archive.info

    print("=" * 65)
    print(" MCSM2 ARCHIVE ANALYSIS REPORT")
    print("=" * 65)
    print(f"File:               {os.path.basename(info.filepath)}")
    print(f"Full Path:          {info.filepath}")
    print(f"File Size:          {info.file_size:,} bytes")
    print(f"Archive Type:       {info.magic_name} (Magic: 0x{info.magic:08X})")
    print(f"Encryption State:   {'ENCRYPTED' if info.is_encrypted else 'UNENCRYPTED'}")
    if info.is_encrypted:
        print(f"Cipher Algorithm:   {info.cipher_name}")
    print(f"Compression Type:   {info.compression_name}")
    print(f"Container Layout:   {'Chunked' if info.is_chunked else 'Direct Uncompressed'}")

    if info.is_chunked:
        print(f"Target Chunk Size:  {info.chunk_size:,} bytes (0x{info.chunk_size:X})")
        print(f"Total Chunks:       {info.chunk_count:,}")
        print(f"Header Table Size:  {len(info.chunk_offsets) * 8:,} bytes")
        print(f"Size Validation:    {'VALID [OK]' if info.is_valid_size else 'INVALID [MISMATCH]'}")
        if info.chunk_count > 0:
            sizes = [
                info.chunk_offsets[i + 1] - info.chunk_offsets[i]
                for i in range(info.chunk_count)
            ]
            print(f"Min Chunk Size:     {min(sizes):,} bytes")
            print(f"Max Chunk Size:     {max(sizes):,} bytes")
            print(f"First Chunk Offset: 0x{info.chunk_offsets[0]:X}")
            print(f"Last Chunk Offset:  0x{info.chunk_offsets[-1]:X}")
    else:
        print(f"Payload Size:       {info.payload_size:,} bytes")
        print(f"Size Validation:    {'VALID [OK]' if info.is_valid_size else 'INVALID [MISMATCH]'}")
        
        # If NCTT, we can parse inner TTA4 index immediately
        try:
            raw_payload = archive.read_raw_payload()
            index = TTA4Index(raw_payload)
            print("-" * 65)
            print(f"Inner Format:       TTA4 (TTArchive Version 4)")
            print(f"Total Resources:    {index.entry_count:,} files")
            print(f"String Table Size:  {index.string_table_size:,} bytes")
            
            named_count = sum(1 for e in index.entries if e.name)
            print(f"Named Resources:    {named_count:,} / {index.entry_count:,}")
            
            if list_files:
                print("-" * 65)
                print(f"{'Index':<6} {'Hash':<18} {'Size (Bytes)':<14} {'Filename'}")
                print("-" * 65)
                for idx, entry in enumerate(index.entries):
                    name_str = entry.name if entry.name else f"<Unknown 0x{entry.symbol_hash:016X}>"
                    print(f"[{idx:4d}] 0x{entry.symbol_hash:016X}  {entry.data_size:<14,d} {name_str}")
        except Exception as e:
            print(f"Inner TTA4 Parse:   Failed ({e})")

    print("=" * 65)


if __name__ == "__main__":
    main()
