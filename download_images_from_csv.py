import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

# CSVファイルのパス
csv_file_path = "get_img_list.csv"

# CSVファイルを読み込み
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    
    # 2行目から処理開始
    # next(reader, None)

    for row in reader:
        # URLとディレクトリ名を取得
        url = row["URL"]
        directory_name = row["ディレクトリ名"]
        print(url)
        print(directory_name)
        # URLからHTMLを取得
        response = requests.get(url)
        html = response.text

        # BeautifulSoupを使用してHTMLを解析
        soup = BeautifulSoup(html, "html.parser")

        # 画像を保存するディレクトリを作成
        os.makedirs(directory_name, exist_ok=True)

        # imgタグを取得し、各画像をダウンロードして保存
        img_tags = soup.find_all("img", src=True)
        for img_tag in img_tags:
            img_url = urljoin(url, img_tag["src"])
            img_alt = img_tag.get("alt", "image")
            img_data = requests.get(img_url).content

            # ファイル名をalt属性から生成
            file_name = f"{img_alt}.webp"
            file_path = os.path.join(directory_name, file_name)

            # 画像をローカルに保存
            with open(file_path, "wb") as f:
                f.write(img_data)
                print(f"Image '{img_alt}' saved as '{file_path}'")
