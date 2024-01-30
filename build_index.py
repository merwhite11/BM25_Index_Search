# input:
#data folder
#output path to serialized index

#output:
#create an index and serialize the index to a file (JSON)
import os
import json
import argparse

# data_path = "./assets/scrape_0"
# output_file = "index_0.json"

# files = os.listdir(data_path)

def main():
  parser = argparse.ArgumentParser(description='Build an index from data folder.')
  parser.add_argument('--data_folder', type=str, help='Path to the data folder', required=True)
  parser.add_argument('--output_index', type=str, help='Name of the output index', required=True)

  args = parser.parse_args()
  build_index(args.data_folder, args.output_index)

def create_index(data_path):
  files = os.listdir(data_path)
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

def serialize_index(index, output_index):
  with open(output_index, 'w') as json_file:
    json.dump(index, json_file, indent=2)

def build_index(data_folder, output_index) :
  data_path = f"./assets/{data_folder}"
  index = create_index(data_path)
  serialize_index(index, output_index)


if __name__ == "__main__":
    main()


