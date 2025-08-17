"""
Simple working tests for yt-ts-cli to verify basic functionality.
"""

import pytest
import sys
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from yt_ts_cli.main import get_language_name, main
from yt_ts_cli.logging_config import setup_logging, SuppressYtDlpLogger


class TestBasicFunctionality:
    """Test basic functionality that doesn't require complex mocking."""
    
    def test_get_language_name_basic(self):
        """Test basic language name mapping."""
        assert get_language_name("en") == "English"
        assert get_language_name("es") == "Spanish"
        assert get_language_name("fr") == "French"
        assert get_language_name("de") == "German"
        assert get_language_name("unknown") == "UNKNOWN"
        assert get_language_name("") == ""  # Empty string returns empty string
        assert get_language_name("xyz") == "XYZ"  # Unknown codes return uppercase
    
    def test_setup_logging_modes(self):
        """Test different logging modes."""
        # Test silent mode
        logger_silent = setup_logging(silent=True, verbose=False)
        assert logger_silent.level == 51  # CRITICAL + 1
        
        # Test verbose mode  
        logger_verbose = setup_logging(silent=False, verbose=True)
        assert logger_verbose.level == 10  # DEBUG
        
        # Test normal mode
        logger_normal = setup_logging(silent=False, verbose=False)
        assert logger_normal.level == 20  # INFO
    
    def test_suppress_ytdlp_logger(self):
        """Test that SuppressYtDlpLogger doesn't raise errors."""
        suppressor = SuppressYtDlpLogger()
        
        # All these should work without raising exceptions
        suppressor.debug("test message")
        suppressor.info("test message")
        suppressor.warning("test message")
        suppressor.error("test message")
        suppressor.critical("test message")


class TestCLIArguments:
    """Test CLI argument parsing."""
    
    def test_main_version_flag(self, capsys):
        """Test --version flag."""
        with patch('sys.argv', ['yt-ts-cli', '--version']):
            with pytest.raises(SystemExit):
                main()
        
        captured = capsys.readouterr()
        assert "yt-ts-cli 0.3.3" in captured.out
    
    def test_main_help_flag(self, capsys):
        """Test --help flag."""
        with patch('sys.argv', ['yt-ts-cli', '--help']):
            with pytest.raises(SystemExit):
                main()
        
        captured = capsys.readouterr()
        assert "usage:" in captured.out
        assert "YouTube Transcript CLI Tool" in captured.out
        assert "--silent" in captured.out
        assert "--verbose" in captured.out
    
    def test_main_no_command(self, capsys):
        """Test main with no command shows help and returns."""
        with patch('sys.argv', ['yt-ts-cli']):
            main()  # Should not raise SystemExit, just return
        
        captured = capsys.readouterr()
        assert "usage:" in captured.out
        assert "YouTube Transcript CLI Tool" in captured.out
    
    def test_main_mutual_exclusion(self, capsys):
        """Test that --silent and --verbose are mutually exclusive."""
        with patch('sys.argv', ['yt-ts-cli', '--silent', '--verbose', 'list', 'https://example.com']):
            with pytest.raises(SystemExit):
                main()
        
        captured = capsys.readouterr()
        assert "not allowed with argument" in captured.err


class TestModuleAvailability:
    """Test module availability checking."""
    
    @patch('importlib.util.find_spec')
    def test_main_missing_ytdlp(self, mock_find_spec, capsys):
        """Test main function when yt-dlp is not available."""
        mock_find_spec.return_value = None
        
        with patch('sys.argv', ['yt-ts-cli', 'list', 'https://example.com']):
            with pytest.raises(SystemExit):
                main()
        
        captured = capsys.readouterr()
        assert "yt-dlp module not found" in captured.err
    
    @patch('importlib.util.find_spec')
    def test_main_ytdlp_available(self, mock_find_spec):
        """Test that main continues when yt-dlp is available."""
        mock_find_spec.return_value = MagicMock()  # yt-dlp available
        
        # Mock the list_languages function to avoid actual network calls
        with patch('yt_ts_cli.main.list_languages') as mock_list:
            with patch('sys.argv', ['yt-ts-cli', 'list', 'https://youtube.com/watch?v=test']):
                main()
            
            # Verify that list_languages was called
            mock_list.assert_called_once()
    
    def test_vtt_flag_in_help(self, capsys):
        """Test that --vtt flag appears in download command help."""
        with patch('sys.argv', ['yt-ts-cli', 'download', '--help']):
            with pytest.raises(SystemExit):
                main()
        
        captured = capsys.readouterr()
        assert "--vtt" in captured.out
        assert "Save transcript in VTT format instead of plain text" in captured.out
    
    @patch('importlib.util.find_spec')
    def test_main_download_with_vtt_flag(self, mock_find_spec):
        """Test that main accepts --vtt flag for download command."""
        mock_find_spec.return_value = MagicMock()  # yt-dlp available
        
        # Mock the download_transcript function to avoid actual network calls
        with patch('yt_ts_cli.main.download_transcript') as mock_download:
            with patch('sys.argv', ['yt-ts-cli', 'download', 'https://youtube.com/watch?v=test', '-l', 'en', '--vtt']):
                main()
            
            # Verify that download_transcript was called with vtt_format=True
            mock_download.assert_called_once()
            args = mock_download.call_args[0]  # positional arguments
            assert args[4] == True  # vtt_format parameter should be True


if __name__ == '__main__':
    pytest.main([__file__])
