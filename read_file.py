import numpy as np
import os

class get_data:
    def __init__(self, path):
        self.path = path

    def get_files(self,path):
        fname = ''.join(path + '/FINITE_VOLUME_CENTROID_COORDINATES.TXT')
        with open(fname, 'r') as f:
            coords = np.array([float(line) for line in f])
        f.close()
        fname = ''.join(path + '/DOMAIN_SIZE.TXT')
        with open(fname, 'r') as f:
            dom_size = np.array([float(line) for line in f])
        f.close()
        fname = ''.join(path + '/MOLE_FRACTIONS.TXT')
        with open(fname, 'r') as f:
            mf = np.array([float(line) for line in f])
        f.close()
        fname = ''.join(path + '/TIME.TXT')
        with open(fname, 'r') as f:
            time = np.array([float(line) for line in f])
        f.close()
        fname = ''.join(path + '/ELEMENT_NAMES.TXT')
        with open(fname, 'r') as f:
            elnames = f.read().split()
        f.close()	
        fname = ''.join(path + '/PHASE_NAMES.TXT')
        with open(fname, 'r') as f:
            phnames = f.read().split()
        f.close()
        nel = np.size(elnames)
        nph = np.size(phnames)
        self.ngp = np.size(mf)/nel/nph/np.size(time)

        return coords, dom_size, mf, nel, ngp, nph, time, elnames, phnames
