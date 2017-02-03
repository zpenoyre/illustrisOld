import requests
import h5py
import numpy as np

baseUrl = 'http://www.illustris-project.org/api/'
headers = {"api-key":"cc4ff6392e79c9e08c158e5ae5493718"}

def get(path, params=None): #gets data from url, saves to file
    # make HTTP GET request to path
    r = requests.get(path, params=params, headers=headers)

    # raise exception if response code is not HTTP SUCCESS (200)
    r.raise_for_status()

    if r.headers['content-type'] == 'application/json':
        return r.json() # parse json responses automatically

    tempFile='temp.hdf5'
    # Saves to file, currently disabled
    if 'content-disposition' in r.headers:
        filename = r.headers['content-disposition'].split("filename=")[1]
        with open(tempFile, 'wb') as f:
            f.write(r.content)
        return tempFile # return the filename string

    return r

def getSim(simName):
    r = get(baseUrl)
    names = [sim['name'] for sim in r['simulations']]
    i = names.index(simName)
    sim = get( r['simulations'][i]['url'] )
    return sim
    
def getSnap(sim,whichSnap):
    snaps = get( sim['snapshots'] )
    snap = get( snaps[whichSnap]['url'] )
    return snap
    
def getSub(subs,whichSub):
    sub_url=subs['results'][whichSub]['url']
    sub=get(sub_url)
    return sub

def getData(sub): #at the moment only return pos and vel, would love to generalise
    cut_req={'dm':'Coordinates,Velocities'}
    cutout=get(sub['meta']['url']+'cutout.hdf5',cut_req)
    
    with h5py.File(cutout,'r') as f:
        x = f['PartType1']['Coordinates'][:,0] - sub['pos_x'] # ckpc/h
        y = f['PartType1']['Coordinates'][:,1] - sub['pos_y']
        z = f['PartType1']['Coordinates'][:,2] - sub['pos_z']
        vx = f['PartType1']['Velocities'][:,0] - sub['vel_x'] # km/s
        vy = f['PartType1']['Velocities'][:,1] - sub['vel_y']
        vz = f['PartType1']['Velocities'][:,2] - sub['vel_z']
    return np.vstack((x,y,z)),np.vstack((vx,vy,vz))