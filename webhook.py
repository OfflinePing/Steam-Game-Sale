import requests

url = "mywebhook"
log_url = "mywebhook"

def sendLog(content):
    data = {"content" : content, "username" : "Logs"}
    result = requests.post(log_url, json = data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
def sendHook(game, og_price, new_price, discount, link, old_price):
    data = {"content" : "New Game Discount: <@&881011767445159947>"}
    data["embeds"] = [
        {
            "description" : f"New Discount found!\r\n\r\nOriginal Price: {og_price}\r\nOld Price: {old_price}\r\nNew Price: {new_price}\r\nDiscount: {discount}\r\nLink: {link}",
            "title" : f"{game}"
        }
    ]
    result = requests.post(url, json = data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)