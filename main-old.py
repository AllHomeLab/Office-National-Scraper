import requests
from bs4 import BeautifulSoup
import pandas as pd
import http.client  # or http.client if you're on Python 3
import time

print("Starting")

http.client._MAXHEADERS = 1000


def get_product_urls():
    print("Running get_product_urls")
    # Base URL components
    base_url = "https://www.officenational.com.au/shop/en/onesolution/stationery"
    query_params = "?fromPage=catalogEntryList&beginIndex={}&pageSize=36&pageView=grid"

    # List to store product data
    products = []

    url = "https://www.officenational.com.au/shop/en/onesolution/stationery?fromPage=catalogEntryList&beginIndex=0&pageSize=36&pageView=grid"
    response = requests.get(
        url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}
    )
    soup = BeautifulSoup(response.text, "html.parser")
    total_pages = int(soup.find_all("a", class_="hoverover")[-1]["data-page-number"])
    total_products = int(total_pages) * 32
    print("Total Pages: " + str(total_pages))
    print("Total Products: " + str(total_products))

    # Pagination loop
    page = 1
    while page < total_pages:
        url = f"{base_url}{query_params.format((page-1)*32)}"
        response = requests.get(
            url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}
        )
        # print(response.status_code)
        # time.sleep(0.2)
        soup = BeautifulSoup(response.text, "html.parser")

        print(
            f"Scraping page {page} / {total_pages} ({round(((page)/total_pages)*100,0)}%) Status Code: {response.status_code}"
        )

        # Find all product containers
        product_containers = soup.find_all("div", class_="product_info")

        # Break if no products are found (end of pagination)
        if not product_containers:
            print("No more products found.")
            break

        # Extract details for each product
        for container in product_containers:

            # Find URL
            try:
                url = container.find("a")["href"]
            except AttributeError:
                print("Error!")
                url = None

            products.append({"URL": url})

        # Increment to the next page
        page += 1

    # Save data to CSV
    df = pd.DataFrame(products)
    df.to_csv("office_national_products.csv", index=False)
    print("Scraping completed. Data saved to office_national_products.csv.")
    return products


# product_urls = get_product_urls()
# products_new = []
# for product_url in product_urls:

#     url = f"{product_url["URL"]}"
#     response = requests.get(
#         url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}
#     )
#     # time.sleep(0.2)
#     soup = BeautifulSoup(response.text, "html.parser")

#     try:
#         brand = soup.find("span", class_="brands-desc").text.strip()  # Update class
#     except AttributeError:
#         brand = None

#     try:
#         product_code = soup.find("span", id="childPartnumber").text.strip()
#     except AttributeError:
#         product_code = None

#     try:
#         product_reference = soup.find("span", id="childRefrenceNumber").text.strip()
#     except AttributeError:
#         product_reference = None

#     try:
#         price = soup.find("span", class_="price").text.strip()
#     except AttributeError:
#         price = None

#     try:
#         name = soup.find("h1", class_="product-name").text.strip()
#     except AttributeError:
#         name = None

#     products_new.append(
#         {
#             "Name": name,
#             "Price": price,
#             "Brand": brand,
#             "Product Code": product_code,
#             "Product Reference": product_reference,
#             "URL": product_url,
#         }
#     )

# get_product_urls()

# df = pd.DataFrame(products_new)
# df.to_csv("office_national_products.csv", index=False)
# print("Scraping completed. Data saved to office_national_products.csv.")
