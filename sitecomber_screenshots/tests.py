import logging
import environ
import json

from selenium import webdriver

from django.core.files.storage import get_storage_class

from sitecomber.apps.shared.interfaces import BaseSiteTest

from .utils.screenshots import generateLatestScreenshot, generateHistoricalScreenshots

logger = logging.getLogger('django')


root = environ.Path(__file__) - 2
env = environ.Env()
environ.Env.read_env(env_file=root('.env'))
SITECOMBER_SCREENSHOTS_DRIVER_CLASS = env('SITECOMBER_SCREENSHOTS_DRIVER_CLASS')
SITECOMBER_SCREENSHOTS_DRIVER_PATH = env('SITECOMBER_SCREENSHOTS_DRIVER_PATH')
SITECOMBER_SCREENSHOTS_STORAGE_BACKEND = env('SITECOMBER_SCREENSHOTS_STORAGE_BACKEND')

def should_test_page(page):
    if not page.last_status_code:
        return False
    if not page.is_internal:
        return False
    if page.last_content_type and 'text/html' not in page.last_content_type.lower():
        return False
    return True


class BaseScreenshotTest(BaseSiteTest):
    driver = None
    storage = None

    def setUp(self):
        driverClass = getattr(webdriver, SITECOMBER_SCREENSHOTS_DRIVER_CLASS)
        self.driver = driverClass(executable_path = SITECOMBER_SCREENSHOTS_DRIVER_PATH)
        self.storage = get_storage_class(SITECOMBER_SCREENSHOTS_STORAGE_BACKEND)

    def tearDown(self):
        self.driver.close()



class LatestScreenshotTest(BaseScreenshotTest):
    """
    Generates latest screenshots of each url
    """
    driver = None

    def get_description_html(self):

        return """<p>Generates latest screenshots of each url.</p>
        """

    def setUp(self):
        driverClass = getattr(webdriver, SITECOMBER_SCREENSHOTS_DRIVER_CLASS)
        self.driver = driverClass(executable_path = SITECOMBER_SCREENSHOTS_DRIVER_PATH)
        self.storage = get_storage_class(SITECOMBER_SCREENSHOTS_STORAGE_BACKEND)

    def tearDown(self):
        self.driver.close()

    def on_page_parsed(self, page):
        from sitecomber.apps.results.models import PageTestResult

        if should_test_page(page):

            try:
                status, message, data = generateLatestScreenshot(self.driver, self.storage, page, self.settings)
            except Exception as e:
                status = "error"
                message = u"Error generating screenshots for page: %s"%(e)
                data = {}
                logger.error(u)

            r, created = PageTestResult.objects.get_or_create(
                page=page,
                test=self.class_path
            )
            r.message = message
            r.status = status
            try:
                r.data = json.dumps(data, sort_keys=True, indent=2)
            except Exception as e:
                logger.error(u"Error dumping JSON data: %s: %s" % (data, e))
            r.save()


class HistoricalScreenshotTest(BaseScreenshotTest):
    """
    Generates historical screenshots of each url
    """
    driver = None

    def get_description_html(self):

        return """<p>Generates historical screenshots of each url.</p>
        """

    def on_page_parsed(self, page):
        from sitecomber.apps.results.models import PageTestResult

        if should_test_page(page):

            try:
                status, message, data = generateHistoricalScreenshots(self.driver, self.storage, page, self.settings)
            except Exception as e:
                status = "error"
                message = u"Error generating screenshots for page: %s"%(e)
                data = {}
                logger.error(u)

            r, created = PageTestResult.objects.get_or_create(
                page=page,
                test=self.class_path
            )
            r.message = message
            r.status = status
            try:
                r.data = json.dumps(data, sort_keys=True, indent=2)
            except Exception as e:
                logger.error(u"Error dumping JSON data: %s: %s" % (data, e))
            r.save()
