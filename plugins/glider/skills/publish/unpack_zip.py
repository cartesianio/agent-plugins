import shutil
import stat
import sys
import zipfile
import zlib
from pathlib import Path

MAX_FILES = 1000
MAX_ENTRIES = 10 * MAX_FILES
OS_METADATA_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini"}
MAX_UNZIPPED_BYTES = 30 * 1024 * 1024
CHUNK_BYTES = 1024 * 1024


class TooLarge(Exception):
    pass


def parts_of(entry):
    return entry.filename.replace("\\", "/").split("/")


def is_os_metadata(parts):
    return (
        "__MACOSX" in parts
        or parts[-1] in OS_METADATA_NAMES
        or parts[-1].startswith("._")
    )


def refusal(entries):
    files = [
        entry
        for entry in entries
        if not entry.is_dir() and not is_os_metadata(parts_of(entry))
    ]
    if len(files) > MAX_FILES:
        return f"too many: {len(files)}"
    if len(entries) > MAX_ENTRIES:
        return f"too many: {len(entries)}"
    declared = 0
    for entry in entries:
        parts = parts_of(entry)
        kind = stat.S_IFMT(entry.external_attr >> 16)
        if parts[0] == "" or ".." in parts or parts[0].endswith(":"):
            return f"outside: {entry.filename}"
        if kind not in (0, stat.S_IFREG, stat.S_IFDIR):
            return f"not a file: {entry.filename}"
        if entry.is_dir() and (kind == stat.S_IFREG or entry.file_size):
            return f"not a file: {entry.filename}"
        if kind == stat.S_IFDIR and not entry.is_dir():
            return f"not a file: {entry.filename}"
        declared += entry.file_size
    if declared > MAX_UNZIPPED_BYTES:
        return "too large"
    return None


def extract(archive, entries, destination, limit):
    written = 0
    for entry in entries:
        target = destination.joinpath(*[part for part in parts_of(entry) if part])
        if entry.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        with archive.open(entry) as source, open(target, "xb") as output:
            while chunk := source.read(CHUNK_BYTES):
                written += len(chunk)
                # Declared sizes come from the zip itself, so count what is really written.
                if written > limit:
                    raise TooLarge
                output.write(chunk)


def unpack(path, destination, limit=MAX_UNZIPPED_BYTES):
    try:
        archive = zipfile.ZipFile(path)
    except (zipfile.BadZipFile, OSError, ValueError, NotImplementedError):
        return "not a zip"
    with archive:
        entries = archive.infolist()
        problem = refusal(entries)
        if problem:
            return problem
        try:
            destination.mkdir(parents=True)
        except FileExistsError:
            return "destination exists"
        except OSError:
            return "cannot write"
        try:
            extract(archive, entries, destination, limit)
        except TooLarge:
            shutil.rmtree(destination)
            return "too large"
        except (
            zipfile.BadZipFile,
            zlib.error,
            EOFError,
            OSError,
            RuntimeError,
            ValueError,
            NotImplementedError,
        ):
            shutil.rmtree(destination)
            return "not a zip"
    return None


if __name__ == "__main__":
    problem = unpack(sys.argv[1], Path(sys.argv[2]))
    print(problem or "ok")
    sys.exit(1 if problem else 0)
