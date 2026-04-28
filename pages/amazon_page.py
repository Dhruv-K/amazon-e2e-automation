"""Amazon Page Object Model for search and cart operations."""
from playwright.sync_api import Page, expect


class AmazonPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        """Navigate to Amazon.com."""
        self.page.goto("https://www.amazon.com", wait_until="networkidle")

    def handle_popups(self):
        """Handle cookie consent and location popups defensively."""
        # Cookie consent - multiple possible selectors
        cookie_selectors = [
            '[data-csa-c-id="uxgz4h-ew6d5f-vqjw6p-6x7l2q-zr7n1k"] button[aria-label*="Accept"]',
            '#sp-cc-accept',
            '[name="accept"]',
            'input[value="Accept"]',
            '#accept-cookies-button'
        ]
        for selector in cookie_selectors:
            if self.page.locator(selector).is_visible(timeout=2000):
                self.page.click(selector)
                break

        # Location popup
        location_selectors = [
            '#nav-global-location-popover-link',
            '[id*="GLUX"] button[aria-label*="Continue"]',
            'span[data-action*="dismiss"]'
        ]
        for selector in location_selectors:
            if self.page.locator(selector).is_visible(timeout=2000):
                self.page.click(selector)
                break

    def search_product(self, query: str):
        """Search for product and return first result details."""
        search_input = self.page.locator('#twotabsearchtextbox')
        search_button = self.page.locator('#nav-search-submit-button')

        search_input.fill(query)
        search_button.click()
        self.page.wait_for_load_state("networkidle")

        # Wait for results
        expect(self.page.locator('.s-main-slot')).to_be_visible()

        # First product link (skip sponsored if possible)
        first_product = self.page.locator(
            'div[data-component-type="s-search-result"] a.a-link-normal:first-of-type'
        ).first
        expect(first_product).to_be_visible()

        product_title = first_product.locator('h2 span').inner_text()
        product_link = first_product.get_attribute("href")

        return product_title, product_link

    def select_product(self, product_link: str):
        """Open product PDP and return price."""
        self.page.goto(product_link, wait_until="networkidle")
        expect(self.page.locator("#productTitle")).to_be_visible()

        # Multiple price selectors for robustness
        price_selectors = [
            '.a-price.aok-align-center.reinventPricePriceToPayMargin span.a-offscreen',
            '#corePrice_feature_div .a-offscreen',
            '#priceblock_ourprice',
            '#priceblock_dealprice',
            'span.a-price-whole',
            '.a-price span[aria-hidden="true"]'
        ]
        price_elem = None
        for selector in price_selectors:
            try:
                price_elem = self.page.locator(selector).first
                expect(price_elem).to_be_visible(timeout=5000)
                break
            except:
                continue

        if not price_elem:
            raise Exception("Price not found")

        product_title = self.page.locator("#productTitle").inner_text().strip()
        price_text = price_elem.inner_text().strip()

        return product_title, price_text

    def add_to_cart(self):
        """Add product to cart and verify success."""
        add_to_cart_btn = self.page.locator('#add-to-cart-button')
        expect(add_to_cart_btn).to_be_visible()
        expect(add_to_cart_btn).to_be_enabled()

        add_to_cart_btn.click()

        # Wait for success indicator
        success_selectors = [
            "#addToCartMessage",
            ".a-alert-success",
            '[data-cel-widget*="addedToCart"]'
        ]
        for selector in success_selectors:
            if self.page.locator(selector).is_visible(timeout=10000):
                return True

        # Alternative: check cart mini
        self.page.click("#nav-cart")
        expect(self.page.locator(".a-size-medium.sc-your-order")).to_be_visible(timeout=5000)
        return True