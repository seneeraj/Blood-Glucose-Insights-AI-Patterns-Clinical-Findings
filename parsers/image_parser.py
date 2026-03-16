import pytesseract
from PIL import Image
import pandas as pd
import re
from datetime import datetime

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def parse_image(file):

    image = Image.open(file).convert("L")

    text = pytesseract.image_to_string(image)

    lines = text.split("\n")

    rows = []

    for line in lines:

        # Flexible date detection
        date_match = re.search(r'(\d{1,2})[-\s]?([A-Za-z]{3})[-\s]?(\d{2})', line)

        if not date_match:
            continue

        day, month, year = date_match.groups()

        try:
            date = datetime.strptime(f"{day}-{month}-{year}", "%d-%b-%y")
        except:
            continue

        numbers = re.findall(r"\d+", line)

        numbers = [int(n) for n in numbers if 0 <= int(n) <= 600]

        # Keep last 6 numbers (glucose values)
        if len(numbers) >= 6:
            glucose_values = numbers[-6:]
            rows.append([date] + glucose_values)

    df = pd.DataFrame(rows, columns=["Date","BB","AB","BL","AL","BD","AD"])

    return df