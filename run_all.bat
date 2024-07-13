@echo off
echo Creating and activating virtual environment...
python -m venv .venv
call .venv\Scripts\activate

echo Installing dependencies...
pip install -U pip
pip install -r requirements.txt

echo Running scripts...
python modeling\config.py
python modeling\dataset.py
python modeling\sanity_checks.py
python modeling\features.py
python modeling\train.py
python modeling\predict.py
python modeling\database.py

echo Cleaning up...
del /s /q .\modeling\*.pyc
del /s /q .\modeling\__pycache__

echo All scripts executed in order.
pause
