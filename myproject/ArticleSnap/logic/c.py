from googletrans import Translator

translator = Translator()
result = translator.translate('Hello, world!', src='en', dest='ja')
print(result.text)  # こんにちは、世界！
