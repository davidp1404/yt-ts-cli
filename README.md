# YouTube Transcript CLI (yt-ts-cli)

A command-line tool to list and download YouTube video transcripts (subtitles) and convert them to plain text format.

## Features

- 📝 List available manual subtitles for YouTube videos
- 🔽 Download transcripts in multiple languages
- 📄 Automatic conversion from VTT to clean plain text
- 🗂️ Support for manual and auto-generated subtitles
- 🧹 Automatic cleanup of temporary files
- 🌍 Support for multiple language codes (en, es, fr, de, etc.)
- 📤 Write to stdout for piping and command chaining

## Installation

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
   uv pip install dist/yt_ts_cli-0.2.0-py3-none-any.whl
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
yt-ts-cli list https://youtu.be/VIDEO_ID
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

### Command Options

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

# Download Spanish transcript
yt-ts-cli download https://youtu.be/5X6uoKA41h4 -l es-ES -o musculos_fuertes.txt

# Download only manual English subtitles
yt-ts-cli download https://youtu.be/5X6uoKA41h4 -l en -t manual -o english_manual.txt

# Write transcript to stdout
yt-ts-cli download https://youtu.be/5X6uoKA41h4 -l es -o -

# Pipe transcript to other commands
yt-ts-cli download https://youtu.be/5X6uoKA41h4 -l es -o stdout | head -10
yt-ts-cli download https://youtu.be/5X6uoKA41h4 -l es -o - | grep -i "muscle"
yt-ts-cli download https://youtu.be/5X6uoKA41h4 -l es -o - | wc -w
```

## Building and Distribution

### Build the Package
```bash
uv build
```

This creates both wheel (.whl) and source distribution (.tar.gz) files in the `dist/` directory.

### Install from Local Build
```bash
pip install dist/yt_ts_cli-0.2.0-py3-none-any.whl
```

### Share with Others
You can share the built wheel file with others:
```bash
# Build the wheel
uv build

# Share the wheel file
# Others can install it with:
pip install yt_ts_cli-0.2.0-py3-none-any.whl
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
pip install dist/yt_ts_cli-0.2.0-py3-none-any.whl --force-reinstall
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

## Changelog

### v0.2.0
- Added stdout support with `-o -` or `-o stdout`
- Status messages now go to stderr when writing to stdout
- Better support for piping and command chaining

### v0.1.0
- Initial release
- Basic list and download functionality
- Support for manual and auto-generated subtitles
- VTT to plain text conversion
