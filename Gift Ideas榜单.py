# https://www.amazon.com/gp/most-gifted/home-garden/381142011/ref=zg_mw_tab_t_home-garden_mg
import os
from datetime import datetime
from DrissionPage import ChromiumPage
from lxml import etree
import requests
from tqdm import tqdm

drive = ChromiumPage()  # 实例化浏览器对象
drive.get(
    r'https://www.amazon.com/gp/most-gifted/home-garden/381142011/ref=zg_mw_tab_t_home-garden_mg')  # 跳转到亚马逊
x = 1  # 定义一个计数器给图片命名并计数
for i in range(1, 3):
    drive.wait(2)  # 等待网页加载
    drive.scroll.down(3000)  # 增加滑动页面的动作,第一次滑动加载出三十八条
    drive.wait(4)  # 等待数据加载再滑动，不然滑到底不加载第五十条
    drive.scroll.down(1050)  # 追加滑动页面的动作，让数据能完整加载出五十条
    drive.wait(4)  # 等待数据加载,不然亚马逊不给你五十条商品的页面数据
    drive.scroll.down(200)  # 追加滑动页面的动作，让数据能完整加载出五十条
    drive.wait(4)
    text = drive.html  # 获得当前页面的html数据返回成字符串的形式
    # 将HTML内容转换为etree对象
    tree = etree.HTML(text)
    # 使用XPath查找id为gridItemRoot的div中的img标签的src属性
    image_urls = tree.xpath('//div[@id="gridItemRoot"]//img/@src')
    path = r'C:\Users\Administrator\Desktop\Amz_Gift'  # 自定义路径,存放这个排行榜的图片
    day_path = os.path.join(path, datetime.today().strftime('%Y-%m-%d'))  # 定义一个按照年月日命名的文件夹
    # 检测这个文件夹是否存在,如果未创建就创建
    if not os.path.exists(day_path):
        os.mkdir(day_path)  # 按照路径创建文件夹
    for url in tqdm(image_urls, desc=f'正在爬取new榜单第{i}页'):
        # 将文件夹保存到day_path中,如果图片重名会直接覆盖
        with open(f'{day_path}/{x}.jpg', 'wb') as f:
            f.write(requests.get(url).content)  # 使用requests对获得的链接进行爬取并转码保存
        x += 1
    # for url in image_urls:
    #     drive.download(url, path, str(x))  # 使用DrissionPage的写法去获取图片，优点是能直接处理重名问题，直接在重名文件后缀加上_和数字
    #                                        # 写法简单易懂适合初学者,但是进度条不好看有些乱
    #     x += 1
    drive.wait(1)  # 等待一下,不然这个下一页按钮不知道为什么加载不出来
    # 寻找不到下一页按钮，直接跳转到第二页的链接去了
    drive.get('https://www.amazon.com/gp/most-gifted/home-garden/381142011/ref=zg_mg_pg_2_home-garden?ie=UTF8&pg=2')
