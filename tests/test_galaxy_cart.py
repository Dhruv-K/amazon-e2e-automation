"""Test Galaxy device search and cart addition on Amazon."""
import pytest
from pages.amazon_page import AmazonPage


@pytest.mark.smoke
def test_galaxy_search_add_to_cart(page):
    amazon = AmazonPage(page)
    amazon.navigate()
    amazon.handle_popups()

    # Search Galaxy
    title, link = amazon.search_product("Galaxy S24")
    print(f"\n📱 Found Galaxy: {title}")

    # Select product
    pdp_title, price = amazon.select_product(link)
    print(f"💰 Galaxy PDP - Title: {pdp_title}")
    print(f"💰 Galaxy Price: {price}")

    # Add to cart
    success = amazon.add_to_cart()
    assert success, "Failed to add Galaxy to cart"
    print("✅ Galaxy successfully added to cart!")