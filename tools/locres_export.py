#!/usr/bin/env python3
"""Export Unreal Engine .locres entries, including UE5 CityHash64/UTF-16 keys."""

from __future__ import annotations

import argparse
import csv
import json
import struct
from pathlib import Path

MAGIC = bytes.fromhex("0e147475674a03fc4a15909dc3377f1b")


class Reader:
    def __init__(self, data: bytes):
        self.data = data
        self.pos = 0

    def take(self, size: int) -> bytes:
        if size < 0 or self.pos + size > len(self.data):
            raise ValueError(f"Unexpected EOF at 0x{self.pos:x} (wanted {size} bytes)")
        result = self.data[self.pos : self.pos + size]
        self.pos += size
        return result

    def unpack(self, fmt: str):
        size = struct.calcsize(fmt)
        return struct.unpack(fmt, self.take(size))[0]

    def fstring(self) -> str:
        length = self.unpack("<i")
        if length == 0:
            return ""
        if length < 0:
            raw = self.take((-length) * 2)
            if raw[-2:] != b"\0\0":
                raise ValueError(f"Unterminated UTF-16 FString at 0x{self.pos - len(raw):x}")
            return raw[:-2].decode("utf-16-le")
        raw = self.take(length)
        if raw[-1:] != b"\0":
            raise ValueError(f"Unterminated FString at 0x{self.pos - len(raw):x}")
        return raw[:-1].decode("utf-8")


def parse(path: Path) -> tuple[int, list[dict[str, object]]]:
    reader = Reader(path.read_bytes())
    if reader.data[:16] == MAGIC:
        reader.pos = 16
        version = reader.unpack("<B")
    else:
        version = 0

    strings: list[str] = []
    if version >= 1:
        string_table_offset = reader.unpack("<q")
        if version >= 2:
            entry_count = reader.unpack("<i")
        else:
            entry_count = None
    else:
        string_table_offset = -1
        entry_count = None

    namespace_count = reader.unpack("<I")
    if namespace_count > 1_000_000:
        raise ValueError(f"Invalid namespace count: {namespace_count}")

    rows: list[dict[str, object]] = []
    actual_entries = 0
    for _ in range(namespace_count):
        if version >= 2:
            # UE stores CityHash64's folded 32-bit result for version 3 keys.
            namespace_hash = reader.unpack("<I")
        else:
            hash_size = 0
            namespace_hash = None
        namespace = reader.fstring()
        key_count = reader.unpack("<I")
        if key_count > 10_000_000:
            raise ValueError(f"Invalid key count in namespace {namespace!r}: {key_count}")
        for _ in range(key_count):
            key_hash = reader.unpack("<I") if version >= 2 else None
            key = reader.fstring()
            source_hash = reader.unpack("<I")
            if version >= 1:
                string_index = reader.unpack("<i")
                localized = None
            else:
                string_index = None
                localized = reader.fstring()
            rows.append(
                {
                    "namespace": namespace,
                    "namespace_hash": namespace_hash,
                    "key": key,
                    "key_hash": key_hash,
                    "source_hash": source_hash,
                    "string_index": string_index,
                    "localized": localized,
                }
            )
            actual_entries += 1

    if entry_count is not None and entry_count != actual_entries:
        raise ValueError(f"Header says {entry_count} entries, parsed {actual_entries}")

    if version >= 1 and string_table_offset >= 0:
        return_pos = reader.pos
        reader.pos = string_table_offset
        string_count = reader.unpack("<i")
        if string_count < 0 or string_count > 10_000_000:
            raise ValueError(f"Invalid string table count: {string_count}")
        ref_counts: list[int | None] = []
        for _ in range(string_count):
            strings.append(reader.fstring())
            ref_counts.append(reader.unpack("<i") if version >= 2 else None)
        reader.pos = return_pos
        for row in rows:
            index = row["string_index"]
            if not isinstance(index, int) or index < 0 or index >= len(strings):
                raise ValueError(f"Invalid string index {index!r} for {row['namespace']}:{row['key']}")
            row["localized"] = strings[index]
            row["ref_count"] = ref_counts[index]

    return version, rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--json", type=Path, help="Write all entries as JSON")
    parser.add_argument("--csv", type=Path, help="Write entries as UTF-8 CSV")
    parser.add_argument("--search", help="Print entries whose source/localized text contains this phrase")
    args = parser.parse_args()

    version, rows = parse(args.input)
    print(f"LocRes version={version}; namespaces={len({r['namespace'] for r in rows})}; entries={len(rows)}")
    if args.search is not None:
        needle = args.search.casefold()
        matches = [r for r in rows if needle in str(r["key"]).casefold() or needle in str(r["localized"]).casefold()]
        for row in matches:
            print(json.dumps(row, ensure_ascii=False))
    if args.json:
        args.json.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.csv:
        with args.csv.open("w", encoding="utf-8-sig", newline="") as output:
            writer = csv.DictWriter(output, fieldnames=list(rows[0]) if rows else [])
            writer.writeheader()
            writer.writerows(rows)


if __name__ == "__main__":
    main()
