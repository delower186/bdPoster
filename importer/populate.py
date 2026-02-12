import csv
import datetime

import pandas as pd
from pathlib import Path
from database.db import get_db_connection
from database.model import get_unposted_title_number
from prompts import title_prompt
from generator import generate_titles


def get_file_path(file):
    # ---- CSV PATH ----
    BASE_DIR = Path(__file__).resolve().parent.parent
    file_path = BASE_DIR / "csvs" / file
    return file_path

# To import from file
csv_path = get_file_path("titles.csv")

# csv column title
column_name_on_the_csv_file = "title"

# To generate from AI model
category_descriptions = [
    {"marketing":"marketing (Social Media Marketing, Digital Marketing, SEO etc.)"},
    {"development":"development (Web or Android or Desktop Application)"},
    {"design":"design (Graphics, Web etc)"},
    {"marketplace":"marketplaces (Upwork, Fiverr, Freelancer etc)"},
    {"philosophy of life":"philosophy of life (Inspirational stories, biographies of famous people, positive behaviors, etc.)"},
    {"known-unknown":"Known-unknown (Detailed information on general knowledge)"}
]
number_of_titles = 1000


# For database
forums = [
    "marketing",
    "development",
    "design",
    "marketplace",
    "philosophy of life",
    "Known-unknown"
]
xpaths = [
    "//a[normalize-space()='Marketing']",
    "//a[normalize-space()='Development']",
    "//a[normalize-space()='Design']",
    "//a[normalize-space()='Marketplace']",
    "//a[normalize-space()='Philosophy of life']",
    "//a[normalize-space()='Known-unknown']"
]

# ---- DB CONNECTION (ONLY ONCE) ----
conn = get_db_connection()
cursor = conn.cursor(buffered=True)

BATCH_SIZE = 500

# ---- CURRENT DATE ----
now = datetime.date.today().isoformat()

def read_csv_safe(path):
    try:
        return pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return pd.read_csv(path, encoding="cp1252")
        except UnicodeDecodeError:
            return pd.read_csv(path, encoding="latin-1")


def import_from_file(forum_name, forum_xpath):

    # ---- READ CSV ----
    df = read_csv_safe(csv_path)

    # ---- PREPARE DATA ----
    data = [
        (
            title.strip(),                         # title
            forum_name,                            # forum
            forum_xpath,                           # xpath
            now                                    # created_at
        )
        for title in df[column_name_on_the_csv_file]
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
    print(f"✅ Inserted {len(data)} titles successfully")

    # ---- COMMIT & CLOSE ----
    conn.commit()
    # cursor.close()
    # conn.close()

def generate_titles_to_csv(forum_name, forum_xpath, category_description):

    all_titles = set()
    BATCH_SIZE_FOR_7B_MODEL = 25  # sweet spot for 7B models

    # Create file with header if it doesn't exist
    #if not os.path.exists(csv_path):
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["title"])  # Only one column


    while len(all_titles) < number_of_titles:

        new_titles = generate_titles(title_prompt, category_description, BATCH_SIZE_FOR_7B_MODEL, all_titles)

        print(f"New titles generated: {len(new_titles)}")
        print(f"Total unique titles so far: {len(all_titles)}")

        if not new_titles:
            print("No new titles generated. Retrying...")
            continue

        # Append ONLY new titles
        with open(csv_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            for title in new_titles:
                writer.writerow([title.strip()])  # Single column only

    else:
        import_from_file(forum_name, forum_xpath)


def get_titles(forum):

    # print(f"Getting titles for {forum} and index {forums.index(forum)}")

    category_description = category_descriptions[forums.index(forum)]

    forum_name = forums[forums.index(forum)]
    forum_xpath = xpaths[forums.index(forum)]

    generate_titles_to_csv(forum_name, forum_xpath, category_description)

# print(get_unposted_title_number("marketing"))
