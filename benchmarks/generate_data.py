import pandas as pd
import numpy as np

def generate_excel(filename, num_rows=100):
    data = {
        'Name': [f'Name_{i}' for i in range(num_rows)],
        'Value': np.random.randint(1, 1000, size=num_rows)
    }
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

if __name__ == "__main__":
    generate_excel('file1.xlsx', 200)
    generate_excel('file2.xlsx', 200)
