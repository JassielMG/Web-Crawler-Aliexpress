## Web-Crawler-Aliexpress

 This is a web scraper or web crawler that extracts product information from the AliExpress page. Its goal is to extract information from most of the products in different categories of AliExpress. The scraper saves the extracted data to a CSV file in the "data_extracted" folder. It uses asynchronous requests and the following core libraries: asyncio, aiohttp, selenium, and BeautifulSoup.
 
## Installation

Clone the repo:
```bash
git clone https://github.com/JassielMg/Web-Crawler-Aliexpress.git
cd Web-Crawler-Aliexpress
```

## Usage

There is many way to run the project, you can run it in a virtual environment or in a docker container, the steps to run the project in each of these ways are described below:

### Runing the project in virtual environment:

1.- Create a virtual environment, activate it, and install the dependencies:
```bash
python -m venv venv
source venv/bin/activate (or venv\Scripts\activate.bat for Windows)
pip install -r requirements.txt
```

2.- Setting the environment variables creating a ".env" or If you are using an IDE like PyCharm, you can configure environment variables directly in the IDE's run configuration.
The variables you need to configure are as follows:

- `URL_BY_CATEGORY`: URL of the AliExpress category to scrape.
- `CATEGORY_LEVEL1`: Level 1 of the category.
- `CATEGORY_LEVEL2`: Level 2 of the category.
- `CATEGORY_LEVEL3`: Level 3 of the category.
- `N_PAGES`: Number of pages to consider for the category.
- `MAX_RETRIES`: Number of retries in case of connection failure.
- `NAME_LINKS_PATH`: Path and filename to store the extracted links.
- `NAME_SAVED_PATH`: Path and filename of the output file to save the extracted data.


#### If you want to save the data on aws s3 follow the next steps the other way skip this step if you prefer save the data in a local path:

a.- If you want to save the data in a S3 bucket on aws, you can configure the following environment variables:
- `SAVE_TO_S3`: True if you want to save the data in a S3 bucket, False otherwise.
- `AWS_ACCESS_KEY_ID`: Your AWS access key ID.
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key.
- `AWS_REGION`: Your AWS region.
- `AWS_BUCKET_NAME`: Your AWS bucket name.


b.- Or other option i recommend using the aws cli to interact with amazon services from your local environment, you can download it from the following link:
https://aws.amazon.com/es/cli/

You need to configure the aws credentials for use cli and interative with the services, you can do it with the following command:
```bash
aws configure
```
The credentials will be stored in a file in your home directory, under ~/.aws/credentials (Linux & Mac) or C:\Users\USERNAME\.aws\credentials (Windows).

once you have configured aws cli you can execute the program and indicate if you want to save your data in any bucket, the boto3 sdk will automatically take the keys configured in your aws cli. (**only if you work on your local machine**)


3.- Run the main file to start the web scraper:

```bash
python main.py
```
The web scraper will start extracting product information from AliExpress based on the settings provided. The results will be saved to the CSV file specified in NAME_SAVED_PATH

### Executing the project in a docker container:

1.- Build the docker image:
```bash
docker build -t ali-web-crawler .
```
2.- Verify that the image was created correctly:
```bash
docker images

REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ali-web-crawler     latest              0f2b2b2b2b2b        2 minutes ago       1.01GB
```
3.- Configure the docker-compose.yml file with the environment variables. An example configuration is shown below:
```yaml
version: '3'
services:
  celphones-container:
    image: ali-web-crawler
    volumes:
      - YOUR-PATH-TO-SAVE-DATA:/app/data_extracted:rw
    environment:
        - URL_BY_CATEGORY=https://es.aliexpress.com/category/204006047/cellphones.html?category_redirect=1&spm=a2g0o.productlist.103.9.7a771f04VEePhG&CatId=204006047&trafficChannel=main&isCategoryBrowse=true&g=y&page=%s
        - CATEGORY_LEVEL1=Celulares y telecomunicaciones
        - CATEGORY_LEVEL2=Marcas populares
        - CATEGORY_LEVEL3=Teléfonos móviles
        - N_PAGES=1
        - MAX_RETRIES=10
        - NAME_LINKS_FILE=links_celulares_populares.csv
        - NAME_DATA_EXTRACTED_FILE=celulares_populares.csv 
        - SAVE_TO_S3=False 
        - AWS_ACCESS_KEY_ID=
        - AWS_SECRET_ACCESS_KEY=
        - AWS_REGION=
        - AWS_BUCKET_NAME=

```
The environment variables are the same as in the previous section. The variables provided above is an example for the category "Celulares y telecomunicaciones -> Marcas populares -> Teléfonos móviles". Here we are indicate that the web scraper will extract the information of the first page of the category, and the output files will be saved in the folder "data_extracted" in the container but how we use volume to persist the data, the files extracted will be saved on the local path indicated. We can change the value of the environment variables to extract the information of more pages or change the category to scrape.

If you need to save the data in a S3 bucket on aws, you must set the variable SAVE_TO_S3 as True and configure the other variables related to aws credentials. The other way the data only will save in the local path indicated.

**Notes:**
* Make sure that the local path for saving the data exists before running the docker-compose up command.
* The image name must match the one you created in the previous step.
* You can create multiple containers with different configurations. In the example above, a container named "celphones-container" was created, but you can create additional containers with different configurations based on the category.
* A good practice is use secrets to store the credentials of aws, you can use docker secrets to do it, you can find more information in the following link: https://docs.docker.com/engine/swarm/secrets/

4.- Run the docker-compose file:
```bash 
docker-compose up
```
This will run all the containers configured in the docker-compose.yml file. Now, the web scraper will start extracting product information from AliExpress based on the provided settings. The results will be saved to the CSV file in the specified local path.

## Recomendations
If you want to have better control over the extraction processes or monitor the data being extracted, you can use Docker commands to manage the containers. Some useful commands include:
```bash
List all containers, including those that are not running:
docker ps -a 
```

```bash
View the logs of a specific container:
docker logs <container_name>
```

```bash
Access the shell of a running container to perform live debugging or execute commands:
docker exec -it <container_name> bash
```

```bash
start a container
docker start <container_name>
```
```bash
stop a container
docker stop <container_name>
```

## Contact
If you have any questions, suggestions, or feedback, please feel free to reach out to us.

Project Maintainer: Jassiel Montes \
GitHub: @JassielMg \
LinkedIn: https://www.linkedin.com/in/jassiel-montes/