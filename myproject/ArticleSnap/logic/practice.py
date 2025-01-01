from selenium import webdriver  # Seleniumライブラリからwebdriverをインポート
from selenium.webdriver.common.by import By  # 要素を特定するためのByクラスをインポート
import time  # スクリプトに遅延を加えるためのtimeモジュール
import os  # ファイル操作に使用するosモジュール
from selenium.webdriver.chrome.service import Service  # Chromeドライバーのサービスを管理するためのクラス

# スクレイピング対象のURL
# url = 'https://www.reddit.com/r/PokemonUnite/comments/1hon7rh/permanent_lucario_unite_license_and_absol_holowear/'
url = 'https://www.reddit.com/r/PokemonUnite/comments/1hon7rh/permanent_lucario_unite_license_and_absol_holowear/'
# url = 'https://www.reddit.com/r/PokemonUnite/comments/1hpvsec/just_a_quick_reminder_the_wheel_is_a_lie/'
# url = 'https://www.reddit.com/r/PokemonUnite/comments/1hqibwb/we_go_to_hell_together_darkrai/'

# ChromeDriverの場所を指定（同じフォルダにあるchromedriver.exeを使用）
service = Service('./chromedriver.exe')  # './' はスクリプトと同じディレクトリを意味します

# Chromeのオプションを設定
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')  # ブラウザを最大化して開始するオプション
options.add_experimental_option('detach', True)  # スクリプト終了後もブラウザを閉じない設定

# WebDriverのインスタンスを作成（Chromeブラウザを制御）
driver = webdriver.Chrome(options=options)

# tryブロック内で処理を行い、エラー発生時もfinallyブロックでリソースを解放
try:
    # 指定されたURLを開く
    driver.get(url)  # 動的なWebページを読み込む

    # ページが完全に読み込まれるのを待機（必要に応じて調整可能）
    time.sleep(2)  # 5秒間の待機。動的コンテンツが読み込まれるのを待つため

    # 現在のページのHTMLソースコードを取得
    html = driver.page_source

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
    driver.quit()
