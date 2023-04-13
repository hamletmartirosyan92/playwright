from playwright.sync_api import Playwright


def test_youtube(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    
    host = "https://youtube.com"
    page = browser.new_page()
    page.goto(host)
    page.wait_for_load_state()

    page.get_by_placeholder("Search").click()
    page.get_by_placeholder("Search").fill("cats")
    page.get_by_placeholder("Search").press("Enter")
    page.wait_for_timeout(5000)

    page_links = page.locator("#video-title")
    if not page_links.count() >= 10:
        print("there is less then 10 videos about cats")

    for link in page_links.all():
        uri = link.get_attribute('href')
        if uri:
            if '/watch' in uri:
                print(f'{host}{uri}')

    context.close()
    browser.close()
