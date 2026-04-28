# Amazon Playwright Tests

Automated end-to-end tests for Amazon.com product search, selection, and cart addition using Playwright, pytest, and Page Object Model. Tests run in parallel using pytest-xdist.

## Tech Stack
- **Python 3.9+**
- **Playwright** (sync API, Chromium)
- **pytest** (test runner)
- **pytest-playwright** (browser fixtures)
- **pytest-xdist** (parallel execution)

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd amazon-playwright-tests
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install chromium
   ```

## Running Tests

### Normal execution (headed Chromium)
```bash
pytest
```

### Headless execution
```bash
pytest --headed=false
```

### Parallel execution (auto-detect CPU cores)
```bash
pytest -n auto
```

### Specific browser
```bash
pytest --browser firefox
```

### HTML report
```bash
pytest --html=report.html
```

## Features
- **Page Object Model** for maintainable code
- **Defensive handling** of cookie/location popups
- **Robust locators** and auto-waits
- **Parallel safe** (isolated browser contexts per test)
- **Console output** of product title/price
- **Cart success verification**

## Assumptions & Limitations
- Tests Amazon.com (US) - region-specific selectors
- Amazon's dynamic UI/anti-bot measures may cause flakiness
- First sponsored/organic result used (prices fluctuate)
- No login required (guest cart)
- Chromium primary browser (others via `--browser`)

## Troubleshooting
- **Timeout errors**: Increase `expect_timeout` in page object
- **Popup blocks**: Run headed mode first to debug
- **Selector changes**: Update in `amazon_page.py` (use Playwright Inspector)
- **Parallel failures**: Ensure no shared state; each test gets fresh context
- **Browser issues**: `playwright install --with-deps chromium`
- **Captcha**: Use headed mode or residential proxies for production

## CI/CD Integration
```yaml
# .github/workflows/tests.yml
name: Tests
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with: { python-version: '3.11' }
    - run: pip install -r requirements.txt
    - run: playwright install --with-deps chromium
    - run: pytest -n auto --headed=false
```

Built for SDET interviews - production-grade, parallel-ready automation.