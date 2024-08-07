from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

from python_crawler.models import BrowserType, Location


class Response:
    def __init__(self):
        self.status_code = 500
        self.headers = {}
        self.html = None
        self.error = None


class Request:
    def __init__(self, crawler, url):
        self.crawler = crawler
        self.url = url
        self.target_url = None
        self.status_code = None
        self.headers = {}

        self.__title = None
        self.__html = None

    @property
    def title(self):
        if not self.__title:
            self.__title = self.crawler.page.title()
        return self.__title

    @property
    def html(self):
        if not self.__html:
            self.__html = self.crawler.page.content()
        return self.__html

    def get(self):
        """
        Try statement using crawler to handle request and get response status_code, headers and html
            :return: Response
        """
        response = Response()

        try:
            self.crawler.new_page(self.url)

            r = self.crawler.request
            response.status_code = r.status_code
            response.headers = r.headers
            response.html = r.html
        except Exception as e:
            response.error = str(e)

        self.crawler.close()
        return response


class GoogleRequest(Request):
    def __init__(self, query, tld=Location.WORLDWIDE):
        self.domain = 'google%s' % tld.value

        super().__init__(
            crawler=Crawler(
                domain='.%s' % self.domain,
                browser_type=BrowserType.CHROMIUM
            ),
            url='https://%s/search?%s' % (
                self.domain,
                query.encoded_str
            )
        )


class BingRequest(Request):
    def __init__(self, query, tld=Location.WORLDWIDE):
        self.domain = 'bing%s' % tld.value

        super().__init__(
            crawler=Crawler(
                domain='.%s' % self.domain,
                browser_type=BrowserType.FIREFOX
            ),
            url='https://%s/search?%s' % (
                self.domain,
                query.encoded_str
            )
        )


class CrawlerRequest:
    def __init__(self, url):
        self.url = url
        self.target_url = None
        self.status_code = None
        self.headers = {}


class Crawler:
    def __init__(self, domain='.google.com', browser_type=BrowserType.CHROMIUM):
        self.domain = domain
        self.playwright = sync_playwright().start()

        if browser_type == BrowserType.FIREFOX:
            self.browser = self.playwright.firefox.launch(
                headless=True,
            )
        else:
            self.browser = self.playwright.chromium.launch(
                headless=True,
                args=['--single-process', '--no-zygote', '--no-sandbox']
            )

        self.context = self.browser.new_context()
        self.context.add_cookies([
            {
                'name': 'SOCS',
                'value': 'CAISHAgBEhJnd3NfMjAyMjA4MjktMF9SQzEaAmVuIAEaBgiB8U-YAg',
                'domain': self.domain,
                'path': '/'
            }
        ])

        self.page = None
        self.request = None

    def new_page(self, url):
        if self.page:
            self.page.close()

        self.request = Request(self, url)
        self.page = self.context.new_page()
        stealth_sync(self.page)
        self.page.on("response", self.__handle_request__)
        self.page.goto(self.request.url)

    def __handle_request__(self, response):
        if not self.request.target_url and response.status not in [302, 301]:
            self.request.target_url = response.url
            self.request.status_code = response.status
            self.request.headers = response.headers

    def close(self):
        self.browser.close()
        self.playwright.stop()
