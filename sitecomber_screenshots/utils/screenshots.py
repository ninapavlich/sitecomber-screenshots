import os
import time
import tempfile


def getSizes(settings):
    if "sizes" in settings:
        if isinstance(settings["sizes"], list) and all(isinstance(x, list) for x in settings["sizes"]):
            return settings["sizes"]
    return [[1600, 900]]


def generateLatestScreenshot(browser, storage, page, settings):
    messages = []
    data = {}
    status = "success" # or warning or error

    data["screenshots"] = generateScreenshot(browser, storage, page.url, settings, "latest", "sitecomber-screenshots/%s/%s/"%(page.site_domain.id, page.id))

    return status, messages, data

def generateHistoricalScreenshots(browser, storage, page, settings):
    messages = []
    data = {}
    status = "success" # or warning or error

    data["screenshots_daily"] = generateScreenshot(browser, storage, page.url, settings, "daily", "sitecomber-screenshots/%s/%s/"%(page.site_domain.id, page.id))
    data["screenshots_weekly"] = generateScreenshot(browser, storage, page.url, settings, "weekly", "sitecomber-screenshots/%s/%s/"%(page.site_domain.id, page.id))
    data["screenshots_monthly"] = generateScreenshot(browser, storage, page.url, settings, "monthly", "sitecomber-screenshots/%s/%s/"%(page.site_domain.id, page.id))
    data["screenshots_yearly"] = generateScreenshot(browser, storage, page.url, settings, "yearly", "sitecomber-screenshots/%s/%s/"%(page.site_domain.id, page.id))

    return status, messages, data


def generateScreenshot(browser, storage, url, settings, filePrefix, folder):
    browser.get(url)

    output = []
    sizes = getSizes(settings)
    for size in sizes:

        # Resize browser
        width = size[0]
        height = size[1]
        browser.set_window_size(width, height)
        time.sleep(1)

        # Create temporary file and determine file names
        fileType = ".png"
        tempFilePrefix = "%s-%sx%s" % (filePrefix, width, height)
        tempFile = tempfile.NamedTemporaryFile(delete=False, suffix=fileType, prefix=tempFilePrefix)
        tempFilename = tempFile.name
        filename = "%s%s" % (tempFilePrefix, fileType)
        savePath = os.path.join(folder, filename)


        # Save the screenshot into the temporary file
        browser.save_screenshot(tempFilename)

        # Make sure to get rid of existing file so we can override it
        if storage.exists(savePath):
            storage.delete(savePath)

        # tempFile.seek(0) -- TBD, not sure if we"ll need this yet
        savedFile = storage.save(savePath, ContentFile(tempFile.read()))

        #TEMP
        # tempFile.seek(0)
        # from pathlib import Path
        # localOutputDir = os.path.abspath(os.path.join(str(Path.home()), savePath))
        # if not os.path.exists(os.path.dirname(localOutputDir)):
        #     os.makedirs(os.path.dirname(localOutputDir))
        # if os.path.exists(localOutputDir):
        #     os.remove(localOutputDir)
        # myFile = open(localOutputDir, "wb")
        # myFile.write(tempFile.read())
        # tempFile.close()
        # savedFile = os.path.abspath(localOutputDir)

        output.append(savedFile)

        # Close and clean up temporary file
        tempFile.close()
        os.unlink(tempFilename)

    return output
