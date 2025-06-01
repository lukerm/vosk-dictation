import os
from pathlib import Path
from typing import List, Tuple, Optional, Dict
import re
from datetime import datetime


def load_transcript(file_path: str) -> Optional[str]:
    """
    Load transcript content from a file.
    
    Args:
        file_path: Path to the transcript file
        
    Returns:
        The content of the transcript or None if file cannot be read
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def load_all_transcripts(transcripts_path: str) -> Dict[str, str]:
    """
    Load all transcript files from a directory.
    
    Args:
        transcripts_path: Directory containing transcript files
        
    Returns:
        Dictionary with file paths as keys and transcript contents as values
    """
    transcripts = {}
    
    if not os.path.exists(transcripts_path):
        print(f"Path does not exist: {transcripts_path}")
        return transcripts
    
    for file_name in os.listdir(transcripts_path):
        if (not file_name.endswith('.txt')) or (not file_name.startswith('transcription_')):
            continue
            
        file_path = os.path.join(transcripts_path, file_name)
        content = load_transcript(file_path)
        
        if content:
            transcripts[file_path] = content
    
    return transcripts


def find_longest_transcript(transcripts: Dict[str, str]) -> List[Tuple[int, str]]:
    """
    Find the transcript(s) with the most words.
    
    Args:
        transcripts: Dictionary with file paths as keys and transcript contents as values
        
    Returns:
        List of tuples with (word_count, file_path) for the longest transcript(s)
    """
    if not transcripts:
        return []
    
    max_word_count = 0
    longest_transcripts = []
    
    for file_path, content in transcripts.items():
        word_count = len(content.split())
        
        if word_count > max_word_count:
            max_word_count = word_count
            longest_transcripts = [(word_count, file_path)]
        elif word_count == max_word_count:
            longest_transcripts.append((word_count, file_path))
    
    return longest_transcripts


def find_transcript_with_longest_word(transcripts: Dict[str, str]) -> List[Tuple[str, str]]:
    """
    Find the transcript(s) containing the longest word.
    
    Args:
        transcripts: Dictionary with file paths as keys and transcript contents as values
        
    Returns:
        List of tuples with (longest_word, file_path) for transcripts with the longest word(s)
    """
    if not transcripts:
        return []
    
    max_word_length = 0
    transcripts_with_longest_word = []
    
    for file_path, content in transcripts.items():
        # Split by whitespace and remove punctuation from words
        words = [word.strip('.,!?;:()[]{}"\'-') for word in content.split()]
        
        # Find the longest word in this transcript
        if words:
            longest_word = max(words, key=len)
            word_length = len(longest_word)
            
            if word_length > max_word_length:
                max_word_length = word_length
                transcripts_with_longest_word = [(longest_word, file_path)]
            elif word_length == max_word_length:
                transcripts_with_longest_word.append((longest_word, file_path))
    
    return transcripts_with_longest_word


def find_transcript_longer_or_shorter_than(transcripts: Dict[str, str], n_thresh: int, year: Optional[int] = None) -> List[Tuple[int, str]]:
    """
    Find transcripts containing at least or at most X words.
    
    Args:
        transcripts: Dictionary with file paths as keys and transcript contents as values
        n_thresh: Threshold for word count (positive for greater than, negative for less than)
        year: Optional year to filter transcripts by creation date
        
    Returns:
        List of tuples with (word_count, file_path) for matching transcripts
    """
    matching_transcripts = []
    
    for file_path, content in transcripts.items():
        # Check year if specified
        if year is not None:
            # Extract date from filename (format: transcription_YYYYMMDDTHHMMSS.txt)
            filename = os.path.basename(file_path)
            match = re.search(r'_(\d{4})(\d{2})(\d{2})T', filename)
            if not match or int(match.group(1)) != year:
                continue
        
        word_count = len(content.split())
        
        # Check threshold condition
        if (n_thresh > 0 and word_count >= n_thresh) or (n_thresh < 0 and word_count <= abs(n_thresh)):
            matching_transcripts.append((word_count, file_path))
    
    # Sort by word count (descending for greater than, ascending for less than)
    return sorted(matching_transcripts, key=lambda x: x[0], reverse=(n_thresh > 0))


if __name__ == "__main__":
    # Get the canonical save path from voice_recorder.py
    ROOT_DIR = os.path.expanduser("~/.vosk")
    TRANSCRIPTION_PATH = Path(ROOT_DIR) / "transcriptions"

    print(f"Analyzing transcripts in: {TRANSCRIPTION_PATH}")
    print("-" * 50)
    
    # Load all transcripts once
    all_transcripts = load_all_transcripts(str(TRANSCRIPTION_PATH))
    
    if not all_transcripts:
        print("No transcripts found for analysis.")
        exit(0)
    
    # Find and display the longest transcripts
    longest_transcripts = find_longest_transcript(all_transcripts)
    if longest_transcripts:
        print("Longest transcript(s):")
        for word_count, file_path in longest_transcripts:
            print(f"  - {os.path.basename(file_path)}: {word_count} words")
    else:
        print("No transcripts found for longest transcript analysis.")
    
    print("-" * 50)
    
    # Find and display transcripts with the longest words
    transcripts_with_longest_word = find_transcript_with_longest_word(all_transcripts)
    if transcripts_with_longest_word:
        print("Transcript(s) with longest word:")
        for longest_word, file_path in transcripts_with_longest_word:
            print(f"  - {os.path.basename(file_path)}: '{longest_word}' ({len(longest_word)} characters)")
    else:
        print("No transcripts found for longest word analysis.")
    
    print("-" * 50)
    
    # Find and display transcripts longer than 100 words in the current year
    current_year = datetime.now().year
    long_transcripts = find_transcript_longer_or_shorter_than(all_transcripts, 100, current_year)
    if long_transcripts:
        print(f"Transcripts with more than 100 words from {current_year}:")
        for word_count, file_path in long_transcripts:
            print(f"  - {os.path.basename(file_path)}: {word_count} words")
    else:
        print(f"No transcripts with more than 100 words found for {current_year}.")
