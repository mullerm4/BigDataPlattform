from os import listdir, path
import json

class Fetching():
    def __init__(self, observing_dir, json_profile):
        config = json.loads(open(json_profile).read())

        self.constraints = tuple(config["suportedformats"])
        self.number_of_files = config['numberoffiles']
        self.files_sizes = config["sizelimit"]
        self.overserving_dir = observing_dir
        self.fetch_list = []

    def fetchFiles(self):
        onlyfiles = [f for f in listdir(self.overserving_dir) if path.isfile(path.join(self.overserving_dir, f)) and f.endswith(self.constraints)]

        while len(self.fetch_list) < self.number_of_files and onlyfiles:
            item = onlyfiles.pop(-1)
            file_size = path.getsize(path.join(self.overserving_dir, item)) / 1024
            if file_size > self.files_sizes:
                print("%s is bigger than the size limit of %s KB" %(item, self.files_sizes))
                continue
            item_path = path.join(self.overserving_dir, item)
            if item_path not in self.fetch_list:
                self.fetch_list.append(item_path)
        return self.fetch_list

