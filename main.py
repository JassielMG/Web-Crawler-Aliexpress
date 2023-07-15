from src.ali_extractor_links import LinkExtractor
import os
import time
import asyncio
from src import ali_crawler_runner
import humanize


async def run_extractor_links():
    """
    This function runs the link extractor and save the csv file with the links to crawl
    """
    url = os.getenv('URL_BY_CATEGORY')
    cat1 = os.getenv('CATEGORY_LEVEL1')
    cat2 = os.getenv('CATEGORY_LEVEL2')
    cat3 = os.getenv('CATEGORY_LEVEL3')
    n_pages = int(os.getenv('N_PAGES'))
    try:
        link_extractor = LinkExtractor(url, cat1, cat2, cat3, n_pages)
        start_time = time.time()
        link, c1, c2, c3 = await link_extractor.run()
        end_time = time.time()
        print(f"Time elapsed during extraction links: {end_time - start_time} seconds")
        return link, c1, c2, c3
    except Exception as e:
        print(f"An error has occurred while extracting links: {str(e)}")


async def main():
    loop = True

    while loop:
        # Run the link extraction task concurrently
        task1 = asyncio.create_task(run_extractor_links())

        while not task1.done():
            print("Waiting for the link extraction task to complete...")
            await asyncio.sleep(1)

        url, cat1, cat2, cat3 = task1.result()
        if len(url) > 0:
            loop = False
        print(url)

    start = time.time()
    data = []
    c1 = 0
    c2 = 0
    # Run the tasks concurrently using an Executor
    loop = asyncio.get_event_loop()  # Get the event loop
    rows = zip(url, cat1, cat2, cat3)  # Zip the rows
    tasks = [loop.create_task(ali_crawler_runner.process_row(row)) for row in rows]  # Create a task for each row
    results = await asyncio.gather(*tasks)  # Gather the results of the tasks as they complete
    for result in results:  # Iterate over the results
        c1 += 1
        if result is not None:
            data.append(result)  # Append the result to our data list
            c2 += 1

    # Saving the data to a CSV file
    print(ali_crawler_runner.save_data_to_csv(data))
    end = time.time()

    print("\n ------------------- Extraction Summary ------------------- \n")
    print(f".-Total links extracted to scrape: {c1}")
    print(f".-Category 1: {os.getenv('CATEGORY_LEVEL1')}")
    print(f".-Category 2: {os.getenv('CATEGORY_LEVEL2')}")
    print(f".-Category 3: {os.getenv('CATEGORY_LEVEL3')}")
    print(f".-Number of pages: {os.getenv('N_PAGES')}")
    print(f".-Total products extracted: {c2}")
    print(f".-Total failed products extracted : {c1 - c2}")
    print(f".-Time spent during crawling: {time.strftime('%H:%M:%S', time.gmtime(end - start))}")
    print(".-Saved file name: " + os.getenv("NAME_DATA_EXTRACTED_FILE"))
    print(".-Size file: " + humanize.naturalsize(os.path.getsize("data_extracted/" + os.getenv("NAME_DATA_EXTRACTED_FILE"))))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()