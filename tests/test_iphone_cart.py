"""Test iPhone search and cart addition on Amazon."""
import pytest
from pages.amazon_page import AmazonPage


@pytest.mark.smoke
def test_iphone_search_add_to_cart(page):
    amazon = AmazonPage(page)
    amazon.navigate()
    amazon.handle_popups()

    # Search iPhone
    title, link = amazon.search_product("iPhone 15")
    print(f"\n📱 Found iPhone: {title}")

    # Select product
    pdp_title, price = amazon.select_product(link)
    print(f"💰 iPhone PDP - Title: {pdp_title}")
    print(f"💰 iPhone Price: {price}")

    # Add to cart
    success = amazon.add_to_cart()
    assert success, "Failed to add iPhone to cart"
    print("✅ iPhone successfully added to cart!")