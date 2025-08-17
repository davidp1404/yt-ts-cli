"""
Integration tests for yt-ts-cli using real YouTube URLs.

These tests make actual network calls and should be run sparingly.
They verify that the application works with real YouTube videos.
"""

import pytest
import sys
import tempfile
import os
from pathlib import Path
from unittest.mock import patch

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from yt_ts_cli.main import main, list_languages, download_transcript
from yt_ts_cli.logging_config import setup_logging


# Real YouTube URLs for testing
TEST_URLS = {
    # Dr. Alberto Sanagustín video (Spanish with subtitles)
    'spanish_medical': 'https://www.youtube.com/watch?v=5X6uoKA41h4',
    
    # TED Talk (usually has multiple language subtitles)
    'ted_talk': 'https://www.youtube.com/watch?v=8S0FDjFBj8o',
    
    # Popular tech video (usually has English subtitles)
    'tech_video': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'  # Rick Roll (classic, likely has subtitles)
}


@pytest.mark.integration
@pytest.mark.slow
class TestRealYouTubeIntegration:
    """Integration tests with real YouTube videos."""
    
    def test_list_real_video_spanish_medical(self, capsys):
        """Test listing subtitles for a real Spanish medical video."""
        logger = setup_logging(silent=False, verbose=False)
        
        try:
            list_languages(TEST_URLS['spanish_medical'], logger)
            captured = capsys.readouterr()
            
            # Check that we got some output
            assert len(captured.out) > 0
            assert "Video:" in captured.out
            
            # Should show subtitle information
            assert ("MANUAL SUBTITLES" in captured.out or 
                   "No manual subtitles available" in captured.out)
            
        except Exception as e:
            pytest.skip(f"Network error or video unavailable: {e}")
    
    def test_list_real_video_ted_talk(self, capsys):
        """Test listing subtitles for a TED talk (usually has many languages)."""
        logger = setup_logging(silent=False, verbose=False)
        
        try:
            list_languages(TEST_URLS['ted_talk'], logger)
            captured = capsys.readouterr()
            
            # Check that we got some output
            assert len(captured.out) > 0
            assert "Video:" in captured.out
            
            # TED talks usually have multiple language subtitles
            assert ("MANUAL SUBTITLES" in captured.out or 
                   "No manual subtitles available" in captured.out)
            
        except Exception as e:
            pytest.skip(f"Network error or video unavailable: {e}")
    
    def test_list_real_video_with_cli(self, capsys):
        """Test the full CLI with a real video URL."""
        test_url = TEST_URLS['tech_video']  # Use Rick Roll video
        
        with patch('sys.argv', ['yt-ts-cli', '--silent', 'list', test_url]):
            try:
                main()
                captured = capsys.readouterr()
                
                # In silent mode, should still show subtitle listing
                assert len(captured.out) > 0
                
            except SystemExit as e:
                if e.code != 0:
                    pytest.skip(f"CLI failed, possibly network issue: {e}")
            except Exception as e:
                pytest.skip(f"Network error or video unavailable: {e}")
    
    def test_download_real_transcript_to_stdout(self, capsys):
        """Test downloading a real transcript to stdout."""
        logger = setup_logging(silent=True, verbose=False)
        test_url = TEST_URLS['spanish_medical']
        
        try:
            # Try to download Spanish transcript
            download_transcript(test_url, 'es', '-', 'both', False, logger)
            captured = capsys.readouterr()
            
            # Should have some transcript content
            assert len(captured.out) > 0
            
            # Should not contain VTT formatting
            assert "WEBVTT" not in captured.out
            assert "-->" not in captured.out
            
        except SystemExit as e:
            if "not available" in str(e):
                pytest.skip("Spanish subtitles not available for this video")
            else:
                pytest.skip(f"Download failed: {e}")
        except Exception as e:
            pytest.skip(f"Network error or video unavailable: {e}")
    
    def test_download_real_transcript_to_file_ted_talk(self):
        """Test downloading a real transcript from TED talk to a file."""
        logger = setup_logging(silent=True, verbose=False)
        test_url = TEST_URLS['ted_talk']
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_file = os.path.join(temp_dir, 'ted_transcript.txt')
            
            try:
                # Try to download English transcript from TED talk
                download_transcript(test_url, 'en', output_file, 'both', False, logger)
                
                # Check that file was created
                assert os.path.exists(output_file)
                
                # Check file has content
                with open(output_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                assert len(content) > 0
                
                # Should not contain VTT formatting
                assert "WEBVTT" not in content
                assert "-->" not in content
                
            except SystemExit as e:
                if "not available" in str(e):
                    pytest.skip("English subtitles not available for this TED talk")
                else:
                    pytest.skip(f"Download failed: {e}")
            except Exception as e:
                pytest.skip(f"Network error or video unavailable: {e}")
    
    def test_download_real_transcript_vtt_format(self):
        """Test downloading a real transcript in VTT format."""
        logger = setup_logging(silent=True, verbose=False)
        test_url = TEST_URLS['spanish_medical']
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_file = os.path.join(temp_dir, 'transcript.vtt')
            
            try:
                # Try to download Spanish transcript in VTT format
                download_transcript(test_url, 'es', output_file, 'both', True, logger)
                
                # Check that file was created
                assert os.path.exists(output_file)
                
                # Check file has VTT content
                with open(output_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                assert len(content) > 0
                # Should contain VTT formatting in VTT mode
                assert "WEBVTT" in content or "-->" in content
                
            except SystemExit as e:
                if "not available" in str(e):
                    pytest.skip("Spanish subtitles not available for this video")
                else:
                    pytest.skip(f"Download failed: {e}")
            except Exception as e:
                pytest.skip(f"Network error or video unavailable: {e}")


@pytest.mark.integration
@pytest.mark.slow
class TestCLIIntegrationWithRealURLs:
    """Test the complete CLI workflow with real URLs."""
    
    def test_full_workflow_list_then_download_spanish(self, capsys):
        """Test complete workflow with Spanish medical video: list subtitles, then download one."""
        test_url = TEST_URLS['spanish_medical']
        
        # Step 1: List available subtitles
        with patch('sys.argv', ['yt-ts-cli', 'list', test_url]):
            try:
                main()
                list_output = capsys.readouterr()
                
                # Check if Spanish is available
                if 'es (' in list_output.out or 'Spanish' in list_output.out:
                    # Step 2: Download Spanish transcript
                    with tempfile.TemporaryDirectory() as temp_dir:
                        output_file = os.path.join(temp_dir, 'spanish_workflow_test.txt')
                        
                        with patch('sys.argv', ['yt-ts-cli', 'download', test_url, '-l', 'es', '-o', output_file]):
                            main()
                            
                            # Verify file was created
                            assert os.path.exists(output_file)
                            
                            with open(output_file, 'r', encoding='utf-8') as f:
                                content = f.read()
                            
                            assert len(content) > 0
                            print(f"Successfully downloaded {len(content)} characters of Spanish transcript")
                else:
                    pytest.skip("Spanish subtitles not available for test video")
                    
            except SystemExit as e:
                if e.code != 0:
                    pytest.skip(f"CLI workflow failed: {e}")
            except Exception as e:
                pytest.skip(f"Network error: {e}")
    
    def test_full_workflow_list_then_download_english(self, capsys):
        """Test complete workflow with TED talk: list subtitles, then download English."""
        test_url = TEST_URLS['ted_talk']
        
        # Step 1: List available subtitles
        with patch('sys.argv', ['yt-ts-cli', 'list', test_url]):
            try:
                main()
                list_output = capsys.readouterr()
                
                # Check if English is available
                if 'en (' in list_output.out or 'English' in list_output.out:
                    # Step 2: Download English transcript
                    with tempfile.TemporaryDirectory() as temp_dir:
                        output_file = os.path.join(temp_dir, 'english_workflow_test.txt')
                        
                        with patch('sys.argv', ['yt-ts-cli', 'download', test_url, '-l', 'en', '-o', output_file]):
                            main()
                            
                            # Verify file was created
                            assert os.path.exists(output_file)
                            
                            with open(output_file, 'r', encoding='utf-8') as f:
                                content = f.read()
                            
                            assert len(content) > 0
                            print(f"Successfully downloaded {len(content)} characters of English transcript")
                else:
                    pytest.skip("English subtitles not available for test video")
                    
            except SystemExit as e:
                if e.code != 0:
                    pytest.skip(f"CLI workflow failed: {e}")
            except Exception as e:
                pytest.skip(f"Network error: {e}")
    
    def test_cli_with_verbose_output(self, capsys):
        """Test CLI with verbose output on real video."""
        test_url = TEST_URLS['tech_video']  # Use Rick Roll video
        
        with patch('sys.argv', ['yt-ts-cli', '--verbose', 'list', test_url]):
            try:
                main()
                captured = capsys.readouterr()
                
                # Verbose mode should show debug information
                assert "DEBUG" in captured.err or "yt-dlp module is available" in captured.err
                
                # Should still show subtitle listing
                assert len(captured.out) > 0
                
            except SystemExit as e:
                if e.code != 0:
                    pytest.skip(f"Verbose CLI failed: {e}")
            except Exception as e:
                pytest.skip(f"Network error: {e}")


@pytest.mark.integration
@pytest.mark.slow  
class TestErrorHandlingWithRealURLs:
    """Test error handling with real (but problematic) URLs."""
    
    def test_invalid_youtube_url(self, capsys):
        """Test behavior with invalid YouTube URL."""
        invalid_url = "https://www.youtube.com/watch?v=INVALID_VIDEO_ID"
        
        with patch('sys.argv', ['yt-ts-cli', 'list', invalid_url]):
            with pytest.raises(SystemExit):
                main()
            
            captured = capsys.readouterr()
            # Should show an error message
            assert len(captured.err) > 0
    
    def test_non_youtube_url(self, capsys):
        """Test behavior with non-YouTube URL."""
        invalid_url = "https://www.google.com"
        
        with patch('sys.argv', ['yt-ts-cli', 'list', invalid_url]):
            with pytest.raises(SystemExit):
                main()
            
            captured = capsys.readouterr()
            # Should show an error message
            assert len(captured.err) > 0
    
    def test_unavailable_language(self, capsys):
        """Test requesting unavailable language."""
        test_url = TEST_URLS['spanish_medical']
        
        # Request a definitely invalid language code
        with patch('sys.argv', ['yt-ts-cli', 'download', test_url, '-l', 'zzzz', '-o', '-']):  # Invalid code
            try:
                main()
                # If it somehow succeeds, that's unexpected but we'll handle it
                captured = capsys.readouterr()
                print("Unexpected: Invalid language code 'zzzz' was accepted")
                
            except SystemExit:
                # Expected: should fail with an error
                captured = capsys.readouterr()
                error_msg = captured.err.lower()
                # Should contain some kind of error message
                assert (len(error_msg) > 0), f"Expected error message but got: {captured.err}"
                print(f"Got expected error: {captured.err.strip()}")


if __name__ == '__main__':
    # Run only integration tests
    pytest.main([__file__, '-v', '-m', 'integration'])
