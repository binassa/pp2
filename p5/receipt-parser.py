import re
import json

with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()
#1 Extract all prices from the receipt
price_pattern = r"\d[\d\s]*,\d{2}"
prices = re.findall(price_pattern, text)

#2 Find all product names
product_pattern = r"\d+\.\s*\n(.+)"
products = re.findall(product_pattern, text)

#3 Calculate total amount
total_pattern = r"ИТОГО:\s*\n([\d\s]+,\d{2})"
total_match = re.search(total_pattern, text)
total_amount = total_match.group(1) if total_match else None

#4 Extract date and time information
datetime_pattern = r"Время:\s*([\d\.]+\s[\d:]+)"
datetime_match = re.search(datetime_pattern, text)
datetime = datetime_match.group(1) if datetime_match else None

#5 Find payment method
payment_pattern = r"(Банковская карта|Наличные)"
payment_match = re.search(payment_pattern, text)
payment_method = payment_match.group(1) if payment_match else None

#6 Create a structured output
receipt_data = {
    "products": products,
    "prices": prices,
    "total_amount": total_amount,
    "datetime": datetime,
    "payment_method": payment_method
}

print(json.dumps(receipt_data, indent=4, ensure_ascii=False))