from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot
import logging
import tqdm
from ..omni.load import unix2datetime


from tqdm import tqdm
import numpy as np
import logging
import pyspedas
from pytplot import get_data
from scipy import interpolate
logging.getLogger().setLevel(logging.CRITICAL)

def hyperload(start_time, end_time, time_cadence=300, data_items=['L','FESA'], v_index = [None,0], interp_method = 'nearest'):
    time_array_product = np.arange(start_time, end_time,time_cadence, dtype='datetime64[s]')
    data_result = np.zeros((len(time_array_product),len(data_items)))
    if (np.datetime64(end_time) - np.datetime64(start_time)) < np.timedelta64(30, 'D'):
        pass
    else:
        # Generate monthly timestamps including the end time
        month_list = np.append(
            np.arange(start_time, end_time, dtype='datetime64[M]').astype('datetime64[D]'),
            np.datetime64(end_time)
        )

        print("Months to process:", month_list)

        # tqdm should wrap the iterable directly
    for i, m in enumerate(tqdm(month_list.astype(str)[:-1], desc="Processing Months")):
        m_next = month_list.astype(str)[i+1]
        print(f"Processing {m} -> {m_next }")
        rept_vars = pyspedas.projects.rbsp.rept(trange=[m, m_next ], level='l2', rel='rel03')
        
        index = np.where((time_array_product>=np.datetime64(m).astype('datetime64[D]')) &
                         (time_array_product<np.datetime64(m_next).astype('datetime64[D]')))
        # interpolate the result
        for k, item in enumerate(data_items):
            data = get_data(item)
            if v_index[k] is not None:
                f = interpolate.interp1d(data.times, data.y[:,v_index[k]],bounds_error=False,kind = interp_method)
            else:
                f = interpolate.interp1d(data.times, data.y,bounds_error=False,kind = interp_method )
            data_new = f(time_array_product[index].astype(int))
            data_result[index,k] = data_new
    return time_array_product,data_result