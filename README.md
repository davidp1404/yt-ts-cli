# YouTube Transcript CLI (yt-ts-cli)

A command-line tool to list and download YouTube video transcripts (subtitles) and convert them to plain text format.

## Features

- 📝 List available manual subtitles for YouTube videos
- 🔽 Download transcripts in multiple languages
- 📄 Automatic conversion from VTT to clean plain text
- 🗂️ Support for manual and auto-generated subtitles
- 🧹 Automatic cleanup of temporary files
- 🌍 Support for multiple language codes (en, es, fr, de, etc.)

## Installation

### From PyPI (when published)
```bash
pip install yt-ts-cli
```

### From Source
```bash
git clone <repository-url>
cd yt-ts-cli
uv sync
uv run yt-ts-cli --help
```

### Development Installation
```bash
git clone <repository-url>
cd yt-ts-cli
uv sync --dev
uv run yt-ts-cli --help
```

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
```

### Command Options

#### `list` command
- `url`: YouTube video URL

#### `download` command
- `url`: YouTube video URL
- `-l, --language`: Language code (required) - e.g., en, es, fr, de
- `-t, --type`: Subtitle type - choices: manual, auto, both (default: both)
- `-o, --output`: Output file path (default: ./transcript.txt)

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
```

## Requirements

- Python 3.8+
- yt-dlp

## Building and Distribution

### Build the Package
```bash
uv build
```

This creates both wheel (.whl) and source distribution (.tar.gz) files in the `dist/` directory.

### Install from Local Build
```bash
pip install dist/yt_ts_cli-0.1.0-py3-none-any.whl
```

## Development

### Setup Development Environment
```bash
uv sync --dev
```

### Run Tests
```bash
uv run pytest
```

### Format Code
```bash
uv run black src/
uv run isort src/
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Troubleshooting

### Common Issues

1. **"yt-dlp module not found"**
   - Install yt-dlp: `pip install yt-dlp`

2. **"No subtitles available"**
   - Check if the video has subtitles using the `list` command first
   - Try different language codes

3. **Permission errors**
   - Make sure you have write permissions to the output directory
   - Try using a different output path

## Changelog

### v0.1.0
- Initial release
- Basic list and download functionality
- Support for manual and auto-generated subtitles
- VTT to plain text conversion
