# input:
#data folder
#output path to serialized index

#output:
#create an index and serialize the index to a file (JSON)
import os
import json
import pickle

data_path = "./assets/scrape_0"
output_file = "index_0.json"

files = os.listdir(data_path)

def create_index(files):
  index = []
  for filename in files:
    if filename.endswith(".txt"):
      file_path = os.path.join(data_path, filename)

      with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

      metadata = {
        'filename': filename,
        'size': os.path.getsize(file_path)
      }

      flattened_entry = {
        'filename': filename,
        'content': content,
        'metadata': metadata
      }

      index.append(flattened_entry)
  return index

def serialize_index(index, output_file):
  with open(output_file, 'w') as json_file:
    json.dump(index, json_file, indent=2)
    #pickle.dump(index, file)

def build_index(data_folder, output_index) :

  index = create_index(files)
  serialize_index(index, output_file)


build_index(data_path, output_file)


