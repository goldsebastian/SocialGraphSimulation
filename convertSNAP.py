import array
import sys
import random
import os
import convertBIN as cb

# Takes the name of the file to be read and the max ID
# Returns the socialGraph (list of arrays), meta graph (list of arrays)
def readGraph(gFile, sizemil):
    graph = open(gFile, 'r')
    social = []
    size = 0
    done1 = False
    print "progress shown below, out of about", sizemil, "million ids"
    for line in graph:
        if line[0] == '#': continue
        ids = line.split()
        idi = [int(ids[0]), int(ids[1])]
       
        while (idi[0] >= size) or (idi[1] >= size):
            size += 1
            social.append(array.array('i', []))
          
        social[idi[0]].append(idi[1])
        social[idi[1]].append(idi[0])
                
        if (idi[0] % 100) == 0:
            #print size, idi[0], "array good?", social[idi[0]][:6]
            sys.stderr.write("\r current size: %d  current id: %d" % (size, idi[0]))    # or print >> sys.stdout, "\r%d%%" %i,
            #sys.stderr.flush()
           
    #meta.sort()
    return social, size 

# reads networks and stores them in a ragged array.  Assumed network ID's are the line in the array in which they occur.
def readNets(nFile):
    graph = open(nFile, 'r')
    nets = []
    for line in graph:
        if line[0] == '#': continue
        ids = line.split()
        idi = [int(numeric_string) for numeric_string in ids]
        nets.append(array.array('i', idi))
    
    return nets

# Converts the desired dataset.  Takes unique ident(ifier), which is used for subdir and prefix, and approximate size in millions
def convertSnap(ident, size):
    print "converting data for", ident
    socialGraphOrig, idSpace = readGraph("com-" + ident + ".ungraph.txt", size)
    idMap = cb.getMap(socialGraphOrig)
    socialGraph = cb.reIndexSocial(socialGraphOrig, idMap)
    metaList = cb.genMeta(len(socialGraph))
    print "\n  now reading networks all"
    networksAllOrig = readNets("com-" + ident + ".all.cmty.txt")
    networksAll = cb.reIndexNets(networksAllOrig, idMap)
    print "  now reading networks top 5000"
    networksTopOrig = readNets("com-" + ident + ".top5000.cmty.txt")
    networksTop = cb.reIndexNets(networksTopOrig, idMap)
    print "  now writing all to binary"
    subdir = "./" + ident + "-binary/"
    cb.assureDir(subdir)
    cb.writeGraphBin(subdir + ident + "-socialgraph.bin", socialGraph)
    cb.writeMetaBin(subdir + ident + "-metalist.bin", metaList)
    cb.writeIdMapBin(subdir + ident + "-idmap.bin", idMap)
    cb.writeNetworksBin(subdir + ident + "-networksAll.bin", networksAll)
    cb.writeNetworksBin(subdir + ident + "-networksTop.bin", networksTop)

#main function
def main():
    convertSnap("test", 0)
    

if __name__ == "__main__":
    main()
