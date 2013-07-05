import array
import sys

#read the binary.  Takes binary file name.
def readGraphBin(gFile):
    """ file format is as follows
    first is the size in ASCII followed by newline
    next is the length of the metadata array, then newline
    next is the width of the metadata array, then newline
    next is the metadata array, all integers, 4 bytes per item
    next is the sequence of degrees in binary, 4 bytes per item
    next is the sequence of edges for each node.
    there are no record separators -- sizes are determines by degrees """
    with open(gFile) as fin:
        size = int(fin.readline())
        length = int(fin.readline())
        width = int(fin.readline())
        
        def loadArray(sz):
            arr = array.array('I')
            arr.fromfile(fin, sz)
            return arr
            
        degree_seq = loadArray(size)
        return [loadArray(width) for x in range(length)], [loadArray(degree) for degree in degree_seq]
        
# write the connections graph to a file
def writeGraphBin(wFile, graph, meta):
    """ file format is as follows
    first is the size in ASCII followed by newline
    next is the length of the metadata array, then newline
    next is the width of the metadata array, then newline
    next is the metadata array, all integers, 4 bytes per item
    next is the sequence of degrees in binary, 4 bytes per item
    next is the sequence of edges for each node.
    there are no record separators -- sizes are determines by degrees """
    with open(wFile, 'w') as fil:
        size = len(graph)
        length = len(meta)
        width = len(meta[0])
        degree_seq = array.array('I')
        for degree in graph:
            degree_seq.append(len(degree))
        
        fil.write(str(size) + "\n")
        fil.write(str(length) + "\n")
        fil.srite(str(width) + "\n")
        for line in meta:
            line.tofile(fil)
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
    n = 0
    print limit
    for line in graph:
        ids = line.split()
        idi = []
        for id_string in ids:
            iTemp = int(id_string)
            if iTemp <= limit:
                idi.append(iTemp)
       
        while idi[0] > size:
            size += 1
            social.append(array.array('I', []))
          
        social.append(array.array('I', idi[2:]))
        if len(idi) > 2:
            meta.append(array.array('I', [idi[0], 0]))
            n += 1
        if (size % 10000) == 0:
            print social[n][:6]
            print size
        size += 1
    return social, meta

#main function
def main():
    socialGraph, metaList = readGraph("mhrw-socialgraph.txt", 957359)
    writeGraphBin("fbgraphComplete.bin", socialGraph, metaList)


if __name__ == "__main__":
    main()
