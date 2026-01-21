import datetime
import pandas as pd
from pathlib import Path
from db.db import get_db_connection

# ---- CSV PATH ----
BASE_DIR = Path(__file__).resolve().parent.parent
csv_path = BASE_DIR / "csvs" / "500_unique_web_android_titles_no_number.csv"

# ---- READ CSV ----
df = pd.read_csv(csv_path)

# ---- DB CONNECTION (ONLY ONCE) ----
conn = get_db_connection()
cursor = conn.cursor(buffered=True)

BATCH_SIZE = 500

# ---- CURRENT DATE ----
now = datetime.date.today().isoformat()

# ---- PREPARE DATA ----
data = [
    (
        title.strip(),                         # title
        "development",                         # forum
        "//a[normalize-space()='Development']",# xpath
        now                                   # created_at
    )
    for title in df["title"]
    if pd.notna(title)
]

# ---- INSERT IN BATCHES ----
for i in range(0, len(data), BATCH_SIZE):
    batch = data[i:i + BATCH_SIZE]
    cursor.executemany(
        """
        INSERT IGNORE INTO articles
        (title, forum, xpath, created_at)
        VALUES (%s, %s, %s, %s)
        """,
        batch
    )

# ---- COMMIT & CLOSE ----
conn.commit()
cursor.close()
conn.close()

print(f"✅ Inserted {len(data)} titles successfully")