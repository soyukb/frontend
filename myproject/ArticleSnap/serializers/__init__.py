import os
import importlib

# 現在のディレクトリを取得
current_dir = os.path.dirname(__file__)

# __all__ を初期化
__all__ = []

# ディレクトリ内のすべての .py ファイルを走査
for filename in os.listdir(current_dir):
    # __init__.py や隠しファイルをスキップ
    if filename.startswith("_") or not filename.endswith(".py"):
        continue

    # ファイル名からモジュール名を取得
    module_name = filename[:-3]  # 拡張子 .py を除去

    # モジュールをインポート
    module = importlib.import_module(f".{module_name}", package=__name__)

    # モジュール内のすべての属性を確認
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)

        # クラスのみを対象にする
        if isinstance(attribute, type):
            globals()[attribute_name] = attribute  # クラスをグローバルに追加
            __all__.append(attribute_name)  # __all__ にクラス名を追加
