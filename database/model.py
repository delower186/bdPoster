import datetime

from database.db import select, update

# get total number of unposted titles by forum
def get_unposted_title_number(forum):
    return len(select("articles", "id", "WHERE forum=%s AND posted=%s", (forum,0)))

# get all data of number of unposted titles by forum
def get_unposted_title_all(forum, limit):
    return select("articles", "*", "WHERE forum=%s AND posted=%s", (forum,0,limit), "LIMIT %s")

# get all data of a single unposted title by forum & title_id
def get_unposted_title(title_id):
    return select("articles", "*", "WHERE id=%s AND posted=%s", (title_id,0))

# update title and set posted = 1 & updated_at = today
def update_title(title_id):
    update("articles",  "posted = %s, updated_at=%s","WHERE id = %s", (1, datetime.datetime.now(), title_id))