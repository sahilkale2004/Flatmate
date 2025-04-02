import mysql.connector
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.cluster import KMeans
import numpy as np

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="KMEANS"
)
cursor = conn.cursor()

# Fetch student data
query = "SELECT student_id, department, year, food_type, room_type FROM Student_Preferences"
cursor.execute(query)
student_data = cursor.fetchall()

# Convert to DataFrame
columns = ["student_id", "department", "year", "food_type", "room_type"]
df = pd.DataFrame(student_data, columns=columns)

# One-Hot Encode categorical variables
encoder = OneHotEncoder()
encoded_features = encoder.fit_transform(df[['department', 'food_type', 'room_type']]).toarray()

# Normalize numerical features (year)
scaler = StandardScaler()
df['year_scaled'] = scaler.fit_transform(df[['year']])

# Combine processed features
X = np.hstack((df[['year_scaled']], encoded_features))

# Apply K-Means Clustering
kmeans = KMeans(n_clusters=3, random_state=42)
df['cluster'] = kmeans.fit_predict(X)

# Store cluster assignments in MySQL
for index, row in df.iterrows():
    cursor.execute("UPDATE Student_Preferences SET cluster=%s WHERE student_id=%s", (int(row['cluster']), int(row['student_id'])))
conn.commit()

# Close connection
cursor.close()
conn.close()
