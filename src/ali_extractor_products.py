from bs4 import BeautifulSoup
import re
import json
import pandas as pd


class AliexpressCrawler:
    data = []

    def __init__(self, url, html_doc, cat1, cat2, cat3) -> None:
        self.url = url
        self.html_doc = html_doc
        self.cat1 = cat1
        self.cat2 = cat2
        self.cat3 = cat3

    def get_product_info(self):
        self.soup = BeautifulSoup(self.html_doc, 'html.parser')
        self.id_product = re.findall(r'"idStr":"(\d+)', self.html_doc)[0]
        self.title_product = re.findall(r'"subject":"([^"]*)"', self.html_doc)[0]
        self.image_url = self.soup.find("div", class_="image-view-magnifier-wrap").find("img")["src"]
        self.pieces = re.findall(r'"numberPerLot":(\d+)', self.html_doc)[0]
        self.solds = re.findall(r'"formatTradeCount":"(\d+)', self.html_doc)[0]
        self.starts = re.findall(r'"evarageStar":"([^"]*)"', self.html_doc)[0]
        self.reviwes = re.findall(r'"totalValidNum":(\d+)', self.html_doc)[0]
        self.wishedcount = re.findall(r'"itemWishedCount":(\d+)', self.html_doc)[0]
        stock = self.soup.find("div", class_="quantity--info--Lv_Aw6e").find("div").find("span")
        if stock is None:
            stock = self.soup.select_one("div.quantity--info--Lv_Aw6e > div:nth-of-type(2) > span")
            if stock is not None:
                self.stock = re.search(r'(\d+)', stock.text.strip("\n ")).group()
            else:
                stock = self.soup.find("div", class_="quantity--info--Lv_Aw6e").find("div")
                self.stock = re.search(r'(\d+)', stock.text.strip("\n ")).group()
        else:
            self.stock = re.search(r'(\d+)', stock.text.strip("\n ")).group()

        print(self.id_product, self.title_product,self.image_url, self.pieces, self.solds, self.starts, self.reviwes, self.stock,
              self.wishedcount)

    def get_product_price(self):
        self.soup = BeautifulSoup(self.html_doc, 'html.parser')
        # extracting the product price with selectors from the rendered html document
        self.currency = "MXN$"

        price = self.soup.find('div', attrs={'class': 'es--wrap--erdmPRe notranslate'})
        if price is None:
            print("*************** This product has no price *************** ",self.id_product )
            price = self.soup.find('span', attrs={'class': 'price--currentPriceText--mLOiFD4 pdp-comp-price-current'})
            self.price = price.get_text().strip("\n ")
            self.price = self.price.strip("MXN").replace("$", "")
        else:
            price = price.find_all('span')
            self.price = "".join([i.get_text().strip("\n ") for i in price]).strip(self.currency)

        discount = self.soup.find("span", class_="price--discount--xET8qnP")
        self.discount = re.findall(r'(\d+)', discount.get_text())[0] if discount is not None else 0
        self.old_price = self.soup.find("span", class_="price--originalText--Zsc6sMv")
        self.old_price = 0 if self.old_price is None else self.old_price.text.strip("\n ").strip(self.currency).replace("$", "")
        print(self.price, self.old_price, self.discount, self.currency)

    def get_product_rating(self):
        feedback_component = re.findall(r'"feedbackComponent":\{(.+?)\}', self.html_doc)
        self.feedback_component = json.loads("{" + feedback_component[0] + "}")
        print(self.feedback_component)

    def get_product_details(self):
        jsonDetails = re.findall(r'"props":\[(.*?)\]\},"skuComponent"', self.html_doc)
        jsonDetails = json.loads("[" + jsonDetails[0] + "]")

        details = dict()

        for detail in jsonDetails:
            if len(detail) == 2:
                details[detail["attrName"]] = detail["attrValue"]

        self.details = details

        print(self.details)

    def get_seller_info(self):
        self.storeName = re.findall(r'"storeName":"([^"]*)"', self.html_doc)[0]
        self.dateOpened = re.findall(r'"formatOpenTime":"([^"]*)"', self.html_doc)[0]
        self.yearsActive = re.findall(r'"openedYear":(\d+)', self.html_doc)[0]
        self.country = re.findall(r'"countryCompleteName":"([^"]*)"', self.html_doc)[0]
        self.company_id = re.findall(r'"companyId":(\d+)', self.html_doc)[0]
        self.storeWishedCount = re.findall(r'"storeWishedCount":(\d+)', self.html_doc)[0]
        self.sellerTotalNum = re.findall(r'"sellerTotalNum":(\d+)', self.html_doc)[0]
        self.sellerPositiveRate = re.findall(r'"sellerPositiveRate":"([^"]*)"', self.html_doc)[0]
        print(self.storeName, self.dateOpened, self.yearsActive, self.country, self.company_id, self.storeWishedCount,
              self.sellerTotalNum, self.sellerPositiveRate)

    def get_shipping_info(self):
        # shipping options
        self.delivery_provider_name = re.findall(r'"deliveryProviderName":"([^"]*)"', self.html_doc)
        # costs of shipping options
        self.displayAmount = re.findall(r'"displayAmount":(\d+\.?\d*)', self.html_doc)
        # delivery date
        self.deliveryDate = re.findall(r'"deliveryDate":"([^"]*)"', self.html_doc)
        # delivery days max
        self.deliveryDayMax = re.findall(r'"deliveryDayMax":(\d+)', self.html_doc)
        # delivery days min
        self.deliveryDayMin = re.findall(r'"deliveryDayMin":(\d+)', self.html_doc)
        # shipTo
        self.shipTo = re.findall(r'"shipTo":"([^"]*)"', self.html_doc)[0]

        print(self.delivery_provider_name, self.displayAmount, self.deliveryDate, self.deliveryDayMax,
              self.deliveryDayMin, self.shipTo)

    def save_data_to_csv(self):
        # save the data to a csv file with headers and the data in a row separated by commas
        name_columns = ["id_product", "title_product", "pieces", "solds", "starts", "reviwes", "stock", "wishedCount",
                        "price", "old_price", "discount", "url", "image_url", "currency", "feedbackComponent", "details",
                        "storeName", "dateOpened", "yearsActive", "storeWishedCount", "sellerTotalNum",
                        "sellerPositiveRate", "country", "company_id", "delivery_provider_name", "displayAmount",
                        "deliveryDate", "deliveryDayMax", "deliveryDayMin", "shipTo", "category1", "category2",
                        "category3"]
        file_path = "data.csv"
        df = pd.DataFrame(self.data, columns=name_columns)

        df.to_csv(file_path, index=False)

    def get_data(self):
        return [self.id_product, self.title_product, self.pieces, self.solds, self.starts, self.reviwes, self.stock,
             self.wishedcount, self.price, self.old_price, self.discount, self.url, self.image_url, self.currency,
             self.feedback_component, self.details, self.storeName, self.dateOpened, self.yearsActive,
             self.storeWishedCount, self.sellerTotalNum, self.sellerPositiveRate, self.country, self.company_id,
             self.delivery_provider_name, self.displayAmount, self.deliveryDate, self.deliveryDayMax,
             self.deliveryDayMin, self.shipTo, self.cat1, self.cat2, self.cat3]

    def run_crawler(self):
        try:
            self.get_product_info()
            self.get_product_price()
            self.get_product_rating()
            self.get_product_details()
            self.get_seller_info()
            self.get_shipping_info()
        except Exception as e:
            print(f"** Error:{e} *** \n There is an error with the product {self.url}")

        return self.get_data()

