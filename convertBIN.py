import array
import sys
import random
import os


# generate mapping array to re-index at 0 with no missing id's
def getMap(socialOld):
    idMap = array.array('i')
    curId = 0
    for node in socialOld:
        if (len(node) == 0):
            idMap.append(-1)
        else:
            idMap.append(curId)
            curId += 1
    
    return idMap

# write the ID map to a file
def writeIdMapBin(wfile, idMap):
    """file format is as follows:
    first is the length of the idMap array, followed by newline
    next is the idMap array, all integers, 4 bytes per item"""
    with open(wfile, 'w') as fil:
        length = len(idMap)        
        fil.write(str(length) + "\n")
        idMap.tofile(fil)

# re-index socialGraph using already computed idMap
def reIndexSocial(socialOld, idMap):
    socialNew = []
    for node in socialOld:
        if len(node) > 0:
            friendArray = array.array('i')
            for friend in node:
                friendArray.append(idMap[friend])
            
            socialNew.append(friendArray)
    return socialNew
        
# re-index networks graph using already computed idMap
def reIndexNets(netsOld, idMap):
    nets = []
    for membersListOld in netsOld:
        membersNew = [idMap[idOld] for idOld in membersListOld]
        nets.append(array.array('i', membersNew))
    
    return nets

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
            arr = array.array('i')
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
        degree_seq = array.array('i')
        for degree in graph:
            degree_seq.append(len(degree))
        
        fil.write(str(size) + "\n")
        degree_seq.tofile(fil)
        for line in graph:
            line.tofile(fil)
 
# generates the meta graph.  contains only id's and thresholds
# threshold defaults to uniform random distribution
def genMeta(size):
    meta = []
    for i in range(size):
        meta.append(array.array('d', [random.random()]))
            
    return meta
 
# write the meta data to a file
def writeMetaBin(wfile, meta):
    """file format is as follows:
    first is the length of the metadata array, followed by newline
    next is the width of the metadata array, followed by newline
    next is the metadata array, all integers, 8 bytes per item"""
    with open(wfile, 'w') as fil:
        length = len(meta)
        width = len(meta[0])
        
        fil.write(str(length) + "\n")
        fil.write(str(width) + "\n")
        for line in meta:
            line.tofile(fil)

# read the meta list from binary
def readMetaBin(rfile):
    """file format is as follows:
    first is the length of the metadata array, followed by newline
    next is the width of the metadata array, followed by newline
    next is the metadata array, all integers, 8 bytes per item"""
    with open(rfile, 'r') as fin:
        length = int(fin.readline())
        width = int(fin.readline())
        
        def loadArray(sz):
            arr = array.array('d')
            arr.fromfile(fin, sz)
            return arr
        
        return [loadArray(width) for x in range(length)]

#write the communities to a file
def writeNetworksBin(wfile, graph):
    """ file format is as follows
    first is the size in ASCII followed by newline
    next is the sequence of degrees in binary, 4 bytes per item
    next is the sequence of edges for each node.
    there are no record separators -- sizes are determines by degrees """
    with open(wfile, 'w') as fil:
        size = len(graph)
        degree_seq = array.array('i')
        for degree in graph:
            degree_seq.append(len(degree))
        
        fil.write(str(size) + "\n")
        degree_seq.tofile(fil)
        for line in graph:
            line.tofile(fil)

#read the binary.  Takes binary file name.
def readNetsBin(gFile):
    """ file format is as follows
    first is the size in ASCII followed by newline
    next is the sequence of degrees in binary, 4 bytes per item 
    next is the sequence of edges for each node, 
    there are no record separators -- sizes are determined by degrees """
    with open(gFile) as fin:
        size = int(fin.readline())
         
        def loadArray(sz):
            arr = array.array('i')
            arr.fromfile(fin, sz)
            return arr

        degree_seq = loadArray(size)
        return [loadArray(degree) for degree in degree_seq]

# makes sure a directory exists
def assureDir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

#main function
def main():
    socialGraph = readGraphBin("./test-binary/test-socialgraph.bin")
    networksAll = readNetsBin("./test-binary/test-networksAll.bin")
    networksTop = readNetsBin("./test-binary/test-networksTop.bin")
    meta = readMetaBin("./test-binary/test-metalist.bin")
    print "social", socialGraph
    print "networks all", networksAll
    print "networks top", networksTop
    print "meta data", meta
    

if __name__ == "__main__":
    main()
