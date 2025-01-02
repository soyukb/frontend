from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ChromeDriverのパス
chrome_driver_path = "path/to/chromedriver"  # ChromeDriverのパスに置き換えてください

# ブラウザを立ち上げる
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

try:
    # URLを開く
    driver.get("https://chatgpt.com/")

    # ログインページへの遷移が必要な場合
    login_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Login')]"))
    )
    login_button.click()

    # ユーザー名とパスワードの入力
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))  # フォームの`name`属性に合わせて変更
    )
    password_field = driver.find_element(By.NAME, "password")  # フォームの`name`属性に合わせて変更

    username = "your_username"  # ここにログインIDを入力
    password = "your_password"  # ここにパスワードを入力

    username_field.send_keys(username)
    password_field.send_keys(password)

    # フォーム送信
    password_field.send_keys(Keys.RETURN)

    # ログイン後のページを待つ
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Welcome')]"))  # 適宜修正
    )

    print("ログイン成功")
finally:
    # ブラウザを閉じる
    driver.quit()
