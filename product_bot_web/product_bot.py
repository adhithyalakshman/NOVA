import os
from typing import List, Dict
from pydantic import BaseModel
from google import genai
from google.genai import types
from nova_act import NovaAct
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load API key from environment
API_KEY = "AIzaSyB2nmWsJ4zLqOG2Q1fFZEnfMKRG325yIhk"

# Initialize Gemini client
genai_client = genai.Client(api_key=API_KEY)


class Product(BaseModel):
    product_link: str
    price: float
    website: str


def extract_product_name(user_query: str) -> str:
    """
    Uses Gemini to extract brand and model from user_query.
    Returns 'invalid query' if it's not a product query.
    """
    try:
        response = genai_client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are a product information analyzer. Extract and return "
                    "only a single string in format brandname modelname from the user's query. "
                    "If the query is not about a product, return 'invalid query'. "
                    "Format: 'BRAND: brand_name, MODEL: model_name' or 'invalid query'."
                )
            ),
            contents=user_query
        )
        return response.text.strip()
    except Exception as e:
        print(f"[Gemini API Error] {e}")
        return "invalid query"


def compare_prices(product_name: str) -> List[Product]:
    """
    Searches Amazon, Flipkart, and Walmart for the given product_name.
    Returns a list of Product objects sorted by price.
    """
    def search_site(name: str, url: str) -> Product | None:
        try:
            with NovaAct(starting_page=url) as nova:
                nova.start()
                # Common search steps
                nova.act("wait for search box to appear")
                nova.act(f"type {product_name} in search box")
                nova.act("press enter")

                # Site-specific click
                if "amazon" in url:
                    nova.act("wait for first result to appear")
                    nova.act("click on first result")
                elif "flipkart" in url:
                    nova.act("wait for first product to appear")
                    nova.act("click on first result")
                elif "walmart" in url:
                    nova.act("wait for first item to appear")
                    nova.act("click on first item")

                # Extract details
                result = nova.act(
                    "get the product link",
                    schema=Product.model_json_schema()
                )
                if not result.matches_schema:
                    return None

                return Product(
                    product_link=result.parsed_response["product_link"],
                    price=result.parsed_response["price"],
                    website=name
                )
        except Exception as e:
            print(f"[{name} Error] {e}")
            return None

    websites: Dict[str, str] = {
        "Amazon": "https://www.amazon.com",
        "Flipkart": "https://www.flipkart.com",
        "Walmart": "https://www.walmart.com"
    }

    all_products: List[Product] = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(search_site, name, url): name for name, url in websites.items()}
        for future in as_completed(futures):
            prod = future.result()
            if prod:
                all_products.append(prod)

    # Sort by price ascending
    return sorted(all_products, key=lambda p: p.price)
    
           