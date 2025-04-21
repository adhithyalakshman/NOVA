from flask import Flask, render_template, request, jsonify
from nova_act import NovaAct, ActError
from pydantic import BaseModel

from typing import Dict, List


app = Flask(__name__)


class Product(BaseModel):
    product_link: str
    price: float
    website : str

   

def search_product_on_website(product_name: str, website_url: str, website_name: str) -> Product | None:
    """Search for a product on a specific website and return its details."""
    try:
        
        with NovaAct(starting_page=website_url, ) as nova:
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
                nova.stop()
            
            
            
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
        print(f"Error searching {website_name}: {e}")
        return None



    
    # Use ThreadPoolExecutor to search across websites in parallel

    
 






@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        print(product_name)
        if not product_name:
            return render_template('home.html', error="Please enter a product name")
        
        # Websites to search
        websites: Dict[str, str] = {
             "Walmart": "https://www.walmart.com",
            
            "Flipkart": "https://www.flipkart.com",
            "Amazon": "https://www.amazon.com"
           
        }
        all_products: List[Product] = []
        for j in websites.items():
            x=search_product_on_website(product_name, j[1],j[0])
            if x is not None:
                all_products.append(x)


        
      
        
        # Sort products by price
        all_products.sort(key=lambda x: x.price)
        
        return render_template('home.html', 
                             products=all_products,
                             product_name=product_name,
                             best_deal=all_products[0] if all_products else None )
    
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True) 
           



 

    
 






    
