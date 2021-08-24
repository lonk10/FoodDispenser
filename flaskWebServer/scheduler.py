#!/usr/bin/env python3

import json

class Config:

    def __init__(self, url):
        with open(url, "r") as file:
            self.conf_dict = json.load(file)

    def get_key(self, key):
        return self.conf_dict[key]

    def set_key(self, key, attr):
        self.conf_dict[key].append(attr)

    def set_entry(self, schedule, weight):
        self.set_key("orari", schedule)
        self.set_key("grammi", weight)
        with open("scheduler.json", "w") as file:
            json.dump(self.conf_dict, file)

if __name__ == "__main__":
    data = Config("scheduler.json")
    while True:
        a = input("set key: ")
        b = input("set attr: ")
        print(data.get_key(a))
        data.set_key(a, b)
        print(data.get_key(a))
        with open("scheduler.json", "w") as file:
            json.dump(data.conf_dict, file)

    
    
