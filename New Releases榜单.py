# https://www.amazon.com/gp/new-releases/home-garden/381142011/ref=zg_bs_tab_t_home-garden_bsnr
import os.path
from datetime import datetime
from DrissionPage import ChromiumPage
from lxml import etree
import requests
from tqdm import tqdm

day_date = datetime.now().strftime("%Y-%m-%d")
drive = ChromiumPage()  # 实例化浏览器对象
drive.get(
    r'https://www.amazon.com/gp/new-releases/home-garden/381142011/ref=zg_bs_tab_t_home-garden_bsnr')  # 跳转到亚马逊
x = 1  # 定义一个计数器给图片命名并计数
for i in range(1, 3):
    drive.wait(2)
    drive.scroll.down(3000)  # 增加滑动页面的动作,第一次滑动加载出三十八条
    drive.wait(4)  # 等待数据加载再滑动，不然滑到底不加载第五十条
    drive.scroll.down(1070)  # 追加滑动页面的动作，让数据能完整加载出五十条
    drive.wait(4)  # 等待数据加载,不然亚马逊不给你五十条商品的页面数据
    text = drive.html  # 获得当前页面的html数据返回成字符串的形式
    # 将HTML内容转换为etree对象
    tree = etree.HTML(text)
    # 使用XPath查找id为gridItemRoot的div中的img标签的src属性
    image_urls = tree.xpath('//div[@id="gridItemRoot"]//img/@src')
    path = r'C:\Users\Administrator\Desktop\Amz_New'  # 自定义路径,存放这个排行榜的图片
    time_path = os.path.join(path, day_date)
    if not os.path.exists(time_path):
        os.makedirs(time_path)
    for url in tqdm(image_urls, desc=f'正在爬取第{i}页'):
        with open(f'{time_path}/{x}.jpg', 'wb') as f:
            f.write(requests.get(url).content)  # 使用requests对获得的链接进行爬取并转码保存
        x += 1
    # for url in image_urls:
    #     drive.download(url, path, str(x))  # 使用DrissionPage的写法去获取图片
    #     x += 1
    drive.wait(1)  # 等待一下，不然这个下一页按钮不知道为什么加载不出来
    drive.ele('@text()=Next page').click()  # 寻找下一页
