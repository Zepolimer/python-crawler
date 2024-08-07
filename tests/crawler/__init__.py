import unittest
from unittest.mock import Mock, patch

from python_crawler.crawler import GoogleRequest, BingRequest


class CrawlerTestCase(unittest.TestCase):
    def test_google_request(self):
        class Query:
            def __init__(self, encoded_str):
                self.encoded_str = encoded_str


        mock_content = Mock()
        mock_content.return_value = '<html></html>'

        mock_page = Mock()
        mock_page.return_value = Mock(
            content=mock_content
        )

        mock_playwright = Mock()
        mock_playwright.start().chromium.launch().new_context().new_page = mock_page

        with patch(
            'python_crawler.crawler.sync_playwright',
            return_value=mock_playwright
        ):
            request = GoogleRequest(
                query=Query(encoded_str='q=google_test')
            )
            self.assertEqual(
                request.url,
                'https://google.com/search?q=google_test'
            )

            response = request.get()
            self.assertEqual(
                response.html,
                '<html></html>'
            )


    def test_bing_request(self):
        class Query:
            def __init__(self, encoded_str):
                self.encoded_str = encoded_str

        mock_content = Mock()
        mock_content.return_value = '<html></html>'

        mock_page = Mock()
        mock_page.return_value = Mock(
            content=mock_content
        )

        mock_playwright = Mock()
        mock_playwright.start().firefox.launch().new_context().new_page = mock_page

        with patch(
                'python_crawler.crawler.sync_playwright',
                return_value=mock_playwright
        ):
            request = BingRequest(
                query=Query(encoded_str='q=bing_test')
            )
            self.assertEqual(
                request.url,
                'https://bing.com/search?q=bing_test'
            )

            response = request.get()
            self.assertEqual(
                response.html,
                '<html></html>'
            )
