import array
import sys
import convertBIN as cb

# Takes the name of the file to be read and the max ID
# Returns the socialGraph (list of arrays), meta graph (list of arrays)
def readGraph(gFile, limit):
    graph = open(gFile, 'r')
    social = []
    size = 0
    print limit
    for line in graph:
        ids = line.split()
        idi = [int(numeric_string) for numeric_string in ids]
        if idi[0] > limit:
            print "Something went horribly wrong with limit", idi[0]
        
        friendList = array.array('i')
        for friend in idi[2:]:
            if friend <= limit:
                friendList.append(friend)
       
        while idi[0] > size:
            size += 1
            social.append(array.array('i', []))
          
        social.append(friendList)
        if (size % 100) == 0:
            sys.stderr.write("\r current size: %d" % size)
        size += 1
        
    return social

# takes the name of the file containing metadata, as well as the number of net idSpace, and returns networks
def readNets(mFile):
    meta = open(mFile, 'r')
    nets = []
    size = 0    
    for line in meta:
        properties = line.split()[0].split('#')
        netstring = properties[4].split('|')
        if netstring[0] != "":
            #print properties[0]
            #sys.stdout.write(netstring[0])
            #print len(netstring[0])
            netlist = [int(numeric_string) for numeric_string in netstring]
            for net in netlist:
                while net >= size:
                    nets.append(array.array('i'))
                    size += 1
                nets[net].append(int(properties[0]))
                
    return nets

def testBin(arw):
    with open('lt.bin', 'w') as fiw:
        arw.tofile(fiw)
    
    arr = array.array(arw.typecode)
    with open('lt.bin', 'r') as fir:
        arr.fromfile(fir, len(arw))
    
    return arr

#main function
def main():
    #networksOrig = readNets("mhrw-nodeproperties.txt")
    #print networksOrig
    
    limit = 957359    
    socialGraphOrig = readGraph("mhrw-socialgraph.txt", limit)
    idMap = cb.getMap(socialGraphOrig)
    socialGraph = cb.reIndexSocial(socialGraphOrig, idMap)
    metaList = cb.genMeta(len(socialGraph))
    networksOrig = readNets("mhrw-nodeproperties.txt")
    networks = cb.reIndexNets(networksOrig, idMap)
    subdir = "./fbmh-binary/"
    prefix = subdir + "fbmh-"
    cb.assureDir(subdir)
    cb.writeGraphBin(prefix + "socialgraph.bin", socialGraph)
    cb.writeMetaBin(prefix + "metalist.bin", metaList)
    cb.writeIdMapBin(prefix + "idmap.bin", idMap)
    cb.writeNetworksBin(prefix + "networksTop.bin", networks)


if __name__ == "__main__":
    main()
