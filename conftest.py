"""
pytest配置文件，定义核心fixture
"""
import pytest
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="function")
def browser():
    """基础浏览器fixture，每个测试用例一个浏览器实例"""
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def search_and_switch(browser):
    """
    整合fixture：搜索 + 窗口句柄切换
    返回一个搜索函数
    """

    def _search(keyword="自动化测试"):
        """
        执行搜索并切换到搜索结果页
        """
        # 1. 打开B站首页
        browser.get("https://www.bilibili.com")
        time.sleep(2)

        # 2. 获取当前窗口句柄
        original_window = browser.current_window_handle

        # 3. 执行搜索
        try:
            search_box = browser.find_element(By.CLASS_NAME, "nav-search-input")
            search_box.clear()
            search_box.send_keys(keyword)
            search_box.send_keys(Keys.ENTER)
            time.sleep(3)

            # 4. 切换到新窗口
            for window in browser.window_handles:
                if window != original_window:
                    browser.switch_to.window(window)
                    print(f"已切换到搜索页: {browser.title}")
                    time.sleep(2)
                    return browser

        except Exception as e:
            print(f"搜索失败: {e}")
            browser.switch_to.window(original_window)
            raise

        return browser

    return _search


@pytest.fixture(scope="function")
def auto_scroll():
    """
    自动滚动翻页fixture
    返回一个滚动函数
    """

    def _scroll(driver, page_count=3, scroll_step=200, interval=0.2):
        """
        自动滚动和翻页功能
        """
        video_titles = []

        def slow_scroll_to_bottom():
            """缓慢滚动到底部"""
            last_height = driver.execute_script("return document.body.scrollHeight")
            current_position = 0

            while current_position < last_height:
                next_position = min(current_position + scroll_step, last_height)
                driver.execute_script(f"window.scrollTo(0, {next_position});")
                time.sleep(interval)
                current_position = next_position

                # 捕获视频标题
                try:
                    videos = driver.find_elements(By.CSS_SELECTOR, ".bili-video-card__info--tit")
                    for video in videos:
                        title = video.text
                        if title and title not in video_titles:
                            video_titles.append(title)
                except:
                    pass

                # 检查页面是否变长
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height > last_height:
                    last_height = new_height

        def go_to_next_page():
            """尝试翻页"""
            try:
                # 多种方式查找下一页按钮
                next_selectors = [
                    "//*[contains(text(), '下一页')]",
                    "//*[contains(text(), '下一頁')]",
                    "//*[contains(text(), 'next')]",
                    "//*[contains(text(), 'Next')]"
                ]

                for xpath in next_selectors:
                    try:
                        buttons = driver.find_elements(By.XPATH, xpath)
                        for button in buttons:
                            if button.is_displayed() and button.is_enabled():
                                driver.execute_script("arguments[0].scrollIntoView(true);", button)
                                time.sleep(1)
                                button.click()
                                time.sleep(3)  # 等待新页面加载
                                return True
                    except:
                        continue
            except Exception as e:
                print(f"翻页失败: {e}")

            return False

        # 主滚动逻辑
        for page_num in range(page_count):
            print(f"处理第 {page_num + 1} 页")

            # 滚动当前页
            slow_scroll_to_bottom()
            print(f"第{page_num + 1}页捕获到 {len(video_titles)} 个视频")

            # 如果不是最后一页，尝试翻页
            if page_num < page_count - 1:
                if not go_to_next_page():
                    print("可能是无限滚动，继续向下滚动...")
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)

        return video_titles

    return _scroll