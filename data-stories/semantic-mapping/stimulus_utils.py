from textgrid import TextGrid
import os
import numpy as np
from collections import defaultdict

def load_grid(story, grid_dir="data/grids"):
    """Loads the TextGrid for the given [story] from the directory [grid_dir].
    The first file that starts with [story] will be loaded, so if there are
    multiple versions of a grid for a story, beward.
    """
    gridfile = [os.path.join(grid_dir, gf) for gf in os.listdir(grid_dir) if gf.startswith(story)][0]
    return TextGrid(open(gridfile).read())

def load_grids_for_stories(stories):
    """Loads grids for the given [stories], puts them in a dictionary.
    """
    return dict([(st, load_grid(st)) for st in stories])

def load_5tier_grids_for_stories(stories, rootdir):
    grids = dict()
    for story in stories:
        storydir = os.path.join(rootdir, [sd for sd in os.listdir(rootdir) if sd.startswith(story)][0])
        storyfile = os.path.join(storydir, [sf for sf in os.listdir(storydir) if sf.endswith("TextGrid")][0])
        grids[story] = TextGrid(open(storyfile).read())
    return grids


class TRFile(object):
    def __init__(self, trfilename, expectedtr=2.0045):
        """Loads data from [trfilename], should be output from stimulus presentation code.
        """
        self.trtimes = []
        self.soundstarttime = -1
        self.soundstoptime = -1
        self.otherlabels = []
        self.expectedtr = expectedtr
        
        if trfilename is not None:
            self.load_from_file(trfilename)
        

    def load_from_file(self, trfilename):
        """Loads TR data from report with given [trfilename].
        """
        ## Read the report file and populate the datastructure
        for ll in open(trfilename):
            timestr = ll.split()[0]
            label = " ".join(ll.split()[1:])
            time = float(timestr)

            if label in ("init-trigger", "trigger"):
                self.trtimes.append(time)

            elif label=="sound-start":
                self.soundstarttime = time

            elif label=="sound-stop":
                self.soundstoptime = time

            else:
                self.otherlabels.append((time, label))
        
        ## Fix weird TR times
        itrtimes = np.diff(self.trtimes)
        badtrtimes = np.nonzero(itrtimes>(itrtimes.mean()*1.5))[0]
        newtrs = []
        for btr in badtrtimes:
            ## Insert new TR where it was missing..
            newtrtime = self.trtimes[btr]+self.expectedtr
            newtrs.append((newtrtime,btr))

        for ntr,btr in newtrs:
            self.trtimes.insert(btr+1, ntr)

    def simulate(self, ntrs):
        """Simulates [ntrs] TRs that occur at the expected TR.
        """
        self.trtimes = list(np.arange(ntrs)*self.expectedtr)
    
    def get_reltriggertimes(self):
        """Returns the times of all trigger events relative to the sound.
        """
        return np.array(self.trtimes)-self.soundstarttime

    @property
    def avgtr(self):
        """Returns the average TR for this run.
        """
        return np.diff(self.trtimes).mean()

def load_generic_trfiles(stories, root="data/trfiles"):
    """Loads a dictionary of generic TRFiles (i.e. not specifically from the session
    in which the data was collected.. this should be fine) for the given stories.
    """
    trdict = dict()

    for story in stories:
        try:
            trf = TRFile(os.path.join(root, "%s.report"%story))
            trdict[story] = [trf]
        except Exception as e:
            print (e)
    
    return trdict
