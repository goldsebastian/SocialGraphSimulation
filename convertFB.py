import array
import sys
import convertBIN as cb

# Takes the name of the file to be read and the max ID
# Returns the socialGraph (list of arrays), meta graph (list of arrays)
def readGraph(gFile, limit):
    graph = open(gFile, 'r')
    social = []
    meta = []
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
        if len(idi) > 2:
            meta.append(array.array('i', [idi[0], 0]))
        """if (size % 10000) == 0:
            print social[n][:6]
            print size"""
        if (size % 100) == 0:
            sys.stderr.write("\r current size: %d" % size)
        size += 1
        
    return social, size

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

#main function
def main():
    #networksOrig = readNets("mhrw-nodeproperties.txt")
    #print networksOrig
    
    limit = 957359    
    socialGraphOrig, idSpace = readGraph("mhrw-socialgraph.txt", limit)
    idMap = cb.getMap(socialGraphOrig)
    socialGraph = cb.reIndexSocial(socialGraphOrig, idMap)
    metaList = cb.genMeta(len(socialGraph))
    networksOrig = readNets("mhrw-nodeproperties.txt")
    networks = cb.reIndexNets(networksOrig, idMap)
    subdir = "./facebook-mhrw-binary/"
    prefix = subdir + "fbmh-"
    cb.assureDir(subdir)
    cb.writeGraphBin(prefix + "socialgraphOriginal.bin", socialGraph)
    cb.writeGraphBin(prefix + "socialgraph.bin", socialGraph)
    cb.writeMetaBin(prefix + "metalist.bin", metaList)
    cb.writeIdMapBin(prefix + "idmap.bin", idMap)
    cb.writeNetworksBin(prefix + "networks.bin", networks)


if __name__ == "__main__":
    main()
