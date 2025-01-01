#!/bin/zsh

# 使用するPythonバージョン
PYTHON_VERSION="python3.8"

# 仮想環境ディレクトリ
VENV_DIR="venv"

# Pythonスクリプトのファイル名
SCRIPT="transcription.py"

# 仮想環境の作成と依存関係のインストール
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment with $PYTHON_VERSION..."
    $PYTHON_VERSION -m venv "$VENV_DIR"
    echo "Installing dependencies..."
    source "$VENV_DIR/bin/activate" && pip install -r requirements.txt
else
    echo "Virtual environment already exists."
fi

# 仮想環境の確認
source "$VENV_DIR/bin/activate" && pip list

# 仮想環境を有効化してスクリプトを実行
if [ -f "$SCRIPT" ]; then
    echo "Running the script..."
    source "$VENV_DIR/bin/activate" && python "$SCRIPT"
else
    echo "Error: Script file $SCRIPT not found!"
    exit 1
fi

# 仮想環境を削除
echo "Cleaning up virtual environment..."
rm -rf "$VENV_DIR"
echo "Virtual environment removed."
