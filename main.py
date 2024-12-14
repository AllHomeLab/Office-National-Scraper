import requests
from bs4 import BeautifulSoup
import pandas as pd
import http.client
import os

http.client._MAXHEADERS = 1000


# education, stationery, one-solution-products, ink-and-toner, paper-supplies, technology, furniture, warehouse-and-packaging, workwear--1


def get_products_from_category(category):
    products = []
    filepath = r"output/categories/"

    if os.path.exists(filepath + category + ".csv") == True:
        print("Already Exists")
        df = pd.read_csv(filepath + category + ".csv")
        return df

    # Get total number of pages & products
    seperator = "------------------------"
    base_url = "https://www.officenational.com.au/shop/en/onesolution/" + category
    query_params = "?fromPage=catalogEntryList&beginIndex={}&pageSize=36&pageView=grid"
    print(seperator)
    print(f"Scanning: {category}")
    url = base_url + query_params.format(0)
    response = requests.get(
        url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}
    )
    soup = BeautifulSoup(response.text, "html.parser")
    total_pages = int(soup.find_all("a", class_="hoverover")[-1]["data-page-number"])
    total_products = int(total_pages) * 32
    print("Total Pages: " + str(total_pages))
    print("Total Products: " + str(total_products))
    print(seperator)

    # iterate through all pages and retrieve all product URLs

    page = 1
    while page < total_pages:
        url = f"{base_url}{query_params.format((page-1)*32)}"
        response = requests.get(
            url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}
        )
        if response.status_code == 200:
            pass
        elif response.status_code == 401:
            print("You've been rate limited!")
        elif response.status_code == 404:
            print("Page not found!")
        else:
            print(response.status_code)
        soup = BeautifulSoup(response.text, "html.parser")

        print(
            f"Scraping page {page} / {total_pages} ({round(((page)/total_pages)*100,0)}%) Status Code: {response.status_code}"
        )

        # Find all product containers on page
        product_containers = soup.find_all("div", class_="product_info")

        for container in product_containers:

            # Find URL
            try:
                url = container.find("a")["href"]
            except AttributeError:
                print("Error!")
                url = None

            products.append({"URL": url, "Category": category})

        page += 1

    df = pd.DataFrame(products)
    df.to_csv(filepath + category + ".csv", index=False)
    print(
        f"Scraping {category} completed. Data saved to {filepath + category + ".csv"}"
    )
    return products


def combine_products():
    print("Combining")
    path = "output/categories/"
    filenames = os.listdir(path)
    df_all = pd.DataFrame()
    for filename in filenames:
        df = pd.read_csv(path + filename)
        df_all = pd.concat([df_all, df])
    df_all.to_csv(r"output/all_urls.csv", index=False)
    return df_all


def update_products():
    print("Updating")
    all_products = []
    df = pd.read_csv(r"output/all_urls.csv")
    total_products = len(df)

    for index, row in df.iterrows():
        url = row["URL"]
        response = requests.get(
            url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}
        )
        soup = BeautifulSoup(response.text, "html.parser")

        try:
            brand = soup.find("span", class_="brands-desc").text.strip()  # Update class
        except AttributeError:
            brand = None

        try:
            product_code = soup.find("span", id="childPartnumber").text.strip()
        except AttributeError:
            product_code = None

        try:
            product_reference = soup.find("span", id="childRefrenceNumber").text.strip()
        except AttributeError:
            product_reference = None

        try:
            price = soup.find("span", class_="price").text.strip()
        except AttributeError:
            price = None

        try:
            name = soup.find("h1", class_="product-name").text.strip()
        except AttributeError:
            name = None

        all_products.append(
            {
                "Name": name,
                "Price": price,
                "Brand": brand,
                "Product Code": product_code,
                "Product Reference": product_reference,
                "URL": url,
            }
        )

        print(
            f"Product Overview: {index+1}/{total_products} | {round(((index+1)/total_products)*100,1)}%"
        )
        print(f"Name: {name}")
        print(f"Price: {price}")
        print(f"Product Code: {product_code}")
        print("\n")

    df = pd.DataFrame(all_products)
    df.to_csv("/output/office_national_products.csv", index=False)
    print("Scraping completed. Data saved to office_national_products.csv.")


categories = [
    "education",
    "stationery",
    "one-solution-products",
    "ink-and-toner",
    "paper-supplies",
    "technology",
    "furniture",
    "warehouse-and-packaging",
    "workwear--1",
]

for category in categories:
    products = []
    get_products_from_category(category)
df = combine_products()
update_products()
