import os
import json
import smtplib
import requests
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}
product_url = "https://www.amazon.in/AMD-Ryzen-5600-Processor-100-100000927BOX/dp/B09VCHR1VH/?_encoding=UTF8&pd_rd_w=fmdLk&content-id=amzn1.sym.e5c03be3-10ba-4bc8-b9be-6fcea12320ed%3Aamzn1.symc.adba8a53-36db-43df-a081-77d28e1b71e6&pf_rd_p=e5c03be3-10ba-4bc8-b9be-6fcea12320ed&pf_rd_r=FX1S7NMKA6J2NJ748X92&pd_rd_wg=FFEu8&pd_rd_r=919c3ca0-393c-4cbd-87c4-8032eb2b1f2e&ref_=pd_gw_ci_mcx_mr_hp_atf_m"
target_price = 13000
mail_id = os.getenv("MAIL_ID")
pswrd = os.getenv("MAIL_PASS")
receiver = os.getenv("MAIL_ID")


# Scrapes the webpage to get the current price
def get_current_price(url):
    """Returns price: int, name: str, img: str"""
    webpage = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(webpage.text, "lxml")

    product_img = soup.select_one(
        selector="div[class='a-section _p13n-desktop-sims-fbt_fbt-desktop_image-background__DVFnZ'] div div img"
    ).get("data-a-dynamic-image")
    product_name = soup.select_one(selector="#title span")
    price_str = soup.find(class_="a-price-whole")
    price_str.find(class_="a-price-decimal").extract()

    return int(price_str.text.replace(",", "")), product_name.text, list(json.loads(product_img).keys())[-1]


def send_mail():
    message = MIMEMultipart("alternative")
    message["Subject"] = "🤩Price Drop Alert !!!🤑🤑"

    body = MIMEText(f"{product}<br>@₹{current_price} only.<br><br><img src='{img}'><br><br><a href={product_url}>Go to product page.</a>", "html")
    message.attach(body)

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=mail_id, password=pswrd)
        connection.sendmail(
            from_addr=mail_id,
            to_addrs=receiver,
            msg=message.as_string()
        )


try:
    current_price, product, img = get_current_price(product_url)
except AttributeError:
    print("Cannot access the webpage, please try after some time.")
    exit()

print(f"\n{product}\nCurrent Price: {current_price}\nTarget Price: {target_price}")

if current_price < target_price:
    send_mail()
    print("\nMail Sent")
else:
    print("\nMail Not Sent")
