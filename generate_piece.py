import os
import random
import datetime
import pytz
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

NUM_PIECES = 248

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

timezone = pytz.timezone("Pacific/Kiritimati")

cursor = conn.cursor()
cursor.execute("SELECT piece from recents")
recents = [row[0] for row in cursor.fetchall()]

universe = [i for i in range(1, NUM_PIECES + 1)]
sample_space = [piece for piece in universe if piece not in recents]
piece = random.choice(sample_space)

now = datetime.datetime.now(timezone)
tmr = now + datetime.timedelta(days=1)
date = int(tmr.strftime("%Y%m%d"))

query = "INSERT INTO recents (date, piece) VALUES (%s, %s)"
values = (date, piece)
cursor.execute(query, values)
conn.commit()

cursor.close()
conn.close()