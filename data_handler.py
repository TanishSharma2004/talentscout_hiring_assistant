import json
import os

class DataHandler:
    def __init__(self):
        self.data_file = "candidates.json"

    def save_candidate(self, candidate_info):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                data = json.load(f)
        else:
            data = []
        data.append(candidate_info)
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=4)