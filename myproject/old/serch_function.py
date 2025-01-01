from selenium import webdriver  # Seleniumライブラリからwebdriverをインポート
from selenium.webdriver.common.by import By  # 要素を特定するためのByクラスをインポート
from selenium.webdriver.chrome.service import Service  # Chromeドライバーのサービスを管理するためのクラス
import time  # スクリプトに遅延を加えるためのtimeモジュール
import os
import json
from selenium.common.exceptions import NoSuchElementException

def extract_text_from_html(url, element_id, driver_path='./chromedriver.exe'):
    """
    指定されたHTMLファイルから要素のテキストを抽出する関数。

    Args:
        url (str): HTMLファイルのパス。
        element_id (str): 抽出したい要素のID。
        driver_path (str): ChromeDriverのパス（デフォルトは'./chromedriver.exe'）。

    Returns:
        str: 抽出したテキスト。エラーの場合はエラーメッセージ。
    """
    # スクリプトのディレクトリを取得
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # スクリプトのディレクトリにある "chromedriver.exe" を指定
    file_path = os.path.join(script_dir, "chromedriver.exe")
    
    # ChromeDriverのサービスを設定
    service = Service(file_path)

    # Chromeのオプションを設定
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')  # ブラウザを最大化して開始するオプション
    options.add_experimental_option('detach', True)  # スクリプト終了後もブラウザを閉じない設定

    # WebDriverのインスタンスを作成
    driver = webdriver.Chrome(service=service, options=options)

    data = {}
    try:
        # 指定したHTMLファイルを開く
        driver.get(url)

        # ページが完全に読み込まれるまで少し待つ
        scroll_to_bottom(driver)

        # shreddit-commentタグをすべて取得
        comment_elements = driver.find_elements(By.TAG_NAME, "shreddit-comment")

        # 各shreddit-commentタグを処理
        for comment_element in comment_elements:
            # 必要な属性を取得
            thingid = comment_element.get_attribute("thingid")
            depth = comment_element.get_attribute("depth")
            parentid = comment_element.get_attribute("parentid")

            # <p>タグ内のテキストを取得
            p_text = comment_element.find_element(By.TAG_NAME, "p").text
            print(f"p_text: {p_text}")

            # <time>タグのdatetime属性を取得
            time_element = comment_element.find_element(By.TAG_NAME, "time")
            datetime = time_element.get_attribute("datetime")
            print(f"datetime: {datetime}")
            
            try:
                # 画像URLを取得 jpegを探す
                img_element = comment_element.find_element(By.TAG_NAME, "img")
                img_url = img_element.get_attribute("src")
                if img_url:
                    media.append({"media_type": "image", "media_url": img_url})
            except Exception as e:
                print("image not found!")
                
            try:
                # 画像URLを取得 jpegを探す
                img_elements = driver.find_elements(By.CSS_SELECTOR, "li img.media-lightbox-img")
                img_urls = [img.get_attribute("src") for img in img_elements]
                if img_urls:
                    for img_url in img_urls:
                        media.append({"media_type": "image", "media_url": img_url})
            except Exception as e:
                print("image not found!")

        # 結果を表示
        print(f"thingid: {thingid}")
        print(f"depth: {depth}")
        print(f"parentid: {parentid}")
        print(f"p_text: {p_text}")
        print(f"p_text: {datetime}")

    except Exception as e:
        print(e)

    finally:
        # WebDriverを終了する
        driver.quit()

def scroll_to_bottom(driver, pause_time=1):
    """
    Scrolls to the bottom of the page using Selenium.

    Parameters:
        driver (webdriver): The Selenium WebDriver instance.
        pause_time (int or float): Time to pause after each scroll step (in seconds).
    """
    # 現在のスクロール高さを取得
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # ページの一番下までスクロール
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # ページが読み込まれるのを待つ
        time.sleep(pause_time)
        time.sleep(2)

        # 新しいスクロール高さを取得
        new_height = driver.execute_script("return document.body.scrollHeight")

        # 一番下に到達したかを確認
        if new_height == last_height:
            view_more_button = driver.find_element(By.XPATH, "//span[contains(text(), 'View more comments')]")
            view_more_button.click()
            break

        last_height = new_height
    
    # ページの一番上にスクロール
    driver.execute_script("window.scrollTo(0, 0);")


# 使用例
if __name__ == "__main__":
    url = r"https://www.reddit.com/r/PokemonUnite/comments/1hqp58l/the_results_are_in/"
    element_id = "post-title-t3_1hpvsec"
    extracted_text = extract_text_from_html(url, element_id)
    print("Extracted Text:", extracted_text)
