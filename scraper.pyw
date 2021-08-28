import os
import time
from bs4 import BeautifulSoup
import requests
import webhook

while (True):
    if not os.path.exists("src/urls.txt"):
        print("No Urls loaded. Exiting")
        exit()
    file_object = open('src/urls.txt', 'r')
    urls = file_object.readlines()
    for i in urls:
        page = requests.get(i)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            #Get Price
            old_price = soup.find('div', attrs={'class':'discount_original_price'})
            final_og_price = old_price.text.strip()
            new_price = soup.find('div', attrs={'class':'discount_final_price'})
            final_new_price = new_price.text.strip()
            percent = soup.find('div', attrs={'class':'discount_pct'})
            final_percent = percent.text.strip()
            name = i.split("/")[5]

            #If name contains underscore replace with space
            if "_" in name:
                name = name.replace("_", " ")

            #If file with price does not exist send Message with Discount and write price to file
            if not os.path.exists(f"src/{name}.txt"):
                with open(f"src/{name}.txt", "w") as file:
                    file.write(final_new_price)
                    webhook.sendHook(name, final_og_price, final_new_price, final_percent, i, "Not Found")

            #Checks if Discount Price is same or changed
            with open(f"src/{name}.txt", "r") as f:
                text = f.readlines()
                if final_new_price in text:
                    webhook.sendLog(f"Price for {name} didnt Change")
                else:
                    webhook.sendLog(f"Price for {name} has changed from {text[0]} to {final_new_price}")
                    webhook.sendHook(name, final_og_price, final_new_price, final_percent, i, text[0])

            #Writes current Discount to file
            with open(f"src/{name}.txt", "w") as file:
                file.write(final_new_price)

        except Exception:
            normal_price = soup.find('div', attrs={'class':'game_purchase_price price'})
            final_price = normal_price.text.strip()
            name = i.split("/")[5]
            if "_" in name:
                name = name.replace("_", " ")
            webhook.sendLog(f"No Discount on {name}")
    time.sleep(60 * 60)