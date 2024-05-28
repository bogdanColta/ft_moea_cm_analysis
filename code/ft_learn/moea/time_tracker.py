import time
import dill
import pandas as pd
import os

directory = "./timestamps/"
os.makedirs(directory, exist_ok=True)

class TimeTracker:
    def __init__(self,metric_config='11100000000000000000000', dataset="dataset", log_file="timestamps.dill"):
        self.log_file = log_file
        self.last_timestamp_start = {}
        self.timestamps = {}
        metric_config = [-int(x) for x in metric_config]
        processed_metric_config = "".join(map(str, metric_config))
        self.timestamps["metric_config"] = processed_metric_config
        self.timestamps["dataset"] = dataset
    
    def start_timer(self, segment_name):
        self.last_timestamp_start[segment_name] = time.time()
    
    def end_timer(self, segment_name):
        if (not segment_name in self.timestamps):
            self.timestamps[segment_name] = []
        start_time = self.last_timestamp_start[segment_name]
        self.timestamps[segment_name].append(time.time() - start_time)
        
        if segment_name == "pareto_sorting":
            with open("./timestamps/" + self.log_file + ".dill", "wb") as file:
                print(self.timestamps)
                dill.dump(pd.DataFrame(self.timestamps), file)
                # dill.dump(self.timestamps, file)