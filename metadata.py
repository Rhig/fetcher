import json
import os
from datetime import datetime

class Metadata:
    def __init__(self, metadata_filepath="metadata.json"):
        self.metadata_filepath = metadata_filepath
        self.metadata = {}

    def read_metadata(self):
        if os.path.exists(self.metadata_filepath):
            with open(self.metadata_filepath, "r") as f:
                self.metadata = json.load(f)
    
    def write_metadata(self):
        with open(self.metadata_filepath, "w") as f:
            json.dump(self.metadata, f)

    def update_page_metadata(self, url, num_of_links, num_of_images):
        # Assuming single thread/process application, this should be OK.
        # If multiple threads/processes access the metadata at once, we will need to add a locking mechanism or even use a DB.
        if not self.metadata:
            self.read_metadata()
        self.metadata[url] = {
            "num_links": num_of_links,
            "images": num_of_images,
            "last_fetch": datetime.now().strftime("%a %b %d %Y %H:%M %Z"),
        }
        self.write_metadata()

    def get_page_metadata(self, url):
        if not self.metadata:
            self.read_metadata()
        return self.metadata.get(url, {})