import requests

baseUrl = 'http://www.illustris-project.org/api/'
headers = {"api-key":"cc4ff6392e79c9e08c158e5ae5493718"}

def get(path, params=None): #gets data from url, saves to file
    # make HTTP GET request to path
    r = requests.get(path, params=params, headers=headers)

    # raise exception if response code is not HTTP SUCCESS (200)
    r.raise_for_status()

    if r.headers['content-type'] == 'application/json':
        return r.json() # parse json responses automatically

    # Saves to file, currently disabled
    if 'content-disposition' in r.headers:
        filename = r.headers['content-disposition'].split("filename=")[1]
        with open(filename, 'wb') as f:
            f.write(r.content)
        return 'this' # return the filename string

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
