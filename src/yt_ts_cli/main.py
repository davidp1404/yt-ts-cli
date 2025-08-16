#!/usr/bin/env python3
"""
YouTube Transcript CLI Tool
A command-line tool to list and download YouTube video transcripts using yt-dlp Python module.
"""

import argparse
import sys
import os
import tempfile
from pathlib import Path
import yt_dlp
import re


def list_languages(url):
    """List available subtitle languages for a YouTube video."""
    print(f"Checking available transcripts for: {url}")
    print("-" * 60)
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'writesubtitles': False,
        'writeautomaticsub': False,
    }
    
    try:
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
        print(f"❌ Error extracting video info: {e}")


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


def download_transcript(url, language, output_file, subtitle_type):
    """Download transcript for specified language."""
    print(f"Downloading {subtitle_type} transcript in '{language}' for: {url}")
    
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
            'quiet': False,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # First, check if the language is available
                info = ydl.extract_info(url, download=False)
                manual_subs = info.get('subtitles', {})
                auto_subs = info.get('automatic_captions', {})
                
                has_manual = language in manual_subs
                has_auto = language in auto_subs
                
                if subtitle_type == 'manual' and not has_manual:
                    print(f"❌ Manual subtitles not available for language '{language}'")
                    return
                elif subtitle_type == 'auto' and not has_auto:
                    print(f"❌ Auto-generated subtitles not available for language '{language}'")
                    return
                elif subtitle_type == 'both' and not (has_manual or has_auto):
                    print(f"❌ No subtitles available for language '{language}'")
                    return
                
                # Download the subtitles
                ydl.download([url])
                
                print("✅ Download completed successfully!")
                
                # Find downloaded VTT files
                vtt_files = list(temp_path.glob("*.vtt"))
                if vtt_files:
                    # Use the first VTT file found
                    vtt_file = vtt_files[0]
                    print(f"📄 Downloaded: {vtt_file}")
                    
                    # Convert to plain text and save to specified output file
                    convert_vtt_to_text_file(vtt_file, output_path)
                    
                    # VTT files will be automatically deleted when temp directory is cleaned up
                    
                else:
                    print("⚠️  No .vtt files found. The transcript might not be available in the requested language.")
                    
        except Exception as e:
            print(f"❌ Download failed: {e}")
        
        # Temporary directory and all its contents are automatically deleted here


def convert_vtt_to_text_file(vtt_file, output_file):
    """Convert VTT file to plain text and save to specified output file."""
    try:
        # Ensure output_file is a Path object and resolve it
        output_path = Path(output_file).resolve()
        
        # If the output path exists and is a directory, create a filename inside it
        if output_path.exists() and output_path.is_dir():
            output_path = output_path / "transcript.txt"
            print(f"⚠️  Output path is a directory, saving to: {output_path}")
        
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
        
        print(f"✅ Transcript saved as plain text: {output_path}")
        
    except Exception as e:
        print(f"❌ Error converting to text: {e}")
        print(f"Debug info - output_file: {output_file}, type: {type(output_file)}")
        print(f"Debug info - resolved path: {Path(output_file).resolve()}")


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
        """
    )
    
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
                               help='Output file path (default: ./transcript.txt)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Check if yt-dlp is available
    try:
        import yt_dlp
    except ImportError:
        print("❌ Error: yt-dlp module not found. Please install it with: pip install yt-dlp")
        sys.exit(1)
    
    if args.command == 'list':
        list_languages(args.url)
    elif args.command == 'download':
        download_transcript(args.url, args.language, args.output, args.type)


if __name__ == '__main__':
    main()
