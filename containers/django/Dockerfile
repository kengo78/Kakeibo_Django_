# Pythonのイメージを指定
FROM python:3.9
# PYTHONDONTWRITEBYTECODEとPYTHONUNBUFFEREDはオプション
# pycファイル(および__pycache__)の生成を行わないようにする
ENV PYTHONDONTWRITEBYTECODE=1
# 標準出力・標準エラーのストリームのバッファリングを行わない
ENV PYTHONUNBUFFERED=1
# コンテナのワークディレクトリを/codeに指定
WORKDIR /code
# ローカルのrequirements.txtをコンテナの/codeフォルダ直下に置く
COPY requirements.txt /code/
# コンテナ内でpip install -r requirements.txtを実行
RUN pip install -r requirements.txt
# ソースコードをコンテナにコピー
COPY . /code/