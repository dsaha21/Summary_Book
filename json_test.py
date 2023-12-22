import sqlite3
import json

# Assuming you have a dictionary called 'my_dict'
page_dict ={40: "writers: comfort is not self- esteem; teachers of self-esteem aren't worshipping false gods . they say it's wise to seek companions who are friends of one's self-worth rather than enemies . writers: we run the risk of becoming approval addicts, which is deadly to mental and emotional well-being . authors: if we look to others as a primary source of our self esteem, we're in danger",
            31: 'author: pride is not a vice to be overcome, but a value to be attained . author: a man who was depressed and unhappy was wounded in his self-esteem . he says we may come into this world with inherent differences that may make it easier or harder . writer: if we want to be a better person, we need to be more like him .',
            32: 'there are people who appear to have been raised superbly by the standards indicated above . yet they are insecure, self-doubting adults who do well in school and relationships . an honest commitment to un- derstanding inspires self-trust and that an avoidance of effort has the opposite effect .'}

# Convert the dictionary to a JSON string
json_data = json.dumps(page_dict)

# Connect to the SQLite database
conn = sqlite3.connect('maindata.db')
cursor = conn.cursor()

# Create a table to store the dictionary
cursor.execute("CREATE TABLE IF NOT EXISTS my_table (dict TEXT)")

# Insert the serialized dictionary into the database
cursor.execute("INSERT INTO my_table (dict) VALUES (?)", (json_data,))

cursor.execute("SELECT dict FROM my_table")

res_obj = cursor.fetchone()[0]
finaldic = json.loads(res_obj)
print(finaldic, "==========",type(finaldic))

print("======",finaldic['30'])
# Commit the changes and close the connection
conn.commit()
conn.close()

