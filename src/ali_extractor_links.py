import asyncio
import aiohttp
from bs4 import BeautifulSoup
import ssl
import re
import os
from dotenv import load_dotenv
import time


load_dotenv()


class LinkExtractor:
    """
    The LinkExtractor class extracts links from a given URL and saves them to a CSV file.
     It uses asyncio and aiohttp to asynchronously retrieve the HTML content of
     the URLs and BeautifulSoup to parse the HTML and extract the product IDs.
     It then constructs the product links and writes them, along with
     the provided categories, to a CSV file.
    """
    def __init__(self, url, cat1, cat2, cat3, n_pages) -> None:
        self.urls = []
        self.cat1 = cat1
        self.cat2 = cat2
        self.cat3 = cat3
        for i in range(1,n_pages+1):
            self.urls.append(url % str(i))

    async def get_links(self,session,url):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        async with session.get(url, ssl=ssl_context) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            html_doc = soup.prettify()  # non-rendered html

            ids = re.findall(r'"productId"\:"(\d+)', html_doc)
            products_id = [i for i in ids]
            return products_id

    async def extract_links(self):
        link = []
        cat1 = []
        cat2 = []
        cat3 = []

        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in self.urls:
                task = asyncio.ensure_future(self.get_links(session, url))
                tasks.append(task)

            # Gather all the tasks and wait for them to complete
            results = await asyncio.gather(*tasks)

            with open("data_extracted/" + os.getenv("NAME_LINKS_FILE"), "w") as file:
                # Iterate over the links and write them to the file
                for ids in results:
                    for id in ids:
                        product_link = 'https://es.aliexpress.com/item/' + id + '.html'
                        # Write the link, cat1, cat2, cat3 to the file
                        file.write(product_link + "," + self.cat1 + "," + self.cat2 + "," + self.cat3 + "\n")
                        link.append(product_link)
                        cat1.append(self.cat1)
                        cat2.append(self.cat2)
                        cat3.append(self.cat3)
        return link, cat1, cat2, cat3

    async def run(self):
        """
        This method runs the async function extract_links
        :return:
        """
        return await self.extract_links()






