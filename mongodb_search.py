import json

# Read JSONL file
with open('combined_prepared_valid.jsonl', 'r') as f:
    lines = f.readlines()

# Update completion field and write back to file
with open('combined_prepared_valid.jsonl', 'w') as f:
    for line in lines:
        data = json.loads(line)
        data['completion'] = data['completion'] + ' ###'
        f.write(json.dumps(data) + '\n')
