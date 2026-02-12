from importer.populate import get_file_path, read_csv_safe

# ---- READ CSV ----
df = read_csv_safe(get_file_path("users.csv"))

# get random user
def get_user():
    # get random user row
    row = df.sample(n=1).iloc[0]
    user = {'username': row['username'], 'password': row['password']}
    return user