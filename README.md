# Installation

To use the scraper, you need to install the web driver for the Microsoft Edge browser and place it in the driver directory with the following name `msedgedriver.exe`.

After downloading and installing the driver, it is advisable to create a virtual environment.

```python
python -m venv env
```

Next, simply install the project's dependencies

```python
pip install -r requirements.txt
```

At the end, run the `main.py` script and check that the scraper is working

```python
python main.py
```