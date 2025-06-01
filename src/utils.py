import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path


def parse_datetime_from_filename(fname: str) -> datetime:
    _, fname = os.path.split(fname)  # remove leading path
    return datetime.strptime(os.path.splitext(fname)[0].split('_')[1], '%Y%m%dT%H%M%S')  # extract and parse time element


def mv_old_transcriptions(n_days, from_folder=Path(os.path.expanduser("~/.vosk/transcriptions")), to_folder=None) -> int:
    """
    Move transcription files older than n_days from from_folder to to_folder.

    Args:
        n_days (int): Number of days. Files older than this will be moved.
        from_folder (str or Path, optional): Source folder containing transcription files.
            Defaults to ~/.vosk/transcriptions.
        to_folder (str or Path, optional): Destination folder for old files.
            Defaults to /tmp/old_transcriptions.
            If None, performs a dry run (prints operations without moving files).
    
    Returns:
        int: Number of files moved (or that would be moved in a dry run).
    """
    
    if to_folder is not None:
        to_folder = Path(to_folder)
        # Create destination folder if it doesn't exist
        os.makedirs(to_folder, exist_ok=True)
    
    # Calculate cutoff date
    cutoff_date = datetime.now() - timedelta(days=n_days)
    
    # Track number of files moved
    files_moved = 0
    
    # Process each file in the source folder
    for file_path in from_folder.glob("*.txt"):
        # Get file modification time
        time_from_filename = parse_datetime_from_filename(file_path)
        
        # Check if file is older than cutoff date
        if time_from_filename < cutoff_date:
            if to_folder is None:
                # Dry run - just print what would happen
                print(f"Would move: {file_path}")
                files_moved += 1
            else:
                # Move the file
                dest_path = to_folder / file_path.name
                try:
                    shutil.move(str(file_path), str(dest_path))
                    print(f"Moved: {file_path} → {dest_path}")
                    files_moved += 1
                except Exception as e:
                    print(f"Error moving {file_path}: {e}")
    
    # Print summary
    if to_folder is None:
        print(f"Dry run complete. {files_moved} files would be moved.")
    else:
        print(f"Move complete. {files_moved} files moved to {to_folder}.")
    
    return files_moved
