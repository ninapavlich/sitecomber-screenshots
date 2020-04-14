import os
import sys
import traceback
from pathlib import Path
from unittest.mock import Mock

# TODO -- I wonder if there is a way to make the path below more dynamic and flexible for other python versions?
SITECOMBER_VENV_PACKAGES_DIR = os.path.abspath(os.path.join('..', os.path.dirname(__file__), 'sitecomber', 'venv', 'lib', 'python3.7', 'site-packages'))
SITECOMBER_DIR = os.path.abspath(os.path.join('..', os.path.dirname(__file__), 'sitecomber'))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'sitecomber_screenshots'))


sys.path.append(SITECOMBER_VENV_PACKAGES_DIR)
sys.path.append(SITECOMBER_DIR)
sys.path.append(BASE_DIR)

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sitecomber.settings')
#
# import django
# django.setup()

# from sitecomber.apps.results.models import PageTestResult


from sitecomber_screenshots.tests import LatestScreenshotTest
from sitecomber_screenshots.utils.screenshots import generateLatestScreenshot

from django.core.files.storage import FileSystemStorage

localOutputDir = os.path.join(str(Path.home()), 'sitecomber-screenshots')
if not os.path.exists(localOutputDir):
    os.makedirs(localOutputDir)
localTestStorage = FileSystemStorage(location=localOutputDir)

mockSite = {}
mockPage = Mock(spec=['url', 'site_domain', 'id'], url='https://www.nytimes.com/', id='101', site_domain=Mock(spec=['id'], id='1'))
mockSettings = {
  "storage": "default",
  "sizes": [[1600, 900], [900, 1600], [400, 800]]
}
testInstance = LatestScreenshotTest(mockSite, mockSettings)
testInstance.setUp()

try:
  status, message, data = generateLatestScreenshot(testInstance.driver, localTestStorage, mockPage, testInstance.settings)
  print(status)
  print(message)
  print(data)
except Exception as e:
  print(e)
  traceback.print_exc(file=sys.stdout)

testInstance.tearDown()
