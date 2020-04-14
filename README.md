# sitecomber-screenshots

Article content tests for [Sitecomber platform](https://github.com/ninapavlich/sitecomber)

## Installation Instructions

Selenium Set Up:

This set of tests requires a Selenium server running in the background.

You can install selenium locally for testing like so:

```
> brew install geckodriver
> which geckodriver
/usr/local/bin/geckodriver # <-- Copy this path
```

For use with Heroku, you will need to deploy with a custom buildpack, and specify the webdriver

```
heroku buildpacks:add --index 1 https://github.com/heroku-buildpack-chromedriver
heroku config:set GOOGLE_CHROME_BIN=/app/.apt/usr/bin/google_chrome
```

Library Set Up:

1. pip install sitecomber-screenshots
2. Add 'sitecomber_screenshots.tests' to your INSTALLED_APPS list in your project's settings.py
3. Add the following values to your Sitecomber .env file.

```
SITECOMBER_SCREENSHOTS_DRIVER_CLASS=Firefox
SITECOMBER_SCREENSHOTS_DRIVER_PATH=/usr/local/bin/geckodriver
```

4. Restart server to see new tests available in site settings

## Supported Tests:

### LatestScreenshotTest

Gets the latest screenshot for each successful page result.

You can specify the image storage location and screenshot sizes in the Site's test settings JSON.

screenshot sizes should be defined as an array of integers, representing the window width of the window taking the screenshot. The default screenshot is 1600px wide by 900px tall.

```json
{
  "storage": "default",
  "sizes": [[1600, 900], [800, 400]]
}
```

Screenshots will be saved in the following storage directory: `sitecomber-screenshots/<site-id>/<result-url-id>/latest-<width>x<height>.png`

### HistoricalScreenshotTest

Gets historical screenshots for each successful page result.

You can specify the image storage location and screenshot sizes in the Site's test settings JSON.

screenshot sizes should be defined as an array of integers, representing the window width of the window taking the screenshot. The default screenshot is 1600px wide by 900px tall.

```json
{
  "storage": "default",
  "sizes": [[1600, 900], [800, 400]]
}
```

Screenshots will be saved in the following storage directory:

```
sitecomber-screenshots/<site-id>/<result-url-id>/daily-<width>x<height>.png
sitecomber-screenshots/<site-id>/<result-url-id>/weekly-<width>x<height>.png
sitecomber-screenshots/<site-id>/<result-url-id>/monthly-<width>x<height>.png
sitecomber-screenshots/<site-id>/<result-url-id>/yearly-<width>x<height>.png
```

## Testing Instructions

To use test functions, run the following:

```bash
    virtualenv venv -p python3
    source venv/bin/activate
    pip install -r requirements.txt

    # This will run a general unit test:
    python unit_tests.py

```
