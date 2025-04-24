import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from product_bot import extract_product_name, compare_prices

# Load environment variables
load_dotenv()

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    goodbye = None

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        low = query.lower()

        # Handle exit commands
        if low in ["end", "exit", "quit"]:
            goodbye = "Thanks for using the Product Price Bot! You can close this page."
        else:
            product_name = extract_product_name(query)
            if "invalid query" in product_name.lower():
                error = (
                    "Please enter a valid product query. "
                    "Example: 'what is cost of hp pavilion plus'"
                )
            else:
                result = compare_prices(product_name)

    return render_template(
        "index.html",
        result=result,
        error=error,
        goodbye=goodbye
    )


if __name__ == "__main__":
    app.run(debug=True)
