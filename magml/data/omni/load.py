import pyspedas
import pandas as pd
import numpy as np
from datetime import timezone

def unix2datetime(unix_list):
    """
    Convert a list of Unix timestamps to datetime.

    Args:
        unix_list (array-like): List or array of Unix timestamps.

    Returns:
        np.array: Array of converted datetime objects.
    """
    date_list = pd.to_datetime(unix_list, unit='s')
    return np.array(date_list)

def fill_gap(x, y, max_gap):
    """
    Identify gaps in time-series data and interpolate missing values.

    Args:
        x (np.array): Time values.
        y (np.array): Corresponding data values.
        max_gap (int): Maximum gap size to interpolate. Gaps larger than this are filled with NaN.

    Returns:
        np.array: Interpolated data with gaps filled.
    """
    dx = x[1:] - x[0:-1]  # time step
    dt0 = np.median(dx)

    if np.any(np.abs(dx - dt0) > 0.01 * dt0):  
        print("Warning: time step is not constant") 

    idx = np.where(np.isfinite(x) & np.isfinite(y))
    idx = idx[0]
   
    data_interp = np.interp(x, x[idx], y[idx], right=np.nan, left=np.nan)
    
    for i in range(len(idx) - 1):  
        if (idx[i + 1] - idx[i]) > max_gap:
            data_interp[idx[i] + 1: idx[i + 1]] = np.nan 

    return data_interp

class InputVar:
    """
    A class to load and preprocess input variables from omni datasets.

    Attributes:
        name (str): Name of the variable to retrieve.
        start_time (str): Start time in YYYY-MM-DD format.
        end_time (str): End time in YYYY-MM-DD format.
        gap_max (int): Maximum gap size for interpolation.
        no_update (bool): If True, prevents automatic data updates.
        data_type (str): Type of data resolution (e.g., '5min').
    """

    def __init__(self, name=None, start_time='2012-10-01', end_time='2017-10-01', gap_max=180, no_update=True, data_type='5min'):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.tdata = None
        self.data = None
        self.gap_max = gap_max
        self.no_update = no_update
        self.data_type = data_type
        self.vars = pyspedas.omni.data(trange=[self.start_time, self.end_time], datatype=self.data_type, notplot=True,
                                       varnames=self.name, no_update=self.no_update)

    def get_data(self, name, gap_fill=True):
        """
        Retrieve data for the specified variable and optionally fill gaps.

        Args:
            name (str): Name of the variable to retrieve.
            gap_fill (bool): Whether to fill missing data gaps (default: True).

        Returns:
            pd.DataFrame: Dataframe containing time-indexed data.
        """
        if name == 'f10_7':
            raise ValueError("Variable 'f10_7' is not available.")

        self.tdata_new = np.array(self.vars[name]['x'])
        #print(self.tdata_new)
        #self.timestamp_new = np.array([tdata.replace(tzinfo=timezone.utc) for tdata in self.tdata_new])
        #self.tdata = np.array([tdata.timestamp() for tdata in self.tdata_new])
        self.tdata = self.tdata_new.astype('datetime64[s]').astype(int)
        #print(self.tdata)
        self.data = np.array(self.vars[name]['y'])

        if gap_fill:
            print(f'Filling gaps in {name}')
            self.data = fill_gap(self.tdata, self.data, max_gap=self.gap_max)
        
        self.tdate = unix2datetime(self.tdata)
        frame = pd.DataFrame(data={'date': self.tdate, name: self.data})
        frame.set_index('date', inplace=True, drop=True)

        return frame
