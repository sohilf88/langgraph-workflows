# from playwright.sync_api import sync_playwright
# with sync_playwright() as play:
#     browser=play.chromium.launch(headless=False)
#     page=browser.new_page()
#     page.goto("https://chartink.com/screener/ema50-with-macd")
#    #  page.wait_for_timeout(2000)
#     page.reload()
#    #  page.locator("button:text('Generate')").click()
#     page.get_by_role("button",name="Generate").click()
#    #  page.get_by_role("",name="Input text cannot be blank.").inner_text()
#     page.get_by_placeholder("Input text cannot be blank.").inner_text()
import re
for name in dir(re):
    obj = getattr(re, name)
    if callable(obj):
        print(f"{name} -> Method/Function")
    else:
        print(f"{name} -> Attribute")