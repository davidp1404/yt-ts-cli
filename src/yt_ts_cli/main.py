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
from pathlib import Path
import yt_dlp
import re

from . import __version__


class SuppressLogger:
    """Custom logger that suppresses all yt-dlp output."""
    def debug(self, msg): pass
    def info(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass


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


def list_languages(url, silent=False):
    """List available subtitle languages for a YouTube video."""
    if not silent:
        print(f"Checking available transcripts for: {url}")
        print("-" * 60)
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'writesubtitles': False,
        'writeautomaticsub': False,
        'noprogress': True,
    }
    
    if silent:
        ydl_opts['logger'] = SuppressLogger()
    
    try:
        # Suppress yt-dlp stderr output when in silent mode
        context_manager = suppress_stderr() if silent else contextlib.nullcontext()
        
        with context_manager:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                manual_subs = info.get('subtitles', {})
                
                print("📝 MANUAL SUBTITLES (Original):")
                if manual_subs:
                    for lang_code, formats in manual_subs.items():
                        lang_name = get_language_name(lang_code)
                        available_formats = [f['ext'] for f in formats]
                        print(f"  ✓ {lang_code} ({lang_name}) - Formats: {', '.join(available_formats)}")
                else:
                    print("  ❌ No manual subtitles available")
                
                total_langs = len(manual_subs)
                print(f"\nTotal manual subtitle languages available: {total_langs}")
                
                # Show video title for context
                title = info.get('title', 'Unknown')
                print(f"Video: {title}")
            
    except Exception as e:
        if not silent:
            print(f"❌ Error extracting video info: {e}")
        else:
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


def download_transcript(url, language, output_file, subtitle_type, silent=False):
    """Download transcript for specified language."""
    if not silent:
        print(f"Downloading {subtitle_type} transcript in '{language}' for: {url}", file=sys.stderr)
    
    # Check if output should go to stdout
    write_to_stdout = output_file == '-' or output_file.lower() == 'stdout'
    
    if not write_to_stdout:
        # Create output directory if it doesn't exist
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create a temporary directory in /tmp for yt-dlp download
    with tempfile.TemporaryDirectory(prefix="youtube_transcript_") as temp_dir:
        temp_path = Path(temp_dir)
        
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
        }
        
        if silent:
            ydl_opts['logger'] = SuppressLogger()
        
        try:
            # Suppress yt-dlp stderr output when in silent mode
            context_manager = suppress_stderr() if silent else contextlib.nullcontext()
            
            with context_manager:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # First, check if the language is available
                    info = ydl.extract_info(url, download=False)
                    manual_subs = info.get('subtitles', {})
                    auto_subs = info.get('automatic_captions', {})
                    
                    has_manual = language in manual_subs
                    has_auto = language in auto_subs
                    
                    if subtitle_type == 'manual' and not has_manual:
                        if not silent:
                            print(f"❌ Manual subtitles not available for language '{language}'", file=sys.stderr)
                        sys.exit(1)
                    elif subtitle_type == 'auto' and not has_auto:
                        if not silent:
                            print(f"❌ Auto-generated subtitles not available for language '{language}'", file=sys.stderr)
                        sys.exit(1)
                    elif subtitle_type == 'both' and not (has_manual or has_auto):
                        if not silent:
                            print(f"❌ No subtitles available for language '{language}'", file=sys.stderr)
                        sys.exit(1)
                    
                    # Download the subtitles
                    ydl.download([url])
                    
                    if not write_to_stdout and not silent:
                        print("✅ Download completed successfully!", file=sys.stderr)
                    
                    # Find downloaded VTT files
                    vtt_files = list(temp_path.glob("*.vtt"))
                    if vtt_files:
                        # Use the first VTT file found
                        vtt_file = vtt_files[0]
                        if not write_to_stdout and not silent:
                            print(f"📄 Downloaded: {vtt_file}", file=sys.stderr)
                        
                        # Convert to plain text
                        if write_to_stdout:
                            convert_vtt_to_stdout(vtt_file)
                        else:
                            convert_vtt_to_text_file(vtt_file, output_path, silent)
                        
                        # VTT files will be automatically deleted when temp directory is cleaned up
                        
                    else:
                        if not silent:
                            print("⚠️  No .vtt files found. The transcript might not be available in the requested language.", file=sys.stderr)
                        sys.exit(1)
                    
        except Exception as e:
            if not silent:
                print(f"❌ Download failed: {e}", file=sys.stderr)
            sys.exit(1)
        
        # Temporary directory and all its contents are automatically deleted here


def convert_vtt_to_stdout(vtt_file):
    """Convert VTT file to plain text and write to stdout."""
    try:
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
                not '-->' in line and
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
        
    except Exception as e:
        print(f"❌ Error converting to text: {e}", file=sys.stderr)


def convert_vtt_to_text_file(vtt_file, output_file, silent=False):
    """Convert VTT file to plain text and save to specified output file."""
    try:
        # Ensure output_file is a Path object and resolve it
        output_path = Path(output_file).resolve()
        
        # If the output path exists and is a directory, create a filename inside it
        if output_path.exists() and output_path.is_dir():
            output_path = output_path / "transcript.txt"
            if not silent:
                print(f"⚠️  Output path is a directory, saving to: {output_path}", file=sys.stderr)
        
        # Create parent directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
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
                not '-->' in line and
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
        
        if not silent:
            print(f"✅ Transcript saved as plain text: {output_path}", file=sys.stderr)
        
    except Exception as e:
        if not silent:
            print(f"❌ Error converting to text: {e}", file=sys.stderr)
            print(f"Debug info - output_file: {output_file}, type: {type(output_file)}", file=sys.stderr)
            print(f"Debug info - resolved path: {Path(output_file).resolve()}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="YouTube Transcript CLI Tool - List and download video transcripts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list https://youtu.be/5X6uoKA41h4
  %(prog)s download https://youtu.be/5X6uoKA41h4 -l es
  %(prog)s download https://youtu.be/5X6uoKA41h4 -l en -t manual -o transcript_en.txt
  %(prog)s download https://youtu.be/5X6uoKA41h4 -l es -o ./transcripts/spanish.txt
  %(prog)s download https://youtu.be/5X6uoKA41h4 -l es -o - > transcript.txt
  %(prog)s download https://youtu.be/5X6uoKA41h4 -l es -o stdout | grep "keyword"
  %(prog)s --silent download https://youtu.be/5X6uoKA41h4 -l es -o - | head -10
        """
    )
    
    # Add version flag
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    
    # Add global silent flag
    parser.add_argument('--silent', action='store_true', 
                       help='Suppress all messages except output (disabled by default)')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List available transcript languages')
    list_parser.add_argument('url', help='YouTube video URL')
    
    # Download command
    download_parser = subparsers.add_parser('download', help='Download transcript')
    download_parser.add_argument('url', help='YouTube video URL')
    download_parser.add_argument('-l', '--language', required=True, 
                               help='Language code (e.g., en, es, fr)')
    download_parser.add_argument('-t', '--type', choices=['manual', 'auto', 'both'], 
                               default='both', help='Subtitle type (default: both)')
    download_parser.add_argument('-o', '--output', default='./transcript.txt', 
                               help='Output file path (default: ./transcript.txt). Use "-" or "stdout" to write to stdout')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Check if yt-dlp is available
    try:
        import yt_dlp
    except ImportError:
        if not args.silent:
            print("❌ Error: yt-dlp module not found. Please install it with: pip install yt-dlp")
        sys.exit(1)
    
    if args.command == 'list':
        list_languages(args.url, args.silent)
    elif args.command == 'download':
        download_transcript(args.url, args.language, args.output, args.type, args.silent)


if __name__ == '__main__':
    main()
