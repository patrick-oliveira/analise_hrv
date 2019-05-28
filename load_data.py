import pandas as pd 
import numpy as np


def load_data(filter = 1):
    # Define the variables (for organization)
    titles_hypertensive = "file_titles_ht.txt"
    titles_normotensive = "file_titles_nt.txt"
    titles_proband      = "file_titles_pb.txt"
    data_path   = "data/raw_data_with_increments/"
    seg_paths   = ["data/segmentation_dataframes_hypertensive/",
                   "data/segmentation_dataframes_normotensive/",
                   "data/segmentation_dataframes_proband/"]
    series_titles  = ["Serie 0", "Serie 1", "Serie 2", "Serie 3"]

    # Extract the titles of the data file of each subject
    text_files = [open(titles_hypertensive, "r"), open(titles_normotensive, "r"), open(titles_proband, "r")]
    file_titles = [[x.strip() for x in text_files[0].readlines()],
                   [x.strip() for x in text_files[1].readlines()],
                   [x.strip() for x in text_files[2].readlines()]]
    text_files[0].close(); text_files[1].close(); text_files[2].close()

    # Load the raw data of the series
    number_of_subjects = [len(file_titles[0]), len(file_titles[1]), len(file_titles[2])]
    seg_res = [[], [], []]
    data = [[], [], []]
    for j in range(3):
        for i in range(number_of_subjects[j]):
            data[j].append(pd.read_csv(data_path+file_titles[j][i][15:]+".csv", index_col = 0))

    # Load the segmentation data
    for j in range(3):    
        for i in range(number_of_subjects[j]):
            temp = [pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()]

            for k in range(4):
                temp[k] = pd.read_csv(seg_paths[j]+file_titles[j][i][15:][:-4]+"_"+series_titles[k]+".csv").set_index("index")
                length = len(temp[k].index)

            seg_res[j].append(temp.copy())
    
    if filter == 1:
        # Delete the segments with undeterminated stage or whose defined stage has a frequency below 85%
        for i in range(3):
            for j in range(len(seg_res[i])):
                for k in range(4):
                    seg_res[i][j][k] = seg_res[i][j][k].drop(seg_res[i][j][k][seg_res[i][j][k]["SleepStage"] == 66.0].index)
                    for l in seg_res[i][j][k].index:
                        if max(seg_res[i][j][k].loc[l, "0_%":"66_%"]) < 0.85:
                            seg_res[i][j][k] = seg_res[i][j][k].drop(l)
                        
    return data, seg_res

def redo_classification(seg_res, data):    
    # Reclassificates the segments using the 4 stage system.
    for i in range(3):
        for j in range(len(seg_res[i])):
            data[i][j]["SleepStage"] = data[i][j]["SleepStage"].replace(to_replace = 2.0, value = 1.0)
            data[i][j]["SleepStage"] = data[i][j]["SleepStage"].replace(to_replace = [3.0, 4.0], value = 2.0)
            data[i][j]["SleepStage"] = data[i][j]["SleepStage"].replace(to_replace = 5.0, value = 3.0)
            for k in range(4):
                seg_res[i][j][k]["SleepStage"] = seg_res[i][j][k]["SleepStage"].replace(to_replace = 2.0, value = 1.0)
                seg_res[i][j][k]["SleepStage"] = seg_res[i][j][k]["SleepStage"].replace(to_replace = [3.0, 4.0], value = 2.0)
                seg_res[i][j][k]["SleepStage"] = seg_res[i][j][k]["SleepStage"].replace(to_replace = 5.0, value = 3.0)

    return seg_res