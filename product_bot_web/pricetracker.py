from nova_act import NovaAct, ActError
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List



class Product(BaseModel):
    product_link: str
    price: float
    website : str

   

def search_product_on_website(product_name: str, website_url: str, website_name: str) -> Product | None:
    """Search for a product on a specific website and return its details."""
    try:
        with NovaAct(starting_page=website_url) as nova:
            nova.start()
              # Wait for initial page load
            
            # Different search commands for different websites
            if "amazon" in website_url.lower():
                nova.act("wait for search box to appear")
                nova.act(f"type {product_name} in search box")
                nova.act("press enter")
                nova.act("wait for first result to appear")
                nova.act("click on first result")
            elif "flipkart" in website_url.lower():
                nova.act("wait for search box to appear")
                nova.act(f"type {product_name} in search box")
                nova.act("press enter")
                
                nova.act("wait for first product to appear")
                nova.act("click on first result")
            elif "walmart" in website_url.lower():
                nova.act("wait for search box to appear")
                nova.act(f"type {product_name} in search box")
                nova.act("press enter")
               
                nova.act("wait for first item to appear")
                nova.act("click on first item")
            
              # Wait for product page to load
            
            # Get product details
            pl = nova.act("get the product link", schema=Product.model_json_schema())
            if not pl.matches_schema:
                print(f"Failed to get link from {website_name}")
                return None
            
          
            
            # Combine results
            product = Product(
                product_link=pl.parsed_response["product_link"],
                price=pl.parsed_response["price"],
                website=website_name
            )
            return product
            
    except Exception as e:
        print(f"Error searching {website_name}: {str(e)}")
        return None

def main():
    # Product to search for
    product_name = input("ENTER THE PRODUCT NAME WITH MODEL NUMBER:")
    
    # Websites to search
    websites: Dict[str, str] = {
        "Amazon": "https://www.amazon.com",
        "Flipkart": "https://www.flipkart.com",
        "Walmart": "https://www.walmart.com"
    }
    
    all_products: List[Product] = []
    
    # Use ThreadPoolExecutor to search across websites in parallel
    with ThreadPoolExecutor(max_workers=1) as executor:
        # Submit all searches
        future_to_website = {
            executor.submit(search_product_on_website, product_name, url, name): name 
            for name, url in websites.items()
        }
        
        # Collect results
        for future in as_completed(future_to_website.keys()):
            website_name = future_to_website[future]
            try:
                product = future.result()
                if product is not None:
                    all_products.append(product)
                    print(f"\nFound on {website_name}:")
                    print(f"  Link: {product.product_link}")
                    print(f"  Price: ${product.price:.2f}")
            except Exception as e:
                print(f"Error processing {website_name}: {str(e)}")
    
    # Sort products by price
    all_products.sort(key=lambda x: x.price)
    
    print("\n=== Price Comparison Summary ===")
    for product in all_products:
        print(f"{product.product_link}: ${product.price:.2f}")
    
    if all_products:
        print(f"\nBest deal: {all_products[0].website} at ${all_products[0].price:.2f}")
    else:
        print("\nNo products found on any website")

if __name__ == "__main__":
    main()
