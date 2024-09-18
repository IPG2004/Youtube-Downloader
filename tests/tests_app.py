import unittest
import os
import sys
from unittest.mock import patch, MagicMock
import customtkinter as ctk
import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app import App

class TestYouTubeDownloaderApp(unittest.TestCase):

    def setUp(self):
        self.app = App()

    def tearDown(self):
        self.app.destroy()

    def test_ui_scaling(self):
        self.app.change_scaling("1080p")
        self.assertEqual(self.app.scaling, 1)
        self.app.change_scaling("1440p")
        self.assertEqual(self.app.scaling, 1.5)
        self.app.change_scaling("4k")
        self.assertEqual(self.app.scaling, 2)

    def test_ui_manual_scaling(self):
        self.app.change_scaling("1080p")
        self.app.modify_scaling(1)
        self.assertGreater(self.app.scaling, 1)
        self.app.modify_scaling(-1)
        self.assertLess(self.app.scaling, 1.1)

    def test_change_appearance_mode(self):
        self.app.change_appearance_mode("Light")
        self.assertEqual(ctk.get_appearance_mode(), "Light")
        self.app.change_appearance_mode("Dark")
        self.assertEqual(ctk.get_appearance_mode(), "Dark")

    def test_clear_search_field(self):
        self.app.url_entry.insert(0, "test url")
        self.app.clear_scfr()
        self.assertEqual(self.app.url_entry.get(), "")

    @patch('pytubefix.YouTube')
    def test_search_video_success(self, mock_youtube):
        mock_video = MagicMock()
        mock_video.title = "Test Title"
        mock_video.author = "Test Author"
        mock_video.length = 3600
        mock_video.views = 1000
        mock_video.publish_date = datetime.datetime(2021, 1, 1)
        mock_video.streams.filter.return_value = [MagicMock(resolution="720p")]
        mock_youtube.return_value = mock_video
        
        self.app.url_entry.insert(0, "https://www.youtube.com/watch?v=jNQXAC9IVRw")
        self.app.search_video()

        self.assertEqual(self.app.content[0], "Me at the zoo")
        self.assertEqual(self.app.content[1], "jawed")

    def test_select_destination_folder(self):
        with patch('tkinter.filedialog.askdirectory', return_value="/test/folder"):
            self.app.select_destination_folder()
            self.assertEqual(self.app.footer_destination.cget("text"), "/test/folder")

    def test_download_no_url(self):
        with patch.object(self.app, 'search_video', wraps=self.app.search_video) as mock_search_video:
            self.app.url_entry.delete(0, "end")
            self.app.search_video()
            self.assertEqual(self.app.url_entry.cget("fg_color"), "red")
            mock_search_video.assert_called_once()

if __name__ == "__main__":
    unittest.main()
