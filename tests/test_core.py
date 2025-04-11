import pytest
import asyncio
import os
from unittest.mock import patch, MagicMock
from autoupdate_languages.core import AutoUpdateLanguages
from pathlib import Path

@pytest.mark.asyncio
async def test_check_for_output_dir(tmp_path):
    updater = AutoUpdateLanguages()
    # Patch project root dir to temp
    with patch("autoupdate_languages.core.os.path.abspath", return_value=str(tmp_path)):
        output_dir = await updater.check_for_output_dir()
        assert os.path.isdir(output_dir)
        assert output_dir.endswith("project_output")

@pytest.mark.asyncio
async def test_generate_file(tmp_path):
    updater = AutoUpdateLanguages()
    mock_ul = [[MagicMock(string='Python\n'), MagicMock(string='JavaScript\n')]]

    with patch.object(updater, 'get_lang_list', return_value=mock_ul):
        await updater.generate_file(str(tmp_path))  # pass str to match function signature

        output_file = tmp_path / "lang_list.txt"  # use Path object for test
        assert output_file.exists()
        content = output_file.read_text()
        assert "Python" in content
        assert "JavaScript" in content

@pytest.mark.asyncio
async def test_get_dates():
    updater = AutoUpdateLanguages()
    today, next_month = await updater.get_dates()
    assert today.month in range(1, 13)
    assert next_month.month == (today.month % 12) + 1 or next_month.month == 1

@pytest.mark.asyncio
async def test_get_lang_list():
    updater = AutoUpdateLanguages()

    fake_html = '''
    <html>
      <body>
        <ul class="column-list">
          <li>Python</li>
          <li>JavaScript</li>
        </ul>
      </body>
    </html>
    '''
    mock_response = MagicMock()
    mock_response.content = fake_html

    with patch("autoupdate_languages.core.requests.get", return_value=mock_response):
        ul_elements = await updater.get_lang_list()
        assert len(ul_elements) == 1
        assert ul_elements[0].find_all("li")[0].text == "Python"

@pytest.mark.asyncio
async def test_start_sequence(monkeypatch):
    updater = AutoUpdateLanguages()
    updater.exp_days = 3  # shorter for testing
    updater.delay = 0.01  # simulate a fast test

    # Mock get_dates and generate_file
