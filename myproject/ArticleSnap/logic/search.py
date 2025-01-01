from selenium import webdriver  # Seleniumライブラリからwebdriverをインポート
from selenium.webdriver.common.by import By  # 要素を特定するためのByクラスをインポート
from selenium.webdriver.chrome.service import Service  # Chromeドライバーのサービスを管理するためのクラス
import time  # スクリプトに遅延を加えるためのtimeモジュール
import os
import json
from pprint import pprint

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

        # ページ読み込みを待機（必要に応じて明示的待機に変更可能）
        time.sleep(2)

        # 動的にメディアと投稿を収集する処理
        media = []
        posts = []

        # タイトル要素を取得
        try:
            element = driver.find_element(By.CSS_SELECTOR, "[id^='post-title-t3']")
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
                    "media": [
                        {
                        },
                    ]
                }

                # 配列に追加
                posts.append(item)
        except Exception as e:
            print("video not found!")
        
        
        
        
        # 整形されたJSONデータを作成
        result = {
            "title": title,
            "source_url": url,
            "media": media,
            "posts": posts
        }

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

if __name__ == "__main__":
    url = r"https://www.reddit.com/r/PokemonUnite/comments/1hon7rh/permanent_lucario_unite_license_and_absol_holowear/"
    result=extract_data_from_html(url, driver_path='./chromedriver.exe')
    pprint(result)



