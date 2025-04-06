import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
import mysql.connector

# Load env variables
load_dotenv()

# Connect to MySQL
conn = mysql.connector.connect(
    host=os.getenv('host'),
    user=os.getenv('user'),
    password=os.getenv('password'),
    database=os.getenv('database'),
)
cursor = conn.cursor(dictionary=True)

# Fetch student data
cursor.execute("SELECT * FROM students")
students = cursor.fetchall()
df = pd.DataFrame(students)

# Encode categorical columns
for column in ['food_type', 'room_type', 'amenities', 'year', 'branch']:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column].astype(str))

# Apply K-Means clustering
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_predict(df[['food_type', 'room_type', 'amenities', 'year', 'branch']])

# Update database with cluster labels
for _, row in df.iterrows():
    cursor.execute("UPDATE students SET cluster = %s WHERE email = %s", (int(row['cluster']), row['email']))

conn.commit()
cursor.close()
conn.close()
print("✅ Clusters updated successfully!")
