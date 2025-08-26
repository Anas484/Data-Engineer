import requests
import random

def get_random_product():
    url = "https://api.freeapi.app/api/v1/public/randomproducts"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    data = response.json()

    if data.get("success") and "data" in data:
        product_list = data["data"].get("data", [])
        if product_list:
            product = random.choice(product_list)
            prod_dict = {
                "id": product.get("id"),
                "title": product.get("title"),
                "price": product.get("price"),
                "category": product.get("category"),
            }
            return prod_dict 
        else:
            raise Exception("No product data found.")
    else:
        raise Exception("Failed to fetch product data.")

def main():
    try:
        product = get_random_product()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
