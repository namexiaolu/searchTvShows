from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import threading


def setup_chrome_driver(headless=True, mobile_emulation=None):
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    if headless:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    if mobile_emulation:
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def pan666(keyword):
    driver = setup_chrome_driver()
    try:
        base_url = "https://pan666.net/"
        search_url = f"{base_url}?sort=newest&q={keyword}"
        driver.get(search_url)
        time.sleep(2)

        page_content = driver.page_source
        soup = BeautifulSoup(page_content, 'html.parser')
        discussion_items = soup.find_all('div', class_='DiscussionListItem-content Slidable-content')

        links_to_visit = set()
        for i, item in enumerate(discussion_items, start=1):
            links = item.find_all('a', href=True)
            for link in links:
                if len(link['href']) <= 10:
                    continue
                full_link = base_url + link['href']
                links_to_visit.add(full_link)
                # print(f"条目 {i} 链接: {full_link}")

        alipan_links_set = set()
        for link in links_to_visit:
            driver.get(link)
            time.sleep(2)
            new_page_content = driver.page_source
            if keyword not in new_page_content:
                continue
            new_soup = BeautifulSoup(new_page_content, 'html.parser')
            alipan_links = new_soup.find_all('a', href=True)
            for alipan_link in alipan_links:
                href = alipan_link['href']
                if href.startswith("https://www.alipan.com"):
                    alipan_links_set.add(href)
                    driver.get(href)
                    time.sleep(1)
                    alipan_page_content = driver.page_source
                    if "来晚啦，该分享已失效" not in alipan_page_content and "该文件已禁止访问" not in alipan_page_content:
                        print(f"有效链接: {alipan_link}")
    finally:
        driver.quit()


def btnull(keyword):
    mobile_emulation = {"deviceName": "iPhone 14 Pro Max"}
    driver = setup_chrome_driver(mobile_emulation=mobile_emulation)
    try:
        url = 'https://www.btnull.in/s/1---1/'
        driver.get(url + keyword)
        time.sleep(2)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        sr_lists_section = soup.find('section', class_='sr_lists')
        first_a_tag = sr_lists_section.find('a') if sr_lists_section else None

        if first_a_tag:
            link = first_a_tag['href']
            seturl = 'https://www.btnull.in'
            print(f"链接: {link}")
            driver.get(seturl + link)
            time.sleep(2)
            new_page_content = driver.page_source
            new_soup = BeautifulSoup(new_page_content, 'html.parser')
            alipan_links = new_soup.find_all('a', href=True)
            for alipan_link in alipan_links:
                href = alipan_link['href']
                if href.startswith("https://www.alipan.com"):
                    print(href)
        else:
            print("未找到 class 为 'sr_lists' 的 section 标签下的 a 标签")
    finally:
        driver.close()


if __name__ == "__main__":
    keyword = input("请输入关键字：")

    thread1 = threading.Thread(target=pan666, args=(keyword,))
    thread2 = threading.Thread(target=btnull, args=(keyword,))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print("两个线程都已完成")