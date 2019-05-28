import pandas as pd
import numpy as np 
import numba
import copy

def dfa_l(df, series, stage, order = 1):
    """
    Modified Detrend Fluctuation Analysis

    This a modification of the original Detrended Fluctuation Analysis Algorithm. Instead of using non-overlapping windows of varying
    sizes arbitrarily defined, the KS-Segmentation algorithm is used to detect intrinsic time scales within the time series and the segments
    are used to compute the fluctuations.

    *** This algorithm needs to be adapted to be more general. Currently, it works in the contex of sleep stage analysis with the KS-Segmentation. ***

    Input:
        - df: the pandas dataframe obtained from the segmentation algorithm.
        - series: a numpy array containing the time series
        - stage: the specified sleep stage whose segments will be analyzed
        - order: (=1 by default) the order of the polynomial that will be fitted at each segment

    Output:
        - fluctuations: the list of values [n, F(n)], where n is the size of the segment and F(n) its fluctuation.
    """

    fluctuations = []   # Will save the fluctuations and their corresponding domain (seg size)
    
    for idx in df.where(df["SleepStage"] == stage).dropna().index:      # Only the segments classified as the specified sleep stage
                                                                        # will be analyzed
        start = int(df.loc[idx, "start"])                               # starting point of the segment
        finish = int(df.loc[idx, "finish"])                             # ending point of the segment
        n = df.loc[idx, "size"]                                         # size of the segment
        data = series[start: finish+1]
        
        # integrate
        walk = np.cumsum(data - np.mean(data))
        
        # calculate local trends
        if n != len(walk): n += 1 # minor correction **** TODO: need to study this more carefully
            
        x = np.arange(n)
        tpoly = np.polyfit(x, walk, order)
        trend = np.polyval(tpoly, x)
        
        # calculate standard deviation ("fluctuations") around trend
        fluc = np.sqrt(np.sum((walk - trend)**2)/n)
        fluctuations.append([n, fluc])
        
    return fluctuations


@numba.jit
def PDFA(series, n, order):
    """
    Progressive Detrended Fluctuation Algorithm

    Input:
        - series: a numpy array containing the time series
        - n: the window size
        - order: the order of the polynomial that will be fitted at each window of size n

    OutputL
        - P: a list of values P(p), the fluctuations, where p = 1,..., N, and N = len(series)
    """
    
    # Calculate the profile
    profile = np.cumsum(series - np.mean(series))
    
    P = np.array([])        # Will save the fluctuations P(p)
    box_points = [0]        # Since the previous series are preserved at each loop on p, the boxes
                            # of size "n" previously calculated will be saved.
    trend = np.array([])    # The trends calculated for each box of size "n" will also be saved
                            # Before a new box of size "n" is detected, temporary boxes are used
                            # to include the last points of the partial sum
    for p in range(2, len(series)+1):
        partial_sum = profile[0: p]

        box_points_t = copy.deepcopy(box_points);       # All the previous boxes of size "n" are loaded into a temporary list
        box_points_t.extend([p])                        # And a temporary box 'T' of size m <= n is added to it.
        
        trend_t = copy.deepcopy(trend)                  # A temporary list of trends is also created to include the values of T
        
        x = np.arange(box_points_t[-1] - box_points_t[-2])          # -1 is the last value of the list
        if len(x) == 1:
            trend_t = np.concatenate((trend_t, partial_sum[-1:]))   # The single point is considered as a trend
        else:
            tpoly = np.polyfit(x, partial_sum[box_points_t[-2]: box_points_t[-1]], order)
            trend_t = np.concatenate((trend_t, np.polyval(tpoly, x)))
        
        if(p%n == 0):                                   # box_points will be updated only if T is a box of size m = n.
            box_points = copy.deepcopy(box_points_t)
            trend = copy.deepcopy(trend_t)
        
        summation = np.sqrt(np.sum( np.power(partial_sum - trend_t, 2) ))
        P = np.concatenate((P, np.asarray([summation])))
        
    return P

@numba.jit
def PDFA_modified(series, seg_end_points, n, order):
    """ 
    Modified Progressive Detrended Fluctuation Analysis

    A modification of the original PDFA, where instead of progressively increase the partial sums one point at a time,
    we apply the KS-Segmentation Algorithm to the series and increase the partial sum one segment at a time. The objective is
    to detect abrupt changes between segments.

    ****** This algorithm must be tested ******

    Input:
        - series: a numpy array containing the time series
        - seg_end_points: a list containing the end points of all the segments of the time series
        - n: the window size
        - order: the order of the polynomial that will be fitted at each window of size n

    Output:
        - P: the list of values P(p), where p are the sorted segment sizes.
    """

    # Calculate the profile
    profile = np.cumsum(series - np.mean(series))

    P = np.array([])            # Will save the fluctuations P(p)
    box_points = [0]            # Since the previous series are preserved at each loop on p, the boxes
                                # of size "n" previously calculated will be saved.
    trend = np.array([])        # The trends calculated for each box of size "n" will also be saved
                                # Before a new box of size "n" is detected, temporary boxes are used
                                # to include the last points of the partial sum    
    for p in seg_end_points:
        partial_sum = profile[0: p]         # The partial sums will be increase one segment of size "s" at a time.

        new_boxes = list(range(box_points[-1], p, n));      # At each loop, new boxes must be fitted insed the added segment
        new_boxes.extend([p])                               # The border between two segments will never be inside a window.

        for i in range(1, len(new_boxes)):
            x = np.arange(new_boxes[i] - new_boxes[i-1])    # -1 is the last value of the list
            if len(x) == 1:
                trend = np.concatenate((trend, partial_sum[-1:]))
            else:
                y = partial_sum[new_boxes[i-1]: new_boxes[i]]
                tpoly = np.polyfit(x, y, order)
                trend = np.concatenate((trend, np.polyval(tpoly, x)))

        box_points.extend(new_boxes[1:])

        summation = np.sqrt(np.sum( np.power(partial_sum - trend, 2) ))
        P = np.concatenate((P, np.asarray([summation])))
        
    return P


def tratamento(f_l, n_stages, log = 1):
    """
    Auxiliary function used to apply the dfa_l algorithm to hrv time series.

    Input:
        - f_l: a dataframe containing the fluctuations for all groups, series and sleep stages.
        - n_stages: the number of stages (4 or 6)
        - log: (=1 by default) a boolean that specifies if the values must be converted to their logarithms or not.
    """
    for g in range(3):
        for s in range(4):
            for p in range(n_stages):
                # Mark empty functions
                if(len(f_l[g][s][p]) == 0):
                    f_l[g][s][p] = pd.DataFrame([[np.nan, np.nan]])
                else:
                    # Rename columns
                    f_l[g][s][p].columns = ["L", "coef"]
                    
                    # Count the occurances of segment sizes
                    sr = f_l[g][s][p]["L"].value_counts()
                    # Compute the mean of F(n) for n with more than 1 occurrance
                    rep_vals = sr.where(sr > 1).dropna().index
                    for v in rep_vals:
                        df = f_l[g][s][p].where(f_l[g][s][p]["L"] == v).dropna()
                        mean = df["coef"].values.mean()
                        f_l[g][s][p].loc[df.index, "coef"] = mean
                    
                    # Delete repeated values
                    f_l[g][s][p] = f_l[g][s][p].drop_duplicates()
                    # Correct the index
                    f_l[g][s][p].index = pd.Index(range(0, len(f_l[g][s][p])))
                    
                    # Change values for their logarithms
                    if log == 1:
                        f_l[g][s][p].loc[:, "L"] = np.log10(f_l[g][s][p]["L"].values) 
                        f_l[g][s][p].loc[:, "coef"] = np.log10(f_l[g][s][p]["coef"].values) 
    return f_l 
    