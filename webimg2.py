import csv
from io import BytesIO
from PIL import Image
from selenium import webdriver

# Set up Selenium webdriver
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(options=options)

# Set page load timeout to 60 seconds
driver.set_page_load_timeout(60)

# Open CSV file and read URLs
with open('csv/webimg2.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row

    for i, row in enumerate(reader):
        url = row[0]

        try:
            # Load webpage and take screenshot
            driver.get(url)
            screenshot = driver.get_screenshot_as_png()

        except Exception as e:
            # Handle errors
            error = str(e)

            if 'timeout' in error:
                # Page load timed out
                print(f'Error for URL {i+1}: {url} - Page load timed out')
                error_msg = 'Page load timed out'

            elif '404' in error:
                # URL returns 404 error
                print(f'Error for URL {i+1}: {url} - 404 error')
                error_msg = '404 error'

            else:
                # URL has other error
                print(f'Error for URL {i+1}: {url} - {error}')
                error_msg = error

            # Write error to errchk.csv file
            with open('csv/errchk.csv', 'a', newline='') as errfile:
                if 'Error' not in row:
                    row.append(error_msg)
                    writer = csv.writer(errfile)
                    writer.writerow(row)

            continue  # Skip to next URL

        # Open screenshot as image and save to file
        img = Image.open(BytesIO(screenshot))
        img.save(f'img/screenshot_{i+1}.png')

        # Write 'Screenshot saved' to errchk.csv file
        with open('csv/errchk.csv', 'a', newline='') as errfile:
            if 'Screenshot saved' not in row:
                row.append('Screenshot saved')
                writer = csv.writer(errfile)
                writer.writerow(row)

        # Print progress
        print(f'Saved screenshot for URL {i+1}: {url}')

# Close Selenium webdriver
driver.quit()
