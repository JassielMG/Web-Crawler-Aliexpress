import os
import pandas as pd
from src import ali_extractor_products
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import ChromiumOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

load_dotenv()


async def get_rendered_html(url, max_retries=int(os.getenv('MAX_RETRIES'))):
    """
    This function uses Selenium to render the HTML of the given URL and returns it,
    with support for multiple retries in case of errors.
    :param url: URL to render
    :param max_retries: maximum number of retries
    :return: rendered HTML or None if all retries fail
    """
    for retry in range(1, max_retries + 1):
        try:
            options = ChromiumOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-setuid-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')

            driver_path = "/usr/bin/chromedriver"
            service = Service(driver_path)

            # Create a new instance of the Chrome driver with the chromedriver path
            driver = webdriver.Chrome(service=service, options=options)

            driver.set_page_load_timeout(20)

            # Navigate to the URL
            driver.get(url)

            # Get the rendered HTML
            rendered_html = driver.page_source

            # Close the browser
            driver.quit()

            # Parse the HTML using BeautifulSoup
            soup = BeautifulSoup(rendered_html, 'html.parser')
            rendered_html = soup.prettify()

            return rendered_html

        except Exception as e:
            # Handle other exceptions
            print(f"An error ocurred while rendering the HTML of {url}: {str(e)}")

        if retry < max_retries:
            print(f"Retry attempt {retry} of {max_retries} to render {url}")
        else:
            print(f"Max retries reached to render {url}. Skipping...")
    return None


def crawl_url(url, html, cat1, cat2, cat3):
    """
    This function crawls the given URL and returns the data extracted from it
    :param url:
    :param html:
    :param cat1:
    :param cat2:
    :param cat3:
    :return:
    """
    Ali = ali_extractor_products.AliexpressCrawler(url, html, cat1, cat2, cat3)
    return Ali.run_crawler()


async def process_row(row):
    """
    This function processes a row of the CSV file and returns the data extracted from it
    This function use the other function to render the HTML and crawl the URL
    :param row:
    :return:
    """
    url = row[0]
    cat1 = row[1]
    cat2 = row[2]
    cat3 = row[3]

    html = await get_rendered_html(url)
    try:
        result = crawl_url(url, html, cat1, cat2, cat3)
    except Exception as e:
        print(f"Error al procesar la URL {url}: {str(e)}")
        result = None

    return result


def save_data_to_csv(data):
    """
    This function saves the data to a CSV file
    :param data:
    :return:
    """
    name_columns = ["id_product", "title_product", "pieces", "solds", "starts", "reviwes", "stock", "wishedCount",
                    "price", "old_price", "discount", "url", "image_url", "currency", "feedbackComponent", "details",
                    "storeName", "dateOpened", "yearsActive", "storeWishedCount", "sellerTotalNum",
                    "sellerPositiveRate", "country", "company_id", "delivery_provider_name", "displayAmount",
                    "deliveryDate", "deliveryDayMax", "deliveryDayMin", "shipTo", "category1", "category2",
                    "category3"]
    try:
        df = pd.DataFrame(data, columns=name_columns)
        df.to_csv("data_extracted/" + os.getenv("NAME_DATA_EXTRACTED_FILE"), index=False)
        return "Data saved successfully"

    except Exception as e:
        return f"An error has occurred while saving the data to CSV: {str(e)}"




