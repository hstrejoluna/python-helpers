import mysql.connector
import json

# Connect to the database
conn = mysql.connector.connect(
    host="159.65.167.117",
    user="webdev",
    password="Nma%IAkny%Zy2sho",
    database="foa2020"
)



# Retrieve data
cur = conn.cursor()
cur.execute("SELECT * FROM changing_lives")
rows = cur.fetchall()

# Format data as JSON
data = []
for row in rows:
    data.append({
        "id": row[0],
        "name": row[1],
        "age": row[2]
    })
json_data = json.dumps(data)

# Output the JSON
print(json_data)