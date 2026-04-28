"""
B站自动化测试脚本
整合了搜索、滚动、登录功能
"""
import pytest
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def test_bilibili_search(search_and_switch):
    """测试搜索功能"""
    print("\n=== 测试搜索功能 ===")

    # 使用fixture执行搜索
    driver = search_and_switch("自动化测试")

    # 验证搜索结果
    assert "自动化测试" in driver.title or "搜索" in driver.title
    assert "search" in driver.current_url

    print(f"✅ 搜索测试通过")
    print(f"页面标题: {driver.title}")
    print(f"页面URL: {driver.current_url}")


def test_scroll_pagination(browser, auto_scroll):
    """测试滚动翻页功能"""
    print("\n=== 测试滚动翻页功能 ===")

    # 直接打开搜索页
    browser.get("https://search.bilibili.com/video?keyword=自动化测试")
    time.sleep(3)

    # 使用滚动fixture
    scroll_func = auto_scroll
    video_titles = scroll_func(browser, page_count=2)

    # 验证结果
    assert len(video_titles) > 0, "未捕获到任何视频标题"

    print(f"✅ 滚动测试通过")
    print(f"共捕获 {len(video_titles)} 个视频标题")
    for i, title in enumerate(video_titles[:5], 1):
        print(f"  {i}. {title[:50]}...")


def test_cookie_login(browser):
    """测试Cookie登录功能"""
    print("\n=== 测试Cookie登录功能 ===")

    try:
        # 1. 先访问首页
        browser.get("https://www.bilibili.com")
        time.sleep(2)

        # 2. 读取Cookie文件
        with open('json', 'r') as f:
            cookies = json.load(f)

        # 3. 添加Cookie
        for cookie in cookies:
            if 'sameSite' in cookie and cookie['sameSite'] not in ["Strict", "Lax", "None"]:
                cookie.pop('sameSite')
            browser.add_cookie(cookie)

        # 4. 刷新页面
        browser.refresh()
        time.sleep(3)

        # 5. 访问需要登录的页面验证
        browser.get("https://t.bilibili.com/")
        time.sleep(2)

        # 验证登录成功
        assert "动态" in browser.title or "个人中心" in browser.title
        print(f"✅ Cookie登录测试通过")
        print(f"登录后页面: {browser.title}")

    except FileNotFoundError:
        print("⚠️ 跳过Cookie登录测试: token.json文件不存在")
        pytest.skip("需要token.json文件")
    except Exception as e:
        print(f"❌ Cookie登录失败: {e}")
        raise


def test_integrated_search_scroll(search_and_switch, auto_scroll):
    """整合测试：搜索 + 滚动翻页"""
    print("\n=== 整合测试：搜索 + 滚动翻页 ===")

    # 1. 搜索并切换到搜索页
    driver = search_and_switch("Python编程")

    # 2. 在搜索结果页滚动
    scroll_func = auto_scroll
    video_titles = scroll_func(driver, page_count=2)

    # 3. 验证结果
    assert len(video_titles) > 0, "未捕获到任何视频标题"
    assert "search" in driver.current_url

    print(f"✅ 整合测试通过")
    print(f"共捕获 {len(video_titles)} 个视频标题")
    print(f"最后页面: {driver.title}")


if __name__ == "__main__":
    # 可以直接运行python bilibili_test.py
    import pytest

    pytest.main(["-v"])