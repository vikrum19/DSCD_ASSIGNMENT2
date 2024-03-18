import json
import os

class Storage:
    def __init__(self, node_id):
        self.logs_dir = f'logs_node_{node_id}'
        self.log_file = os.path.join(self.logs_dir, 'logs.txt')
        self.metadata_file = os.path.join(self.logs_dir, 'metadata.txt')
        os.makedirs(self.logs_dir, exist_ok=True)
    
    def append_to_log(self, entry):
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    
    def read_log(self):
        if not os.path.exists(self.log_file):
            return []
        with open(self.log_file, 'r') as f:
            return [json.loads(line) for line in f]
    
    def write_metadata(self, metadata):
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f)
    
    def read_metadata(self):
        if not os.path.exists(self.metadata_file):
            return None
        with open(self.metadata_file, 'r') as f:
            return json.load(f)
