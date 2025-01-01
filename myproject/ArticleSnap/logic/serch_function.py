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
        time.sleep(1)

        # div要素を指定して取得 (class名とdata属性を使用)
        div_element = driver.find_element(By.CSS_SELECTOR, "div.mb-sm[data-post-click-location='text-body']")

        # div内のテキストを取得
        div_text = div_element.text

        print(div_text)

    except Exception as e:
        print("Image element not found!")

    finally:
        # WebDriverを終了する
        driver.quit()


# 使用例
if __name__ == "__main__":
    url = r"https://www.reddit.com/r/PokemonUnite/comments/1hpvsec/just_a_quick_reminder_the_wheel_is_a_lie/"
    element_id = "post-title-t3_1hpvsec"
    extracted_text = extract_text_from_html(url, element_id)
    print("Extracted Text:", extracted_text)
