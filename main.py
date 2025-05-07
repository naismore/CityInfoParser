import scripts.extract.rosstat.rosstat_extract_data as rosstat
import scripts.extract.wikipedia.wikipedia_extract_data as wikipedia
from scripts.load.load_to_db import load_data
from scripts.transform.transform_data import transform_data

try:
    rosstat.download_data()
    rosstat_raw_data = rosstat.extract_data()
    wiki_raw_data = wikipedia.extract_data()
    data = transform_data(rosstat_raw_data, wiki_raw_data)
    load_data(data)
except Exception as e:
    print(e)