"""
Pytest configuration and fixtures for yt-ts-cli tests.
"""

import pytest
import tempfile
import os
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def sample_vtt_content():
    """Sample VTT content for testing."""
    return """WEBVTT

NOTE
This is a test subtitle file

00:00:01.000 --> 00:00:03.000
Hello world

00:00:04.000 --> 00:00:06.000
This is a test subtitle

STYLE
::cue {
  color: white;
}

00:00:07.000 --> 00:00:09.000
<c.yellow>Colored text</c.yellow>

00:00:10.000 --> 00:00:12.000
Text with <00:00:11.500>timestamp tags

00:00:13.000 --> 00:00:15.000
Multiple
lines
of text
"""


@pytest.fixture
def sample_vtt_file(temp_dir, sample_vtt_content):
    """Create a sample VTT file for testing."""
    vtt_path = os.path.join(temp_dir, 'test_subtitle.vtt')
    with open(vtt_path, 'w', encoding='utf-8') as f:
        f.write(sample_vtt_content)
    return vtt_path


@pytest.fixture
def mock_ytdl_info():
    """Mock yt-dlp info response."""
    return {
        'title': 'Test Video Title',
        'id': 'test123',
        'subtitles': {
            'en': [
                {
                    'url': 'http://example.com/en.vtt',
                    'ext': 'vtt',
                    'name': 'English'
                }
            ],
            'es': [
                {
                    'url': 'http://example.com/es.vtt', 
                    'ext': 'vtt',
                    'name': 'Spanish'
                }
            ],
            'fr': [
                {
                    'url': 'http://example.com/fr.vtt',
                    'ext': 'vtt', 
                    'name': 'French'
                }
            ]
        },
        'automatic_captions': {
            'en': [
                {
                    'url': 'http://example.com/en_auto.vtt',
                    'ext': 'vtt',
                    'name': 'English (auto-generated)'
                }
            ]
        }
    }
