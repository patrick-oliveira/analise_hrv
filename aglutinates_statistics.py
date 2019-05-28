import numpy as np

def aglutinates(data, seg_res, n_stages):
    # Aglutinates the segments statistics of all the subjects, distinguishing them only by their groups.

    means     = [[], [], []]
    medians   = [[], [], []]
    variances = [[], [], []]
    lengths   = [[], [], []]
    t_i       = [[], [], []]
    t_f       = [[], [], []]
    delta_t   = [[], [], []]

    for group in range(3):
        means_series_temp     = [[], [], [], []]
        medians_series_temp   = [[], [], [], []]
        variances_series_temp = [[], [], [], []]
        lengths_series_temp   = [[], [], [], []]
        t_i_series_temp       = [[], [], [], []]
        t_f_series_temp       = [[], [], [], []]
        delta_t_series_temp   = [[], [], [], []]
        
        for series in range(4):
            if n_stages == 6:
                means_stages_temp     = [[], [], [], [], [], []]
                medians_stages_temp   = [[], [], [], [], [], []]
                variances_stages_temp = [[], [], [], [], [], []]
                lengths_stages_temp   = [[], [], [], [], [], []]
                t_i_stages_temp       = [[], [], [], [], [], []]
                t_f_stages_temp       = [[], [], [], [], [], []]
                delta_t_stages_temp   = [[], [], [], [], [], []]
            else:
                means_stages_temp     = [[], [], [], []]
                medians_stages_temp   = [[], [], [], []]
                variances_stages_temp = [[], [], [], []]
                lengths_stages_temp   = [[], [], [], []]
                t_i_stages_temp       = [[], [], [], []]
                t_f_stages_temp       = [[], [], [], []]
                delta_t_stages_temp   = [[], [], [], []]
                

            for i in range(len(data[group])): 
                df = seg_res[group][i][series]  
                for j in range(n_stages):
                    for index in df.where(df["SleepStage"] == j).dropna().index:
                        means_stages_temp[j].append(df["mean"][index])
                        medians_stages_temp[j].append(df["Median"][index])
                        variances_stages_temp[j].append(df["variance"][index])
                        lengths_stages_temp[j].append(df["finish"][index] - df["start"][index])
                        t_i_stages_temp[j].append(df["T_i"][index])
                        t_f_stages_temp[j].append(df["T_f"][index])
                        delta_t_stages_temp[j].append(df["Dt"][index])

            for i in range(n_stages):
                means_stages_temp[i]     = np.log(np.asarray(means_stages_temp[i]))
                medians_stages_temp[i]   = np.log(np.asarray(medians_stages_temp[i]))
                variances_stages_temp[i] = np.log(np.asarray(variances_stages_temp[i]))
                lengths_stages_temp[i]   = np.log(np.asarray(lengths_stages_temp[i]))

                t_i_stages_temp[i]     = np.asarray(t_i_stages_temp[i])
                t_f_stages_temp[i]     = np.asarray(t_f_stages_temp[i])
                delta_t_stages_temp[i] = np.asarray(delta_t_stages_temp[i])
            
            means_series_temp[series]     = means_stages_temp
            medians_series_temp[series]   = medians_stages_temp
            variances_series_temp[series] = variances_stages_temp
            lengths_series_temp[series]   = lengths_stages_temp
            t_i_series_temp[series]       = t_i_stages_temp
            t_f_series_temp[series]       = t_f_stages_temp
            delta_t_series_temp[series]   = delta_t_stages_temp
        
        means[group]     = means_series_temp
        medians[group]   = medians_series_temp
        variances[group] = variances_series_temp
        lengths[group]   = lengths_series_temp
        t_i[group]       = t_i_series_temp
        t_f[group]       = t_f_series_temp
        delta_t[group]   = delta_t_series_temp
    
    return means, medians, variances, lengths, t_i, t_f, delta_t
