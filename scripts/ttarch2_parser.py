import os
import sys
import struct

MAGIC_MAP = {
    0x54544345: ("TTCE", "Blowfish", "Oodle LZ", True),
    0x5454435a: ("TTCZ", "None", "Zlib", False),
    0x5454434e: ("TTCN", "None", "None", False),
    0x54544365: ("TTCe", "Blowfish (Variant)", "Oodle LZ", True),
    0x5454437a: ("TTCz", "None", "Zlib (Variant)", False),
}

def parse_ttarch2(filepath, verbose=True):
    file_size = os.path.getsize(filepath)
    if file_size < 12:
        raise ValueError(f"File too small to be a valid TTARCH2 archive ({file_size} bytes)")

    with open(filepath, "rb") as f:
        header_data = f.read(12)
        magic, chunk_size, chunk_count = struct.unpack("<III", header_data)

        if magic not in MAGIC_MAP:
            # Check ASCII representation
            magic_ascii = "".join(chr((magic >> (8 * i)) & 0xFF) for i in range(4))
            raise ValueError(f"Unknown TTARCH2 magic: 0x{magic:08X} ('{magic_ascii}')")

        magic_name, cipher_name, comp_name, is_encrypted = MAGIC_MAP[magic]

        # Calculate expected offset table size: (chunk_count + 1) * 8 bytes
        offset_table_size = (chunk_count + 1) * 8
        offset_data = f.read(offset_table_size)
        if len(offset_data) < offset_table_size:
            raise ValueError(f"Unexpected EOF reading chunk offset table. Expected {offset_table_size} bytes, got {len(offset_data)}")

        chunk_offsets = struct.unpack(f"<{chunk_count + 1}Q", offset_data)

    final_offset = chunk_offsets[-1]
    is_valid_size = (final_offset == file_size)

    # Compute compressed chunk sizes
    chunk_sizes = [
        chunk_offsets[i + 1] - chunk_offsets[i]
        for i in range(chunk_count)
    ]

    header_end = chunk_offsets[0]

    result = {
        "filepath": filepath,
        "filename": os.path.basename(filepath),
        "file_size": file_size,
        "magic": magic,
        "magic_name": magic_name,
        "cipher": cipher_name,
        "compression": comp_name,
        "is_encrypted": is_encrypted,
        "chunk_size": chunk_size,
        "chunk_count": chunk_count,
        "header_size": header_end,
        "chunk_offsets": chunk_offsets,
        "chunk_sizes": chunk_sizes,
        "valid_size": is_valid_size,
    }

    if verbose:
        print("=" * 60)
        print(f"Archive: {os.path.basename(filepath)}")
        print(f"File Size: {file_size:,} bytes")
        print(f"Magic: 0x{magic:08X} ('{magic_name}')")
        print(f"Encrypted: {is_encrypted} (Cipher: {cipher_name})")
        print(f"Compression: {comp_name}")
        print(f"Target Uncompressed Chunk Size: {chunk_size:,} bytes (0x{chunk_size:X})")
        print(f"Total Chunks: {chunk_count:,}")
        print(f"Header End Offset: {header_end} bytes")
        print(f"Final Chunk Offset: {final_offset:,} bytes")
        print(f"Size Validation: {'MATCH [OK]' if is_valid_size else 'MISMATCH [FAIL]'}")
        if chunk_sizes:
            print(f"Min Compressed Chunk: {min(chunk_sizes):,} bytes")
            print(f"Max Compressed Chunk: {max(chunk_sizes):,} bytes")
            print(f"First 3 Chunk Offsets: {[hex(x) for x in chunk_offsets[:3]]}")
            print(f"Last 3 Chunk Offsets:  {[hex(x) for x in chunk_offsets[-3:]]}")
        print("=" * 60)

    return result

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        # Default test file
        target = r"C:\GOG Games\Minecraft Story Mode - Season Two\Archives\MC2_pc_PC_P2_Menu_compressed.ttarch2"

    parse_ttarch2(target)
