#!/usr/bin/env python3
"""
YouTube Transcript CLI Tool
A command-line tool to list and download YouTube video transcripts using yt-dlp Python module.
"""

import argparse
import sys
import os
import tempfile
import contextlib
import importlib.util
from pathlib import Path
import yt_dlp
import re

from . import __version__
from .logging_config import setup_logging, SuppressYtDlpLogger


@contextlib.contextmanager
def suppress_stderr():
    """Context manager to suppress stderr output."""
    with open(os.devnull, 'w') as devnull:
        old_stderr = sys.stderr
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stderr = old_stderr


def list_languages(url, logger):
    """List available subtitle languages for a YouTube video."""
    logger.info(f"Checking available transcripts for: {url}")
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'writesubtitles': False,
        'writeautomaticsub': False,
        'noprogress': True,
        'logger': SuppressYtDlpLogger(),
    }
    
    try:
        with suppress_stderr():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                manual_subs = info.get('subtitles', {})
                
                # Print actual output to stdout (not through logger)
                print("MANUAL SUBTITLES (Original):")
                if manual_subs:
                    for lang_code, formats in manual_subs.items():
                        lang_name = get_language_name(lang_code)
                        available_formats = [f['ext'] for f in formats]
                        print(f"  {lang_code} ({lang_name}) - Formats: {', '.join(available_formats)}")
                else:
                    print("  No manual subtitles available")
                
                total_langs = len(manual_subs)
                print(f"Total manual subtitle languages available: {total_langs}")
                
                # Show video title for context
                title = info.get('title', 'Unknown')
                print(f"Video: {title}")
                
                logger.debug(f"Found {total_langs} manual subtitle languages")
                logger.debug(f"Video title: {title}")
            
    except Exception as e:
        logger.error(f"Error extracting video info: {e}")
        sys.exit(1)


def get_language_name(lang_code):
    """Get human-readable language name from code."""
    # Basic language mapping - you could expand this
    lang_map = {
        'en': 'English',
        'es': 'Spanish', 
        'es-ES': 'Spanish (Spain)',
        'es-MX': 'Spanish (Mexico)',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'ja': 'Japanese',
        'ko': 'Korean',
        'zh': 'Chinese',
        'ar': 'Arabic',
        'hi': 'Hindi',
    }
    return lang_map.get(lang_code, lang_code.upper())


def download_transcript(url, language, output_file, subtitle_type, vtt_format, logger):
    """Download transcript for specified language."""
    format_type = "VTT" if vtt_format else "plain text"
    logger.info(f"Downloading {subtitle_type} transcript in '{language}' as {format_type} for: {url}")
    
    # Set default output filename based on format if not provided
    if output_file is None:
        output_file = './transcript.vtt' if vtt_format else './transcript.txt'
    
    # Check if output should go to stdout
    write_to_stdout = output_file == '-' or output_file.lower() == 'stdout'
    
    if not write_to_stdout:
        # Create output directory if it doesn't exist
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Output directory created: {output_path.parent}")
    
    # Create a temporary directory in /tmp for yt-dlp download
    with tempfile.TemporaryDirectory(prefix="youtube_transcript_") as temp_dir:
        temp_path = Path(temp_dir)
        logger.debug(f"Created temporary directory: {temp_path}")
        
        # Configure yt-dlp options
        ydl_opts = {
            'writesubtitles': subtitle_type in ['manual', 'both'],
            'writeautomaticsub': subtitle_type in ['auto', 'both'],
            'subtitleslangs': [language],
            'subtitlesformat': 'vtt',
            'skip_download': True,
            'outtmpl': f'{temp_path}/%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'noprogress': True,
            'logger': SuppressYtDlpLogger(),
        }
        
        try:
            with suppress_stderr():
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # First, check if the language is available
                    info = ydl.extract_info(url, download=False)
                    manual_subs = info.get('subtitles', {})
                    auto_subs = info.get('automatic_captions', {})
                    
                    has_manual = language in manual_subs
                    has_auto = language in auto_subs
                    
                    logger.debug(f"Manual subtitles available: {has_manual}")
                    logger.debug(f"Auto-generated subtitles available: {has_auto}")
                    
                    if subtitle_type == 'manual' and not has_manual:
                        logger.error(f"Manual subtitles not available for language '{language}'")
                        sys.exit(1)
                    elif subtitle_type == 'auto' and not has_auto:
                        logger.error(f"Auto-generated subtitles not available for language '{language}'")
                        sys.exit(1)
                    elif subtitle_type == 'both' and not (has_manual or has_auto):
                        logger.error(f"No subtitles available for language '{language}'")
                        sys.exit(1)
                    
                    # Download the subtitles
                    logger.debug("Starting subtitle download...")
                    ydl.download([url])
                    
                    if not write_to_stdout:
                        logger.info("Download completed successfully")
                    
                    # Find downloaded VTT files
                    vtt_files = list(temp_path.glob("*.vtt"))
                    logger.debug(f"Found VTT files: {[f.name for f in vtt_files]}")
                    
                    if vtt_files:
                        # Use the first VTT file found
                        vtt_file = vtt_files[0]
                        logger.debug(f"Processing VTT file: {vtt_file}")
                        
                        # Process based on format requested
                        if vtt_format:
                            # Save as VTT format
                            if write_to_stdout:
                                copy_vtt_to_stdout(vtt_file, logger)
                            else:
                                copy_vtt_to_file(vtt_file, output_path, logger)
                        else:
                            # Convert to plain text
                            if write_to_stdout:
                                convert_vtt_to_stdout(vtt_file, logger)
                            else:
                                convert_vtt_to_text_file(vtt_file, output_path, logger)
                        
                        # VTT files will be automatically deleted when temp directory is cleaned up
                        
                    else:
                        logger.warning("No .vtt files found. The transcript might not be available in the requested language.")
                        sys.exit(1)
                    
        except Exception as e:
            logger.error(f"Download failed: {e}")
            logger.debug("Exception details:", exc_info=True)
            sys.exit(1)
        
        # Temporary directory and all its contents are automatically deleted here
        logger.debug("Temporary directory cleaned up")


def copy_vtt_to_stdout(vtt_file, logger):
    """Copy VTT file content directly to stdout."""
    try:
        logger.debug(f"Copying VTT file to stdout: {vtt_file}")
        
        with open(vtt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Write VTT content directly to stdout
        print(content)
        logger.debug("VTT copy to stdout completed")
        
    except Exception as e:
        logger.error(f"Error copying VTT to stdout: {e}")
        logger.debug("Exception details:", exc_info=True)
        sys.exit(1)


def copy_vtt_to_file(vtt_file, output_file, logger):
    """Copy VTT file to specified output file."""
    try:
        # Ensure output_file is a Path object and resolve it
        output_path = Path(output_file).resolve()
        logger.debug(f"Copying VTT file: {vtt_file} -> {output_path}")
        
        # If the output path exists and is a directory, create a filename inside it
        if output_path.exists() and output_path.is_dir():
            output_path = output_path / "transcript.vtt"
            logger.warning(f"Output path is a directory, saving to: {output_path}")
        
        # Create parent directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Ensured parent directory exists: {output_path.parent}")
        
        with open(vtt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Write VTT content to specified output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Transcript saved in VTT format: {output_path}")
        logger.debug(f"File size: {output_path.stat().st_size} bytes")
        
    except Exception as e:
        logger.error(f"Error copying VTT to file: {e}")
        logger.debug(f"Debug info - output_file: {output_file}, type: {type(output_file)}")
        logger.debug(f"Debug info - resolved path: {Path(output_file).resolve()}")
        logger.debug("Exception details:", exc_info=True)
        sys.exit(1)


    """Convert VTT file to plain text and write to stdout."""
    try:
        logger.debug(f"Converting VTT file to stdout: {vtt_file}")
        
        with open(vtt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove VTT headers and timestamps
        lines = content.split('\n')
        text_lines = []
        
        for line in lines:
            line = line.strip()
            # Skip VTT headers, timestamps, style tags, and empty lines
            if (line and 
                not line.startswith('WEBVTT') and 
                not line.startswith('NOTE') and
                not line.startswith('STYLE') and
                '-->' not in line and
                not re.match(r'^\d+$', line) and
                not line.startswith('<') and
                not line.endswith('>')):
                
                # Remove timestamp tags like <00:01:23.456>
                line = re.sub(r'<[\d:.,]+>', '', line)
                # Remove other HTML-like tags
                line = re.sub(r'<[^>]+>', '', line)
                
                if line:  # Only add non-empty lines
                    text_lines.append(line)
        
        # Join lines and clean up extra whitespace
        text_content = '\n'.join(text_lines)
        text_content = re.sub(r'\n\s*\n', '\n\n', text_content)  # Clean up multiple newlines
        
        # Write plain text to stdout
        print(text_content)
        logger.debug("VTT conversion to stdout completed")
        
    except Exception as e:
        logger.error(f"Error converting to text: {e}")
        logger.debug("Exception details:", exc_info=True)
        sys.exit(1)


def convert_vtt_to_text_file(vtt_file, output_file, logger):
    """Convert VTT file to plain text and save to specified output file."""
    try:
        # Ensure output_file is a Path object and resolve it
        output_path = Path(output_file).resolve()
        logger.debug(f"Converting VTT to text file: {vtt_file} -> {output_path}")
        
        # If the output path exists and is a directory, create a filename inside it
        if output_path.exists() and output_path.is_dir():
            output_path = output_path / "transcript.txt"
            logger.warning(f"Output path is a directory, saving to: {output_path}")
        
        # Create parent directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Ensured parent directory exists: {output_path.parent}")
        
        with open(vtt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove VTT headers and timestamps
        lines = content.split('\n')
        text_lines = []
        
        for line in lines:
            line = line.strip()
            # Skip VTT headers, timestamps, style tags, and empty lines
            if (line and 
                not line.startswith('WEBVTT') and 
                not line.startswith('NOTE') and
                not line.startswith('STYLE') and
                '-->' not in line and
                not re.match(r'^\d+$', line) and
                not line.startswith('<') and
                not line.endswith('>')):
                
                # Remove timestamp tags like <00:01:23.456>
                line = re.sub(r'<[\d:.,]+>', '', line)
                # Remove other HTML-like tags
                line = re.sub(r'<[^>]+>', '', line)
                
                if line:  # Only add non-empty lines
                    text_lines.append(line)
        
        # Join lines and clean up extra whitespace
        text_content = '\n'.join(text_lines)
        text_content = re.sub(r'\n\s*\n', '\n\n', text_content)  # Clean up multiple newlines
        
        # Write plain text to specified output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
        
        logger.info(f"Transcript saved as plain text: {output_path}")
        logger.debug(f"File size: {output_path.stat().st_size} bytes")
        
    except Exception as e:
        logger.error(f"Error converting to text: {e}")
        logger.debug(f"Debug info - output_file: {output_file}, type: {type(output_file)}")
        logger.debug(f"Debug info - resolved path: {Path(output_file).resolve()}")
        logger.debug("Exception details:", exc_info=True)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="YouTube Transcript CLI Tool - List and download video transcripts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list https://youtu.be/5X6uoKA41h4
  %(prog)s --verbose list https://youtu.be/5X6uoKA41h4
  %(prog)s download https://youtu.be/5X6uoKA41h4 -l es
  %(prog)s download https://youtu.be/5X6uoKA41h4 -l en -t manual -o transcript_en.txt
  %(prog)s download https://youtu.be/5X6uoKA41h4 -l es --vtt -o transcript.vtt
  %(prog)s download https://youtu.be/5X6uoKA41h4 -l es -o ./transcripts/spanish.txt
  %(prog)s download https://youtu.be/5X6uoKA41h4 -l es -o - > transcript.txt
  %(prog)s download https://youtu.be/5X6uoKA41h4 -l es --vtt -o - > transcript.vtt
  %(prog)s download https://youtu.be/5X6uoKA41h4 -l es -o stdout | grep "keyword"
  %(prog)s --silent download https://youtu.be/5X6uoKA41h4 -l es -o - | head -10
  %(prog)s --verbose download https://youtu.be/5X6uoKA41h4 -l es -o transcript.txt
        """
    )
    
    # Add version flag
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    
    # Add mutually exclusive group for logging flags (global only)
    logging_group = parser.add_mutually_exclusive_group()
    logging_group.add_argument('--silent', action='store_true', 
                              help='Suppress all messages except output')
    logging_group.add_argument('--verbose', action='store_true',
                              help='Enable verbose logging with timestamps and debug information')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List command (no logging flags - they're global only)
    list_parser = subparsers.add_parser('list', help='List available transcript languages')
    list_parser.add_argument('url', help='YouTube video URL')
    
    # Download command (no logging flags - they're global only)
    download_parser = subparsers.add_parser('download', help='Download transcript')
    download_parser.add_argument('url', help='YouTube video URL')
    download_parser.add_argument('-l', '--language', required=True, 
                               help='Language code (e.g., en, es, fr)')
    download_parser.add_argument('-t', '--type', choices=['manual', 'auto', 'both'], 
                               default='both', help='Subtitle type (default: both)')
    download_parser.add_argument('-o', '--output', default=None, 
                               help='Output file path (default: ./transcript.txt or ./transcript.vtt based on format). Use "-" or "stdout" to write to stdout')
    download_parser.add_argument('--vtt', action='store_true',
                               help='Save transcript in VTT format instead of plain text')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Setup logging based on global arguments (much simpler!)
    logger = setup_logging(silent=args.silent, verbose=args.verbose)
    
    if not args.command:
        parser.print_help()
        return
    
    # Check if yt-dlp is available
    if importlib.util.find_spec("yt_dlp") is None:
        logger.error("yt-dlp module not found. Please install it with: pip install yt-dlp")
        sys.exit(1)
    
    logger.debug("yt-dlp module is available")
    
    logger.debug(f"Command: {args.command}")
    logger.debug(f"Arguments: {vars(args)}")
    
    if args.command == 'list':
        list_languages(args.url, logger)
    elif args.command == 'download':
        download_transcript(args.url, args.language, args.output, args.type, args.vtt, logger)


if __name__ == '__main__':
    main()
