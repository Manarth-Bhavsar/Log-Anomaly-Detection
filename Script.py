import splunklib.client as client
import csv


# Connect to Splunk
service = client.connect(host='192.168.1.187', port='8089', username='admin', password='password')

# Define search query
search_query = 'source="/var/log/syslog" host="Mylogs" sourcetype="syslog" | search *'

# Run search
job = service.jobs.create(search_query)

# Wait for search to finish
while True:
    while not job.is_ready():
        pass
    if job['isDone'] == '1':
        break

# Get results
results = job.results()

# Process results and save to CSV
with open('output.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Month', 'Date', 'Time', 'Level', 'Component', 'PID', 'Content', 'EventId', 'EventTemplate'])  # Write header row
    for result in results:
        # Process result and extract fields as needed
        csvwriter.writerow([
            result['Month'],
            result['Date'],
            result['Time'],
            result['Level'],
            result['Component'],
            result['PID'],
            result['Content'],
            result['EventId'],
            result['EventTemplate']
        ])

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder, OneHotEncoder


# Read log data into a pandas DataFrame (Path to your csv file)
logs = pd.read_csv('/content/Linux_2k.log_structured.csv', delimiter=',')

print(logs.columns)

# Encode categorical variables using one-hot encoding

categorical_columns = ['Month', 'Date', 'Time', 'Level', 'Component', 'PID', 'Content', 'EventId', 'EventTemplate']

# Perform one-hot encoding on categorical columns
onehot_encoder = OneHotEncoder(sparse_output=False)
encoded_columns = pd.DataFrame(onehot_encoder.fit_transform(logs[categorical_columns]))
encoded_columns.columns = onehot_encoder.get_feature_names_out(categorical_columns)


# Concatenate encoded columns with original DataFrame
logs_encoded = pd.concat([logs.drop(columns=categorical_columns), encoded_columns], axis=1)

# print("Encoded Columns:")
# print(encoded_columns)

# For ease, let's use all columns as features except 'LineId'

# Training the Isolation Forest model
isolation_forest = IsolationForest(contamination=0.05)  # random_state=42
isolation_forest.fit(logs_encoded)

anomalies = isolation_forest.predict(logs_encoded)
anomaly_scores = isolation_forest.decision_function(logs_encoded)

# Adding anomaly scores to DataFrame
logs_encoded['anomaly'] = anomalies
logs_encoded['anomaly_score'] = anomaly_scores

# Filtering anomalies
anomalies_df = logs_encoded[logs_encoded['anomaly'] == -1]

output_file = 'anomalies_output.csv'
anomalies_df.to_csv(output_file, index=False)

event_template_columns = [col for col in logs_encoded.columns if col.startswith('EventTemplate_')]

# Creating readable output
event_template_mapping = {col: col.split('_', 1)[1] for col in event_template_columns}

for idx, anomaly in enumerate(anomalies):
    if anomaly == -1:
        line_id = logs_encoded.iloc[idx]['LineId']
        event_templates = [event_template_mapping[col] for col, value in zip(event_template_columns, logs_encoded.iloc[idx][event_template_columns]) if value == 1]
        event_template_str = ", ".join(event_templates)
        alert_message = f"Anomaly detected at LineId {line_id}, Event Templates: {event_template_str}"
        print(alert_message)

total_anomalies_df = len(logs_encoded[logs_encoded['anomaly'] == -1])
print("Total number of anomalies:", total_anomalies_df)

# Downloading the file to local system
files.download('anomalies_output.csv')
print("Downloaded anomalies_output.csv to your local system")