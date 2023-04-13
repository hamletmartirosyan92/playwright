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
    assert page_links.count() >= 10, "there is less then 10 videos about cats"

    links = []
    for link in page_links.all():
        uri = link.get_attribute('href')
        if uri:
            if '/watch' in uri:
                links.append(f'{host}{uri}')

        if len(links) == 10:
            break

    print(links)

    context.close()
    browser.close()
