import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
import mysql.connector

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="FLATMATES"
)
cursor = conn.cursor()

cursor.execute("""
    SELECT email, food_type, room_type, amenities, pricing_value, landmark 
    FROM students 
    WHERE food_type IS NOT NULL AND room_type IS NOT NULL 
    AND amenities IS NOT NULL AND pricing_value IS NOT NULL AND landmark IS NOT NULL
""")
students_data = cursor.fetchall()
student_df = pd.DataFrame(students_data, columns=['email', 'food_type', 'room_type', 'amenities', 'pricing_value', 'landmark'])

encoder = LabelEncoder()
student_encoded = student_df.drop(columns=['email']).apply(lambda col: encoder.fit_transform(col))
kmeans_students = KMeans(n_clusters=4, random_state=42)
student_df['cluster'] = kmeans_students.fit_predict(student_encoded)
for _, row in student_df.iterrows():
    cursor.execute("UPDATE students SET cluster = %s WHERE email = %s", (int(row['cluster']), row['email']))

# function to encode and cluster data
def encode_and_cluster(df, columns, n_clusters=4):
    data = df[columns].copy()
    for col in data.columns:
        data[col] = LabelEncoder().fit_transform(data[col])
    km = KMeans(n_clusters=n_clusters, random_state=42)
    df['cluster'] = km.fit_predict(data)
    return df

# --- Food Services ---
cursor.execute("""
    SELECT email, food_type 
    FROM services 
    WHERE service = 'Food' AND food_type IS NOT NULL
""")
food_data = cursor.fetchall()
food_df = pd.DataFrame(food_data, columns=['email', 'food_type'])
if not food_df.empty:
    food_df = encode_and_cluster(food_df, ['food_type'])
    for _, row in food_df.iterrows():
        cursor.execute("UPDATE services SET cluster = %s WHERE email = %s", (int(row['cluster']), row['email']))

# --- Laundry Services ---
cursor.execute("""
    SELECT email, laundry_service 
    FROM services 
    WHERE service = 'Laundry' AND laundry_service IS NOT NULL
""")
laundry_data = cursor.fetchall()
laundry_df = pd.DataFrame(laundry_data, columns=['email', 'laundry_service'])

if not laundry_df.empty:
    laundry_df = encode_and_cluster(laundry_df, ['laundry_service'])
    for _, row in laundry_df.iterrows():
        cursor.execute("UPDATE services SET cluster = %s WHERE email = %s", (int(row['cluster']), row['email']))

# --- Broker Services ---
cursor.execute("""
    SELECT email, room_type, amenities, pricing_value, landmark 
    FROM services 
    WHERE service = 'Broker' AND room_type IS NOT NULL AND amenities IS NOT NULL 
    AND pricing_value IS NOT NULL AND landmark IS NOT NULL
""")
broker_data = cursor.fetchall()
broker_df = pd.DataFrame(broker_data, columns=['email', 'room_type', 'amenities', 'pricing_value', 'landmark'])

if not broker_df.empty:
    broker_df = encode_and_cluster(broker_df, ['room_type', 'amenities', 'pricing_value', 'landmark'])
    for _, row in broker_df.iterrows():
        cursor.execute("UPDATE services SET cluster = %s WHERE email = %s", (int(row['cluster']), row['email']))

conn.commit()
cursor.close()
conn.close()

print("Clusters assigned successfully to students and each type of service provider.")
