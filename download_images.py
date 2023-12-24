import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_images(url, download_dir):
    # URLからHTMLを取得
    response = requests.get(url)
    html = response.text

    # BeautifulSoupを使用してHTMLを解析
    soup = BeautifulSoup(html, "html.parser")

    # 画像を保存するディレクトリを作成
    os.makedirs(download_dir, exist_ok=True)

    # imgタグを取得し、各画像をダウンロードして保存
    img_tags = soup.find_all("img", src=True)
    for img_tag in img_tags:
        img_url = urljoin(url, img_tag["src"])
        img_alt = img_tag.get("alt", "image")
        img_data = requests.get(img_url).content

        # ファイル名をalt属性から生成
        file_name = f"{img_alt}.webp"
        file_path = os.path.join(download_dir, file_name)

        # 画像をローカルに保存
        with open(file_path, "wb") as f:
            f.write(img_data)
            print(f"Image '{img_alt}' saved as '{file_path}'")

if __name__ == "__main__":
    # URLの入力を促すメッセージを表示
    url_input = input("URLを入力してください: ")

    # ダウンロード先ディレクトリの入力を促すメッセージを表示
    download_dir = input("画像を保存するディレクトリを入力してください: ")

    # 画像のダウンロードを実行
    download_images(url_input, download_dir)
