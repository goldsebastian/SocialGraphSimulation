import array
import sys
import random
import os

#read the binary.  Takes binary file name.
def readGraphBin(gFile):
    """ file format is as follows
    first is the size in ASCII followed by newline
    next is the sequence of degrees in binary, 4 bytes per item 
    next is the sequence of edges for each node, 
    there are no record separators -- sizes are determined by degrees """
    with open(gFile) as fin:
        size = int(fin.readline())
         
        def loadArray(sz):
            arr = array.array('I')
            arr.fromfile(fin, sz)
            return arr

        degree_seq = loadArray(size)
        return [loadArray(degree) for degree in degree_seq]
        
# write the connections graph to a file
def writeGraphBin(wFile, graph):
    """ file format is as follows
    first is the size in ASCII followed by newline
    next is the sequence of degrees in binary, 4 bytes per item
    next is the sequence of edges for each node.
    there are no record separators -- sizes are determines by degrees """
    with open(wFile, 'w') as fil:
        size = len(graph)
        degree_seq = array.array('I')
        for degree in graph:
            degree_seq.append(len(degree))
        
        fil.write(str(size) + "\n")
        degree_seq.tofile(fil)
        for line in graph:
            line.tofile(fil)
# write the meta data to a file
def writeMetaBin(wfile, meta):
    """file format is as follows:
    first is the length of the metadata array, followed by newline
    next is the width of the metadata array, followed by newline
    next is the metadata array, all integers, 8 bytes per item"""
    with open(wFile, 'w') as fil:
        length = len(meta)
        width = len(meta[0])
        
        fil.write(str(length) + "\n")
        fil.srite(str(width) + "\n")
        for line in meta:
            line.tofile(fil)

#write the communities to a file
def writeNetworksBin(wfile, graph):
    """ file format is as follows
    first is the size in ASCII followed by newline
    next is the sequence of degrees in binary, 4 bytes per item
    next is the sequence of edges for each node.
    there are no record separators -- sizes are determines by degrees """
    with open(wFile, 'w') as fil:
        size = len(graph)
        degree_seq = array.array('I')
        for degree in graph:
            degree_seq.append(len(degree))
        
        fil.write(str(size) + "\n")
        degree_seq.tofile(fil)
        for line in graph:
            line.tofile(fil)

# Takes the name of the file to be read and the max ID
# Returns the socialGraph (list of arrays), meta graph (list of arrays)
def readGraph(gFile, limit):
    graph = open(gFile, 'r')
    social = []
    meta = []
    size = 0
    print limit
    done1 = False
    print "progress shown below, out of about 4 million ids"
    for line in graph:
        if line[0] == '#': continue
        ids = line.split()
        idi = [int(ids[0]), int(ids[1])]
       
        while (idi[0] >= size) or (idi[1] >= size):
            size += 1
            social.append(array.array('I', []))
          
        social[idi[0]].append(idi[1])
        social[idi[1]].append(idi[0])
                
        if (idi[0] % 100) == 0:
            #print size, idi[0], "array good?", social[idi[0]][:6]
            sys.stdout.write("\r current size: %d  current id: %d" % (size, idi[0]))    # or print >> sys.stdout, "\r%d%%" %i,
            sys.stdout.flush()
           
    #meta.sort()
    return social, size

# generates the meta graph.  contains only id's and thresholds
# threshold defaults to uniform random distribution
def getMeta(social, size):
    meta = []
    for i in range(size):
        if len(social[i]) > 0:
            meta.append(array.array('d', [i, random.random()]))
            
    return meta

# Takes the name of the file containing the networks
def readNet(nfile):
    net = []
    return net

# makes sure a directory exists
def assureDir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

#main function
def main():
    socialGraph, idSpace = readGraph("lj-undirgraph.txt", -1)
    metaList = getMeta(socialGraph, idSpace)
    networks = readNet("lj-communities.txt")
    assureDir("./liveJournal/lj-socialgraph.bin")
    writeGraphBin("./liveJournal/lj-socialgraph.bin", socialGraph)
    assureDir("./liveJournal/lj-metalist.bin")
    writeMetaBin("./liveJournal/lj-metalist.bin", metaList)
    assureDir("./liveJournal/lj-networks.bin")
    writeNetworksBin("./liveJournal/lj-networks.bin", networks)


if __name__ == "__main__":
    main()
