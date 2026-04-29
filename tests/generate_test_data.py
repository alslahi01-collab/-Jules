import pandas as pd
import random

def generate_arabic_name():
    first_names = ["محمد", "أحمد", "علي", "حسن", "فاطمة", "زينب", "عائشة", "عمر"]
    last_names = ["محمود", "إبراهيم", "خليل", "سعيد", "عبدالله", "يوسف"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_excel(filename, rows=100):
    data = {
        "Name": [generate_arabic_name() for _ in range(rows)],
        "Age": [random.randint(20, 60) for _ in range(rows)],
        "City": ["القاهرة", "الرياض", "دبي", "عمان"] * (rows // 4 + 1)
    }
    # Fix the slicing issue: slice the list in the dictionary values or use head() on df
    df = pd.DataFrame({k: v[:rows] for k, v in data.items()})
    df.to_excel(filename, index=False)

if __name__ == "__main__":
    generate_excel("test_file1.xlsx", 500)
    generate_excel("test_file2.xlsx", 500)
