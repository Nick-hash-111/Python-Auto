B站自动化测试脚本
项目简介
基于 Pytest + Selenium 搭建的轻量级 Web 自动化测试脚本。针对 B 站核心搜索功能实现了端到端的测试闭环，重点解决了多窗口句柄切换、动态懒加载页面滚动，以及 Cookie 免密登录等企业级测试痛点。
核心技术栈
测试框架: Pytest(高效的 Python 测试框架)
自动化工具: Selenium(WebDriver 浏览器驱动)
辅助工具: JSON(本地 Cookie 持久化缓存)
核心技术: 窗口句柄切换、显式/隐式等待、JavaScript 页面滚动、异常处理机制

项目亮点 
多窗口智能切换: 精准捕获搜索动作触发的新窗口句柄，解决点击搜索后页面跳转的元素定位失效问题。
动态懒加载处理: 自定义 JavaScript 缓慢滚动算法，配合显式等待，完美适配 B 站瀑布流式的视频列表动态加载。
Cookie 免密登录: 将登录凭证序列化存入本地 token.json，脚本启动时自动注入 Cookie，绕过验证码拦截，极大提升脚本执行效率。
高内聚 Fixture 设计: 采用 Pytest 的 yield机制封装前置操作（打开浏览器、初始化环境）与后置清理（关闭浏览器），保证每个测试用例的绝对隔离。

如何运行 
安装依赖: pip install pytest selenium
准备环境: 确保本地安装了与 Chrome 版本匹配的 ChromeDriver。
运行测试: 在命令行执行 pytest bilibili_test.py -v即可看到详细的测试过程与结果打印。
生成测试报告:在根目录执行pytest --html=report.html  


项目结构
bilibili_test.py: 主测试脚本，包含搜索、滚动、登录及整合测试四大核心用例。
conftest.py: Pytest 核心配置文件，封装了 browser、search_and_switch、auto_scroll等可复用的 Fixture 工具。
token.json: 登录态缓存文件（需自行在浏览器开发者工具中复制 B 站的登录 Cookie 并保存至此目录）。