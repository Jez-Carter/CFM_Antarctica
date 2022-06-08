import h5py
import numpy as np
import xarray as xr

def load_data(filename):
    with h5py.File(filename,'r') as cfm_results:
        keys = list(cfm_results.keys())
        depth = cfm_results['depth']
        times = depth[:,0]
        cells = np.arange(0,len(depth[0,1:]),1)
        coords1d = dict(time=(["time"], times))
        coords2d = dict(time=(["time"], times),cell=(["cell"], cells))
        data = dict(depth=(["time", "cell"], depth[:,1:]))
        ds = xr.Dataset(data_vars=data,coords=coords2d)

        if 'DIP' in keys:
            ds["delta_ele"]=(['time'],cfm_results['DIP'][:,5])
            ds["cum_ele"]=(['time'],cfm_results['DIP'][:,6])
        if 'compaction' in keys:
            ds["compaction"]=(['time', 'cell'],  cfm_results['compaction'][:,1:])
            ds["tot_compaction"]=(['time'],np.sum(cfm_results['compaction'][:,1:],axis=1))
            ds["cum_compaction"]=np.cumsum(ds["compaction"],axis=1)
            ds["cum_tot_compaction"]=np.cumsum(ds["tot_compaction"])
        if 'density' in keys:
            ds["density"]=(['time', 'cell'],  cfm_results['density'][:,1:])
        if 'Modelclimate' in keys:
            ds["snowfall"]=(['time'],cfm_results['Modelclimate'][:,1])
            
        #custom fields:
        ds['width']=ds['depth'].diff("cell",label='lower')
        ds['mass'] = ds['density']*ds['width']
        ds['cum_mass'] = np.cumsum(ds["mass"],axis=1)
        
        
    return(ds)