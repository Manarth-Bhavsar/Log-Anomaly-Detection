# Log-Anomaly-Detection

Prerequisites:

1> Python 3.6+
2> Libraries: pandas, scikit-learn, matplotlib, numpy, Splunk SDK.

Data Collection and Preprocessing:

1> Sample Data: Sample pre-processed data from the logpai/loghub repository on GitHub.
2> Real-time Data: Automatically export logs from Splunk and feed them into the model for real-time anomaly prediction.

Data Processing:

1> Integrated Splunk to collect Linux System logs.
2> Extracted features including Time stamp, Process ID, Event Template, etc. into columns.
3> Converted processed log data into CSV format for model input.

Project Structure:

1> Script.py: Main Python script containing the entire workflow.
2> syslogs.csv: Sample log data (if applicable).
3> anomalies_output.csv: Output file containing detected anomalies.

Usage:

1> Connect to the Splunk client by providing appropriate credentials to the script.
2> Load the fetched data.
3> Make sure all the dependencies are installed.
4> Run the code as a whole and you will get the output on the screen as well as csv file with anomalies for further investigation.



