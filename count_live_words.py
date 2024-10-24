import json
import pandas as pd
import os

# Specify the path to the JSON file
json_file_path = "recognized_texts.json"

# Load the JSON data from the file
with open(json_file_path, "r", encoding="utf-8") as file:
    json_data = json.load(file)

# Initialize a list to store counts
results = []

# Words to search for
words_to_count = ["água", "esgoto"]

# Process each entry in the JSON data
for entry in json_data:
    timestamp = entry["timestamp"]
    count_dict = {word: 0 for word in words_to_count}  # Initialize counts

    # Count occurrences of each word in recognized texts
    for text in entry["recognized_texts"]:
        for word in words_to_count:
            count_dict[word] += text.lower().count(word)  # Count occurrences (case insensitive)

    # Append results to the list
    results.append({
        "timestamp": timestamp,
        **count_dict
    })

# Create a DataFrame from the results
df = pd.DataFrame(results)

# Specify the output Excel file
output_file = "output_live_counts.xlsx"

# Write DataFrame to an Excel file
df.to_excel(output_file, index=False)

print(f"Counts saved to {output_file}")
