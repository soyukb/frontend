from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os

# ChromeDriverのパスを指定
# スクリプトのディレクトリを取得
script_dir = os.path.dirname(os.path.abspath(__file__))

# スクリプトのディレクトリにある "chromedriver.exe" を指定
driver_path = os.path.join(script_dir, "chromedriver.exe")
chrome_service = Service(driver_path)  # ChromeDriverのパスを適切に指定
driver = webdriver.Chrome(service=chrome_service)

# HTMLファイルのパスを指定して開く
html_path = r"C:\Users\soyuk\OneDrive\デスクトップ\portfolio2\backend\myproject\ArticleSnap\logic\output.html"  # HTMLファイルのパスを適切に指定
driver.get(html_path)

# icon-name="join-outline" を持つ SVG タグを取得
svg_elements = driver.find_elements(By.TAG_NAME, "svg")
join_outline_svg = [svg for svg in svg_elements if svg.get_attribute("icon-name") == "join-outline"]
print(join_outline_svg)
        
# "packaged-media-json"属性を取得
# packaged_media_json = player_element.get_attribute("join-outline")

# svg_elements = driver.find_elements(By.XPATH, '//svg[@icon-name="join-outline"]')

# SVG タグの情報を表示
# for idx, svg in enumerate(img_urls, start=1):
#     # SVGタグ全体を取得
#     svg_html = svg.get_attribute('outerHTML')
#     print(f"SVG {idx}:")
#     print(svg_html)

# 終了
driver.quit()
