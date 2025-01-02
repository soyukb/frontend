from selenium import webdriver  # Seleniumライブラリからwebdriverをインポート
from selenium.webdriver.common.by import By  # 要素を特定するためのByクラスをインポート
from selenium.webdriver.chrome.service import Service  # Chromeドライバーのサービスを管理するためのクラス
import time  # スクリプトに遅延を加えるためのtimeモジュール
import os
import json
from pprint import pprint
from selenium.webdriver.common.action_chains import ActionChains
from googletrans import Translator


def extract_data_from_html(url, driver_path='./chromedriver.exe'):
    """
    指定されたウェブページからデータを抽出し、整形されたJSON形式で返す関数。

    Args:
        url (str): 対象ウェブページのURL。
        driver_path (str): ChromeDriverの実行ファイルパス（デフォルトは'./chromedriver.exe'）。

    Returns:
        dict: 整形されたJSON形式のデータ。
    """
    
    # スクリプトのディレクトリを取得
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # スクリプトのディレクトリにある "chromedriver.exe" を指定
    driver_path = os.path.join(script_dir, "chromedriver.exe")
    
    # ChromeDriverのサービスオブジェクトを作成
    service = Service(driver_path)

    # Chromeのブラウザオプションを設定
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')  # ブラウザを起動時に最大化する設定
    options.add_experimental_option('detach', True)  # スクリプト終了後もブラウザを閉じないオプション

    # WebDriverのインスタンスを作成
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # 指定されたURLを開く
        driver.get(url)
        try:
            scroll_to_bottom(driver)
            click_join_outline_buttons(driver, wait_time=1)
        except Exception as e:
            print("title not found!")
            
        # 動的にメディアと投稿を収集する処理
        media = []
        posts = []

        # タイトル要素を取得
        try:
            element = driver.find_element(By.CSS_SELECTOR, "[id^='post-title-t3']")
            if element.text:
                title = element.text
        except Exception as e:
            print("title not found!")
        
        try:
            # 画像URLを取得 jpegを探す
            img_element = driver.find_element(By.CSS_SELECTOR, ".zoomable-img-wrapper img")
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
                
        try:
            # 動画URLを取得
            video_url = get_video_url_from_loaded_page(driver)
            if video_url:
                media.append({"media_type": "video", "media_url": video_url})
        except Exception as e:
            print("video not found!")
        
        # 投稿要素を取得 (例: divタグなど)
        # div要素を指定して取得 (class名とdata属性を使用)
        try:
            div_element = driver.find_element(By.CSS_SELECTOR, "div.mb-sm[data-post-click-location='text-body']")
            # div内のテキストを取得
            div_text = div_element.text
            if(div_text):
                # 辞書を作成して追加
                item = {
                    "content": div_text,
                    # "media": [
                    #     {
                    #     },
                    # ]
                }

                # 配列に追加
                posts.append(item)
        except Exception as e:
            print("video not found!")
        
        # shreddit-commentタグをすべて取得
        comment_elements = driver.find_elements(By.TAG_NAME, "shreddit-comment")

        # 各shreddit-commentタグを処理
        for comment_element in comment_elements:
            item = {
                # "content": "This is a sample content string.",
                # "media": [
                #     {
                #     "media_type": "image",
                #     "media_url": "https://example.com/sample-image.jpg"
                #     }
                # ],
                # "thingid": "abc123",
                # "depth": 100,
                # "parentid": "parent456",
                # "created_at": "2025-01-01T18:30:40.782Z",
                # "likes": 1500
                }
            # 必要な属性を取得
            thingid = comment_element.get_attribute("thingid")
            depth = comment_element.get_attribute("depth")
            parentid = comment_element.get_attribute("parentid")
            likes = comment_element.get_attribute("score")
            try:
                p_text = comment_element.find_element(By.TAG_NAME, "p").text
            except Exception as e:
                print("text not found!")
                continue
            if not p_text:
                continue
            item["content"]=p_text
            item["depth"]=depth
            if parentid:
                item["parentid"]=parentid
            item["thingid"]=thingid
            item["likes"]=likes
            
            # <time>タグのdatetime属性を取得
            time_element = comment_element.find_element(By.TAG_NAME, "time")
            datetime = time_element.get_attribute("datetime")
            
            item["created_at"]=datetime
            
            try:
                # 画像URLを取得 
                img_elements = comment_element.find_elements(By.TAG_NAME, "img")
                for img_element in img_elements:
                    img_url = img_element.get_attribute("src")
                    if img_url:
                        posts["media"].append({"media_type": "image", "media_url": img_url})
            except Exception as e:
                print("image not found!")
                
            try:
                # 画像URLを取得 
                video_elements = comment_element.find_elements(By.TAG_NAME, "video")
                for video_element in video_elements:
                    video_url = video_element.get_attribute("src")
                    if video_url:
                        posts["media"].append({"media_type": "video", "media_url": video_url})
            except Exception as e:
                print("video not found!")
            
            posts.append(item)
        
        
        # 整形されたJSONデータを作成
        result = {
            "title": title,
            "source_url": url,
            "media": media,
            "posts": posts
        }
        
        # translator = Translator()
        # result["title_translated"] = translator.translate(result["title"], src="en", dest="ja").text
        # for post in result["posts"]:
        #     post["content_translated"] = translator.translate(post["content"], src="en", dest="ja").text

        return result

    except Exception as e:
        # エラー発生時にエラーメッセージを返す
        return {"error": str(e)}

    finally:
        # WebDriverを終了してリソースを解放
        driver.quit()

def get_video_url_from_loaded_page(driver, resolution_width=1280):
    """
    すでにページが読み込まれている状態のWebDriverから特定の解像度の動画URLを取得します。

    Args:
        driver (webdriver): すでにページが読み込まれている状態のSelenium WebDriver。
        resolution_width (int): 取得したい動画の横幅（デフォルトは1280pxで720p）。

    Returns:
        str: 見つかった動画のURL。見つからなければNoneを返します。
    """
    try:
        # <shreddit-player-2>タグを探す
        player_element = driver.find_element(By.TAG_NAME, "shreddit-player-2")
        
        # "packaged-media-json"属性を取得
        packaged_media_json = player_element.get_attribute("packaged-media-json")
        
        # JSONデータをパース
        media_data = json.loads(packaged_media_json)
        
        # 指定解像度の動画URLを取得
        playback_mp4s = media_data.get("playbackMp4s", {}).get("permutations", [])
        for video in playback_mp4s:
            source = video.get("source", {})
            if source.get("dimensions", {}).get("width") == resolution_width:
                return source.get("url")

    except Exception as e:
        print(f"video not found!")

    return None

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

        # 新しいスクロール高さを取得
        new_height = driver.execute_script("return document.body.scrollHeight")

        # 一番下に到達したかを確認
        if new_height == last_height:
            try:
                view_more_button = driver.find_element(By.XPATH, "//span[contains(text(), 'View more comments')]")
                view_more_button.click()
            except Exception as e:
                print(f"Buton not found!")
            break

        last_height = new_height
        
    # ページの一番上にスクロール
    driver.execute_script("window.scrollTo(0, 0);")

def click_join_outline_buttons(driver, wait_time=1.5):
    """
    Seleniumを使用して、ページ内のすべての`join-outline`属性が付いたボタンをクリックします。

    Args:
        driver (webdriver): Selenium WebDriverオブジェクト
        wait_time (int): ボタンをクリックする間隔（秒）

    Returns:
        int: クリックしたボタンの数
    """
    time.sleep(1)
    
    try:
        # join-outlineアイコンが付いているボタンをすべて取得
        for i in range(3):  # 0から2まで繰り返す
            svg_elements = driver.find_elements(By.TAG_NAME, "svg")
            join_outline_svg = [svg for svg in svg_elements if svg.get_attribute("icon-name") == "join-outline"]
            print(f"見つかったボタンの数: {len(join_outline_svg)}")
            time.sleep(3)
            # 各ボタンをクリック
            for button in join_outline_svg:
                try:
                    # ボタンが表示されるようスクロール
                    ActionChains(driver).move_to_element(button).perform()
                    button.click()
                    print("ボタンをクリックしました")
                    time.sleep(wait_time)  # ボタンを押す間隔
                except Exception as e:
                    print(f"ボタンをクリック中にエラーが発生しました")
        return len(join_outline_svg)
    except Exception as e:
        print(f"処理中にエラーが発生しました")
        return 0

if __name__ == "__main__":
    url = r"https://www.reddit.com/r/PokemonUnite/comments/1hqpbt8/when_you_steal_rayquaza_oc/"
    result=extract_data_from_html(url, driver_path='./chromedriver.exe')
    pprint(result)



