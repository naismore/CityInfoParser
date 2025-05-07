import scripts.extract.rosstat.rosstat_extract_data as rosstat
<<<<<<< HEAD
import scripts.extract.wikipedia.wikipedia_extract_data as wikipedia
from scripts.transform.transform_data import transform_data
#TODO: Убрать комментарий
#rosstat.download_data()
rosstat_data = rosstat.extract_data()
wiki_data = wikipedia.extract_data()
transform_data(rosstat_data, wiki_data)
=======

try:
    rosstat.download_data()
    rosstat.extract_data()
except Exception as e:
    print(e)
>>>>>>> 1008506 (no message)
