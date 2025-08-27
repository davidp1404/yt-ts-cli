#!/usr/bin/env python3
"""
Test script to verify the language detection functionality.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from yt_ts_cli.main import detect_original_language, get_language_name
from yt_ts_cli.logging_config import setup_logging

def test_language_detection():
    """Test language detection with a sample video."""
    logger = setup_logging(verbose=True)
    
    # Test with a known video (replace with a real URL for testing)
    test_url = "https://youtu.be/5X6uoKA41h4"  # Spanish medical video from README
    
    print(f"Testing language detection for: {test_url}")
    
    try:
        detected_lang = detect_original_language(test_url, logger)
        lang_name = get_language_name(detected_lang)
        
        print(f"Detected language: {detected_lang} ({lang_name})")
        
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    test_language_detection()
