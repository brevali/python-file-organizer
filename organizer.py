
from pathlib import Path
import shutil

# The program only works inside this practice folder.
TEST_FOLDER = Path(__file__).parent / "test_files"

# File extensions and their destination folders.
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"],
    "Documents": [".txt", ".pdf", ".doc", ".docx", ".odt"],
    "Videos": [".mp4", ".mov", ".mkv", ".avi"],
    "Audio": [".mp3", ".wav", ".flac", ".m4a"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Spreadsheets": [".csv", ".xls", ".xlsx"],
}

def get_category(file_path):
    """Find the folder for a supported file type."""
    extension = file_path.suffix.lower()

    for category, extensions in FILE_TYPES.items():
        if extension in extensions:
            return category

    return None


def unique_destination(destination):
    """Avoid overwriting a file with the same name."""
    if not destination.exists():
        return destination

    number = 1

    while True:
        new_name = (
            f"{destination.stem}_{number}{destination.suffix}"
        )
        candidate = destination.with_name(new_name)

        if not candidate.exists():
            return candidate

        number += 1


def main():
    if not TEST_FOLDER.is_dir():
        print("The test_files folder was not found.")
        print("Create it beside organizer.py and try again.")
        return

    moves = []

    # Look only at files directly inside test_files.
    for item in TEST_FOLDER.iterdir():
        if not item.is_file():
            continue

        category = get_category(item)

        # Unsupported file types are left alone.
        if category is None:
            continue

        destination_folder = TEST_FOLDER / category
        destination = unique_destination(
            destination_folder / item.name
        )

        moves.append((item, destination))

    if not moves:
        print("No supported files were found to organize.")
        return

    print("\nPREVIEW: These files would be moved:\n")

    for source, destination in moves:
        print(f"{source.name} -> {destination.parent.name}/"
              f"{destination.name}")

    print("\nNothing has been moved yet.")
    answer = input(
        "\nType YES to move these files, or anything else to cancel: "
    )

    if answer != "YES":
        print("Cancelled. No files were moved.")
        return

    moved = 0

    for source, destination in moves:
        try:
            destination.parent.mkdir(
                parents=True, exist_ok=True
            )

            # Recheck in case a destination appeared meanwhile.
            destination = unique_destination(destination)

            shutil.move(str(source), str(destination))
            moved += 1
            print(f"Moved: {source.name}")

        except OSError as error:
            print(f"Could not move {source.name}: {error}")

    print(f"\nFinished. Successfully moved {moved} file(s).")


if __name__ == "__main__":
    main()
