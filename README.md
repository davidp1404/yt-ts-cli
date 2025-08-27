[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/davidp1404/yt-ts-cli)



# YouTube Transcript CLI (yt-ts-cli)

A simple command-line tool to list and download YouTube video transcripts (subtitles) and convert them to plain text format or keep them in VTT format.
It is part of the preliminary work to develop an MCP agent.

## Features

- List available manual subtitles for YouTube videos
- Download transcripts in multiple languages
- Automatic conversion from VTT to clean plain text
- Option to save transcripts in original VTT format
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
   uv pip install dist/yt_ts_cli-0.3.3-py3-none-any.whl
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
yt-ts-cli --verbose list https://youtu.be/VIDEO_ID

# Silent listing (minimal output)
yt-ts-cli --silent list https://youtu.be/VIDEO_ID
```

### Download Transcript
```bash
# Download transcript in original video language (auto-detected)
yt-ts-cli download https://youtu.be/VIDEO_ID

# Download Spanish transcript to default file (transcript.txt)
yt-ts-cli download https://youtu.be/VIDEO_ID -l es

# Download English manual transcript to specific file
yt-ts-cli download https://youtu.be/VIDEO_ID -l en -t manual -o transcript_en.txt

# Download transcript in VTT format (preserves timing and formatting)
yt-ts-cli download https://youtu.be/VIDEO_ID --vtt -o transcript.vtt

# Download transcript in original language as VTT format
yt-ts-cli download https://youtu.be/VIDEO_ID --vtt -o transcript.vtt

# Download to a file in a subdirectory
yt-ts-cli download https://youtu.be/VIDEO_ID -l es -o ./transcripts/spanish.txt

# Write to stdout (useful for piping) - uses original language
yt-ts-cli download https://youtu.be/VIDEO_ID -o -

# Write specific language to stdout
yt-ts-cli download https://youtu.be/VIDEO_ID -l es -o -

# Write VTT format to stdout
yt-ts-cli download https://youtu.be/VIDEO_ID --vtt -o -

# Write to stdout and redirect to file
yt-ts-cli download https://youtu.be/VIDEO_ID -o stdout > transcript.txt

# Pipe to other commands
yt-ts-cli download https://youtu.be/VIDEO_ID -o - | grep "keyword"
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
- `-l, --language`: Language code (optional) - e.g., en, es, fr, de. If not specified, automatically detects and uses the original video language
- `-t, --type`: Subtitle type - choices: manual, auto, both (default: both)
- `-o, --output`: Output file path (default: ./transcript.txt or ./transcript.vtt based on format). Use "-" or "stdout" to write to stdout
- `--vtt`: Save transcript in VTT format instead of plain text

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

# Download transcript in original language (auto-detected)
yt-ts-cli download https://youtu.be/5X6uoKA41h4

# Download Spanish transcript with standard logging
yt-ts-cli download https://youtu.be/5X6uoKA41h4 -l es-ES -o musculos_fuertes.txt

# Download Spanish transcript in VTT format (preserves timing)
yt-ts-cli download https://youtu.be/5X6uoKA41h4 -l es-ES --vtt -o musculos_fuertes.vtt

# Download only manual English subtitles with verbose logging
yt-ts-cli download --verbose https://youtu.be/5X6uoKA41h4 -l en -t manual -o english_manual.txt

# Write transcript to stdout in silent mode (perfect for piping) - uses original language
yt-ts-cli download --silent https://youtu.be/5X6uoKA41h4 -o -

# Write specific language transcript to stdout
yt-ts-cli download --silent https://youtu.be/5X6uoKA41h4 -l es -o -

# Write VTT format to stdout
yt-ts-cli download --silent https://youtu.be/5X6uoKA41h4 -l es --vtt -o -

# Pipe transcript to other commands with clean output
yt-ts-cli download --silent https://youtu.be/5X6uoKA41h4 -o stdout | head -10
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
pip install dist/yt_ts_cli-0.3.3-py3-none-any.whl
```

### Share with Others
You can share the built wheel file with others:
```bash
# Build the wheel
uv build

# Share the wheel file
# Others can install it with:
pip install yt_ts_cli-0.3.3-py3-none-any.whl
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
pip install dist/yt_ts_cli-0.3.3-py3-none-any.whl --force-reinstall
yt-ts-cli --help
```

## Testing

The project includes a comprehensive test suite to ensure reliability and correctness.

### Running Tests

```bash
# Run fast unit tests (no network calls)
python run_tests.py unit

# Run integration tests with real YouTube URLs (slow)
python run_tests.py integration

# Run all tests (unit + integration)
python run_tests.py all
```

### Test Types

#### **Unit Tests** (`tests/test_simple.py`) - Fast ⚡
- **No network calls** - Run offline
- Test CLI argument parsing, logging, utility functions
- **9 tests, ~0.2 seconds**
- Safe to run frequently during development

#### **Integration Tests** (`tests/test_integration.py`) - Slow 🌐
- **Real YouTube URLs** - Requires internet connection
- Test actual video listing and transcript downloading
- **Uses real videos** including the Spanish medical video you mentioned
- **~80+ seconds** - Network dependent
- May fail due to video availability or network issues

### Test Coverage

The test suite covers:

- **CLI Argument Parsing**: Version flags, help text, mutual exclusion
- **Logging Configuration**: Silent, verbose, and normal modes  
- **Language Mapping**: Language code to human-readable name conversion
- **Module Availability**: yt-dlp dependency checking
- **Error Handling**: Missing dependencies, invalid arguments
- **Real Video Processing**: Actual YouTube video listing and downloading
- **File Operations**: VTT to text conversion, stdout output
- **Network Error Handling**: Invalid URLs, unavailable languages

### Test Structure

```
tests/
├── __init__.py          # Test package
├── conftest.py          # Shared fixtures and configuration
├── test_simple.py       # Basic functionality tests (working)
├── test_main.py         # Comprehensive main functionality tests
└── test_edge_cases.py   # Edge cases and error handling tests
```

### Adding New Tests

When adding new functionality:

1. Add tests to the appropriate test file
2. Use descriptive test names that explain what is being tested
3. Include both positive and negative test cases
4. Mock external dependencies (yt-dlp, file system, network calls)
5. Run the test suite to ensure all tests pass

### Test Dependencies

The test suite uses:
- **pytest**: Test framework
- **pytest-mock**: Mocking utilities
- **unittest.mock**: Python's built-in mocking (via pytest-mock)

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

### v0.4.0
- **BREAKING CHANGE**: Made `-l/--language` parameter optional for download command
- Added automatic original language detection when no language is specified
- Language detection prioritizes manual subtitles over auto-generated ones
- Falls back to common languages (en, es, fr, de, etc.) when video metadata is unavailable
- Updated help examples to show usage without language parameter
- Enhanced user experience by removing the need to specify language for most use cases

### v0.3.3
- Added `--vtt` flag to save transcripts in original VTT format instead of plain text
- VTT format preserves timing information and original subtitle formatting
- Default output filename now changes based on format (transcript.txt vs transcript.vtt)
- Added VTT format support for stdout output
- Enhanced help examples to demonstrate VTT format usage

### v0.3.2
- Added comprehensive pytest test suite with both unit and integration tests
- **Unit Tests**: Fast offline tests for CLI parsing, logging, and utilities (9 tests)
- **Integration Tests**: Real YouTube URL tests with actual video downloads (11 tests)
- Added test runner script (`run_tests.py`) with support for different test types
- Tests now use diverse YouTube content (Spanish medical, TED talks, popular videos)
- Fixed linter issues (E713) for better code style compliance
- Improved error handling in integration tests for network issues
- Added pytest configuration and dev dependencies to pyproject.toml
- Enhanced test coverage for real-world scenarios and edge cases

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
