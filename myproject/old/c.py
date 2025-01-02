from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def setup_driver():
    """SeleniumのWebDriverをセットアップ"""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # ブラウザを最大化
    options.add_argument("--disable-blink-features=AutomationControlled")  # 自動化制御のバイパス
    driver = webdriver.Chrome(options=options)
    return driver

def automate_prompt_engineering(driver, prompt_text):
    """プロンプトを入力して送信"""
    try:
        # ChatGPTページを開く
        driver.get("https://chat.openai.com/")  # OpenAIのChatGPT URL（ログインが必要）
        time.sleep(5)  # ページのロードを待つ

        # ログインが必要な場合は、ログイン処理を追加
        # TODO: 必要に応じてログインフォームの自動入力を実装

        # プロンプト入力ボックスを特定
        input_box = driver.find_element(By.XPATH, "//textarea")  # ChatGPTの入力ボックス
        input_box.send_keys(prompt_text)

        # Enterキーを押して送信
        input_box.send_keys(Keys.RETURN)
        time.sleep(5)  # 応答を待つ
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    # プロンプトの内容
    prompt = "Can you explain the basics of prompt engineering?"

    # WebDriverのセットアップ
    driver = setup_driver()

    # プロンプトエンジニアリングの自動化
    automate_prompt_engineering(driver, prompt)

    # ドライバを終了
    driver.quit()
