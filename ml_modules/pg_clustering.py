import mysql.connector
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
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

# Fetch PG data
query = "SELECT pg_id, landmark, price, food_type FROM PG_Details"
cursor.execute(query)
pg_data = cursor.fetchall()

# Convert to DataFrame
columns = ["pg_id", "landmark", "price", "food_type"]
df = pd.DataFrame(pg_data, columns=columns)

# Handle missing values
df[['landmark', 'food_type']] = df[['landmark', 'food_type']].fillna('Unknown')
df['price'].fillna(df['price'].mean(), inplace=True)

# Encode categorical features (Landmark & Food Type)
encoder = OneHotEncoder()
encoded_features = encoder.fit_transform(df[['landmark', 'food_type']]).toarray()

# Normalize numerical feature (Price)
scaler = StandardScaler()
df['price_scaled'] = scaler.fit_transform(df[['price']].values.reshape(-1, 1))

# Combine processed data
X = np.hstack((df[['price_scaled']], encoded_features))

# Apply K-Means Clustering
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_predict(X)

# Store cluster assignments back into MySQL
for index, row in df.iterrows():
    cursor.execute("SELECT pg_id FROM PG_Details WHERE pg_id = %s", (int(row['pg_id']),))
    result = cursor.fetchone()
    if result:
        cursor.execute("UPDATE PG_Details SET cluster=%s WHERE pg_id=%s", (int(row['cluster']), int(row['pg_id'])))

conn.commit()

# Close connection
cursor.close()
conn.close()

