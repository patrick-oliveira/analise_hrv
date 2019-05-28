import pandas as pd
import numpy as np 

def load(data, seg_res, n_stages):    
    # Load the data of the increments
    increments = [[[], [], [], []],
                  [[], [], [], []],
                  [[], [], [], []]]

    for grupo in range(3):
        for serie in range(4):
            if n_stages == 6:
                saltos_temp = [ [],
                                [],
                                [],
                                [],
                                [],
                                [] ]
            else:
                saltos_temp = [ [],
                                [],
                                [],
                                [] ]
                
            n_saltos = ["Serie 0 Saltos", "Serie 1 Saltos", "Serie 2 Saltos", "Serie 3 Saltos"]

            for i in range(len(data[grupo])):
                if n_stages == 6:
                    sep_seg_fase = [seg_res[grupo][i][serie][ seg_res[grupo][i][serie]["SleepStage"] == 0 ],
                                    seg_res[grupo][i][serie][ seg_res[grupo][i][serie]["SleepStage"] == 1 ],
                                    seg_res[grupo][i][serie][ seg_res[grupo][i][serie]["SleepStage"] == 2 ],
                                    seg_res[grupo][i][serie][ seg_res[grupo][i][serie]["SleepStage"] == 3 ],
                                    seg_res[grupo][i][serie][ seg_res[grupo][i][serie]["SleepStage"] == 4 ],
                                    seg_res[grupo][i][serie][ seg_res[grupo][i][serie]["SleepStage"] == 5 ]]
                else:
                    sep_seg_fase = [seg_res[grupo][i][serie][ seg_res[grupo][i][serie]["SleepStage"] == 0 ],
                                    seg_res[grupo][i][serie][ seg_res[grupo][i][serie]["SleepStage"] == 1 ],
                                    seg_res[grupo][i][serie][ seg_res[grupo][i][serie]["SleepStage"] == 2 ],
                                    seg_res[grupo][i][serie][ seg_res[grupo][i][serie]["SleepStage"] == 3 ]]
                    
                for j in range(n_stages):
                    for k in sep_seg_fase[j].index:
                        start =  int(sep_seg_fase[j]["start"][k])
                        finish = int(sep_seg_fase[j]["finish"][k])
                        saltos_temp[j].extend(list(data[grupo][i][start:finish+1][n_saltos[serie]]))
                    #saltos_temp[j] = [np.abs(x) for x in saltos_temp[j] if x != 0.0]
            
            if n_stages == 6:
                increments[grupo][serie] = [ pd.Series(saltos_temp[0]).dropna(),
                                             pd.Series(saltos_temp[1]).dropna(),
                                             pd.Series(saltos_temp[2]).dropna(),
                                             pd.Series(saltos_temp[3]).dropna(),
                                             pd.Series(saltos_temp[4]).dropna(),
                                             pd.Series(saltos_temp[5]).dropna()]
            else:
                increments[grupo][serie] = [ pd.Series(saltos_temp[0]).dropna(),
                                             pd.Series(saltos_temp[1]).dropna(),
                                             pd.Series(saltos_temp[2]).dropna(),
                                             pd.Series(saltos_temp[3]).dropna()]
                

    # Calculates the absolute values of the increments
    for grupo in range(3):
        for serie in range(4):
            for fase in range(n_stages):
                increments[grupo][serie][fase] = pd.Series([np.abs(x) for x in increments[grupo][serie][fase] if x != 0]).dropna().values
    
    return increments