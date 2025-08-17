# YouTube Transcript CLI (yt-ts-cli)

A professional command-line tool to list and download YouTube video transcripts (subtitles) and convert them to plain text format.

## Features

- List available manual subtitles for YouTube videos
- Download transcripts in multiple languages
- Automatic conversion from VTT to clean plain text
- Support for manual and auto-generated subtitles
- Automatic cleanup of temporary files
- Support for multiple language codes (en, es, fr, de, etc.)
- Write to stdout for piping and command chaining
- Professional logging with configurable verbosity levels
- Silent mode for clean output in scripts and pipelines

## Installation

### From Repository Clone

1. **Clone the repository:**
   ```bash
   git clone https://github.com/davidp1404/yt-ts-cli.git
   cd yt-ts-cli
   ```

2. **Install globally using UV:**
   ```bash
   uv pip install .
   yt-ts-cli --help
   ```

3. **Or install from built wheel:**
   ```bash
   uv build
   uv pip install dist/yt_ts_cli-0.3.1-py3-none-any.whl
   yt-ts-cli --help
   ```

4. **Or use traditional pip:**
   ```bash
   pip install .
   yt-ts-cli --help
   ```

### Development Installation

For development and contributing:
```bash
git clone https://github.com/davidp1404/yt-ts-cli.git
cd yt-ts-cli
uv sync --dev
# Run from source (within project directory)
uv run yt-ts-cli --help
```

### Requirements

- Python 3.8+
- UV package manager (recommended) or pip
- yt-dlp (automatically installed as dependency)

## Usage

### List Available Transcripts
```bash
# Basic listing
yt-ts-cli list https://youtu.be/VIDEO_ID

# Verbose listing with debug information
yt-ts-cli list --verbose https://youtu.be/VIDEO_ID

# Silent listing (minimal output)
yt-ts-cli list --silent https://youtu.be/VIDEO_ID
```

### Download Transcript
```bash
# Download Spanish transcript to default file (transcript.txt)
yt-ts-cli download https://youtu.be/VIDEO_ID -l es

# Download English manual transcript to specific file
yt-ts-cli download https://youtu.be/VIDEO_ID -l en -t manual -o transcript_en.txt

# Download to a file in a subdirectory
yt-ts-cli download https://youtu.be/VIDEO_ID -l es -o ./transcripts/spanish.txt

# Write to stdout (useful for piping)
yt-ts-cli download https://youtu.be/VIDEO_ID -l es -o -

# Write to stdout and redirect to file
yt-ts-cli download https://youtu.be/VIDEO_ID -l es -o stdout > transcript.txt

# Pipe to other commands
yt-ts-cli download https://youtu.be/VIDEO_ID -l es -o - | grep "keyword"
yt-ts-cli download https://youtu.be/VIDEO_ID -l es -o - | wc -w
```

### Logging and Verbosity Options

```bash
# Silent mode - suppress all messages except output
yt-ts-cli --silent download https://youtu.be/VIDEO_ID -l es -o -

# Verbose mode - detailed logging with timestamps
yt-ts-cli --verbose download https://youtu.be/VIDEO_ID -l es -o transcript.txt

# Normal mode - standard informational messages (default)
yt-ts-cli download https://youtu.be/VIDEO_ID -l es -o transcript.txt

# Silent listing
yt-ts-cli --silent list https://youtu.be/VIDEO_ID

# Verbose listing
yt-ts-cli --verbose list https://youtu.be/VIDEO_ID
```

### Command Options

#### Global Options
- `--version`: Show version information and exit
- `--silent`: Suppress all messages except output (mutually exclusive with --verbose)
- `--verbose`: Enable detailed logging with timestamps and debug information (mutually exclusive with --silent)

#### `list` command
- `url`: YouTube video URL

#### `download` command
- `url`: YouTube video URL
- `-l, --language`: Language code (required) - e.g., en, es, fr, de
- `-t, --type`: Subtitle type - choices: manual, auto, both (default: both)
- `-o, --output`: Output file path (default: ./transcript.txt). Use "-" or "stdout" to write to stdout

### Language Codes

Common language codes supported:
- `en` - English
- `es` - Spanish
- `es-ES` - Spanish (Spain)
- `es-MX` - Spanish (Mexico)
- `fr` - French
- `de` - German
- `it` - Italian
- `pt` - Portuguese
- `ru` - Russian
- `ja` - Japanese
- `ko` - Korean
- `zh` - Chinese
- `ar` - Arabic
- `hi` - Hindi

## Examples

```bash
# List all available manual subtitles
yt-ts-cli list https://youtu.be/5X6uoKA41h4

# Download Spanish transcript with standard logging
yt-ts-cli download https://youtu.be/5X6uoKA41h4 -l es-ES -o musculos_fuertes.txt

# Download only manual English subtitles with verbose logging
yt-ts-cli download --verbose https://youtu.be/5X6uoKA41h4 -l en -t manual -o english_manual.txt

# Write transcript to stdout in silent mode (perfect for piping)
yt-ts-cli download --silent https://youtu.be/5X6uoKA41h4 -l es -o -

# Pipe transcript to other commands with clean output
yt-ts-cli download --silent https://youtu.be/5X6uoKA41h4 -l es -o stdout | head -10
yt-ts-cli download --silent https://youtu.be/5X6uoKA41h4 -l es -o - | grep -i "muscle"
yt-ts-cli download --silent https://youtu.be/5X6uoKA41h4 -l es -o - | wc -w

# Debug mode for troubleshooting
yt-ts-cli list --verbose https://youtu.be/5X6uoKA41h4

# Show version
yt-ts-cli --version
```

## Building and Distribution

### Build the Package
```bash
uv build
```

This creates both wheel (.whl) and source distribution (.tar.gz) files in the `dist/` directory.

### Install from Local Build
```bash
pip install dist/yt_ts_cli-0.3.1-py3-none-any.whl
```

### Share with Others
You can share the built wheel file with others:
```bash
# Build the wheel
uv build

# Share the wheel file
# Others can install it with:
pip install yt_ts_cli-0.3.1-py3-none-any.whl
```

## Development

### Setup Development Environment
```bash
git clone <repository-url>
cd yt-ts-cli
uv sync --dev
```

### Run from Source (without installing)
```bash
# Within the project directory
uv run yt-ts-cli --help
```

### Install for Global Use
```bash
# Install globally with UV
uv pip install .
# Now available system-wide
yt-ts-cli --help
```

### Build and Test
```bash
# Build the package
uv build

# Test the built wheel
pip install dist/yt_ts_cli-0.3.1-py3-none-any.whl --force-reinstall
yt-ts-cli --help
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test your changes with `uv run yt-ts-cli`
5. Build and test the package with `uv build`
6. Submit a pull request

## Troubleshooting

### Common Issues

1. **"yt-dlp module not found"**
   - This should be automatically installed as a dependency
   - If issues persist, manually install: `pip install yt-dlp`

2. **"No subtitles available"**
   - Check if the video has subtitles using the `list` command first
   - Try different language codes
   - Some videos only have auto-generated subtitles

3. **Permission errors**
   - Make sure you have write permissions to the output directory
   - Try using a different output path or write to stdout with `-o -`

4. **UV not found**
   - Install UV: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Or use pip instead: `pip install .`

5. **Debugging issues**
   - Use `--verbose` flag to see detailed logging information
   - Check the debug output for specific error details

## Logging Levels

The application uses professional logging with three levels:

- **Silent Mode** (`--silent`): No output except the actual transcript content. Perfect for scripting and piping.
- **Normal Mode** (default): Standard informational messages about the process.
- **Verbose Mode** (`--verbose`): Detailed debug information with timestamps for troubleshooting.

All log messages are sent to stderr, ensuring they don't interfere with stdout output when piping or redirecting transcript content.

## Changelog

### v0.3.1
- Added `--silent` flag to suppress messages
- Added `--version` flag to display version information
- Enhanced silent mode to suppress ALL messages (including app messages)
- Improved yt-dlp output suppression with better error handling
- Silent mode now provides completely clean output for piping

### v0.2.0
- Added stdout support with `-o -` or `-o stdout`
- Status messages now go to stderr when writing to stdout
- Better support for piping and command chaining

### v0.1.0
- Initial release
- Basic list and download functionality
- Support for manual and auto-generated subtitles
- VTT to plain text conversion
