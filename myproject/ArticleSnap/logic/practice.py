from selenium import webdriver  # Seleniumライブラリからwebdriverをインポート
from selenium.webdriver.common.by import By  # 要素を特定するためのByクラスをインポート
import time  # スクリプトに遅延を加えるためのtimeモジュール
import os  # ファイル操作に使用するosモジュール
from selenium.webdriver.chrome.service import Service  # Chromeドライバーのサービスを管理するためのクラス
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

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

def click_join_outline_buttons(driver, wait_time=1):
    """
    Seleniumを使用して、ページ内のすべての`join-outline`属性が付いたボタンをクリックします。

    Args:
        driver (webdriver): Selenium WebDriverオブジェクト
        wait_time (int): ボタンをクリックする間隔（秒）

    Returns:
        int: クリックしたボタンの数
    """
    time.sleep(2)
    
    try:
        # join-outlineアイコンが付いているボタンをすべて取得
        svg_elements = driver.find_elements(By.TAG_NAME, "svg")
        join_outline_svg = [svg for svg in svg_elements if svg.get_attribute("icon-name") == "join-outline"]
        print(f"見つかったボタンの数: {len(join_outline_svg)}")

        # 各ボタンをクリック
        for button in join_outline_svg:
            try:
                # ボタンが表示されるようスクロール
                ActionChains(driver).move_to_element(button).perform()
                button.click()
                print("ボタンをクリックしました")
                time.sleep(wait_time)  # ボタンを押す間隔
            except Exception as e:
                print(f"ボタンをクリック中にエラーが発生しました: {e}")
        return len(join_outline_svg)
    except Exception as e:
        print(f"処理中にエラーが発生しました: {e}")
        return 0


# スクレイピング対象のURL
# url = 'https://www.reddit.com/r/PokemonUnite/comments/1hon7rh/permanent_lucario_unite_license_and_absol_holowear/'
url = 'https://chatgpt.com/'
# url = 'https://www.reddit.com/r/PokemonUnite/comments/1hpvsec/just_a_quick_reminder_the_wheel_is_a_lie/'
# url = 'https://www.reddit.com/r/PokemonUnite/comments/1hqibwb/we_go_to_hell_together_darkrai/'

# ChromeDriverの場所を指定（同じフォルダにあるchromedriver.exeを使用）
service = Service('./chromedriver.exe')  # './' はスクリプトと同じディレクトリを意味します

# Chromeのオプションを設定
options = webdriver.ChromeOptions()
options.add_argument(r'--user-data-dir=C:\Users\soyuk\AppData\Local\Google\Chrome\User Data\Profile 1')
# 使用するプロファイル(ユーザー)を指定
options.add_argument('--profile-directory=Profile 1')
options.add_argument('--start-maximized')  # ブラウザを最大化して開始するオプション
options.add_experimental_option('detach', True)  # スクリプト終了後もブラウザを閉じない設定

# WebDriverのインスタンスを作成（Chromeブラウザを制御）
driver = webdriver.Chrome(options=options)

# tryブロック内で処理を行い、エラー発生時もfinallyブロックでリソースを解放
try:
    # 指定されたURLを開く
    driver.get(url)  # 動的なWebページを読み込む
    # scroll_to_bottom(driver)

    # 現在のページのHTMLソースコードを取得
    html = driver.page_source
    # click_join_outline_buttons(driver, wait_time=1)
    # html = driver.page_source

    # HTMLを保存するための準備
    # スクリプトが保存されているディレクトリを取得
    current_folder = os.path.dirname(__file__)
    # 保存するHTMLファイルのパスを作成
    output_file = os.path.join(current_folder, "output.html")

    # HTMLソースコードをファイルに書き込み
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(html)

    # 保存が完了したことを通知
    print(f"HTMLが '{output_file}' に保存されました。")

finally:
    # ブラウザを閉じてリソースを解放
    # driver.quit()
    print("a")
    
