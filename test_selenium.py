"""
Test GitHub signup accessibility.
Proxy is optional — set via env var:
  export CHROME_PROXY=socks5://127.0.0.1:9050
  python test_selenium.py

Without proxy (test IP directly):
  python test_selenium.py
"""
import os
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CHROMEDRIVER_PATH = "/home/beni/github-account-creator-bot/chromedriver"
CHROME_BINARY     = "/usr/bin/chromium"
CHROME_PROXY      = os.environ.get("CHROME_PROXY", "")

print("=" * 50)
print(f"Proxy  : {CHROME_PROXY if CHROME_PROXY else 'none (direct IP)'}")
print("=" * 50)

# ── Launch browser ────────────────────────────────────────────────────────────
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
if CHROME_PROXY:
    options.add_argument(f"--proxy-server={CHROME_PROXY}")
    options.add_argument("--disable-webrtc")

print("Starting undetected Chrome...")
driver = uc.Chrome(
    driver_executable_path=CHROMEDRIVER_PATH,
    browser_executable_path=CHROME_BINARY,
    options=options,
    headless=True,
    version_main=150,
)
wait = WebDriverWait(driver, 30)

# ── Show current IP ───────────────────────────────────────────────────────────
try:
    driver.get("https://api.ipify.org?format=json")
    time.sleep(2)
    print(f"Browser IP : {driver.find_element(By.TAG_NAME, 'body').text}")
except Exception as e:
    print(f"IP check failed: {e}")

# ── Open GitHub signup ────────────────────────────────────────────────────────
print("\nOpening https://github.com/signup ...")
driver.get("https://github.com/signup")

print("Waiting for page to render (up to 30s)...")
try:
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
    print("✅ Input elements detected.")
except Exception:
    print("⚠️  No inputs after 30s — page may be blocked or JS-heavy.")

print(f"\nURL   : {driver.current_url}")
print(f"Title : {driver.title}")

# ── Check inputs ──────────────────────────────────────────────────────────────
inputs = driver.find_elements(By.TAG_NAME, "input")
print(f"\nFound {len(inputs)} input(s):")
for inp in inputs:
    print(f"  id={inp.get_attribute('id')!r:30s}  type={inp.get_attribute('type')!r}")

# ── Bot-detection check ───────────────────────────────────────────────────────
page = driver.page_source.lower()
bad  = ["access is temporarily restricted", "unusual activity",
        "captcha", "recaptcha", "hcaptcha", "turnstile",
        "verify you are human", "robot"]
print("\nBot-detection check:")
blocked = False
for w in bad:
    if w in page:
        print(f"  ⚠️  '{w}' FOUND")
        blocked = True
    else:
        print(f"  ✅  '{w}' not found")

print()
if not blocked and len(inputs) > 0:
    print("🎉 GitHub signup is ACCESSIBLE — bot can proceed!")
elif not blocked and len(inputs) == 0:
    print("⚠️  No block detected but no inputs either — page may still loading.")
    print("   Try increasing wait time or check the screenshot.")
else:
    print("❌ GitHub is blocking this IP/session.")
    print("   Options:")
    print("   1. Use mobile hotspot (different IP)")
    print("   2. Use a residential proxy:")
    print("      export CHROME_PROXY=socks5://user:pass@proxy:port")
    print("      python test_selenium.py")
    print("   3. Deploy bot on a fresh VPS")

driver.save_screenshot("/tmp/github_signup_test.png")
# Also copy to project folder for easy viewing on Windows
try:
    import shutil
    shutil.copy("/tmp/github_signup_test.png",
                "/home/beni/github-account-creator-bot/github_signup_test.png")
    print("\nScreenshot: github_signup_test.png (also in project folder)")
except Exception:
    print("\nScreenshot: /tmp/github_signup_test.png")

driver.quit()
