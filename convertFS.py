import array
import sys
import os
import convertSNAP as cs
import convertBIN as cb

#main function
def main():
    socialGraphOrig, idSpace = cs.readGraph("friendster-undirgraph.txt", 115)
    idMap = cb.getMap(socialGraphOrig)
    socialGraph = cb.reIndexSocial(socialGraphOrig, idMap)
    metaList = cb.genMeta(len(socialGraph))
    #networks = cs.readNet("friendster-communities.txt")
    subdir = "./friendster/"
    prefix = subdir + "fs-"
    cb.assureDir(subdir)
    cb.writeGraphBin(prefix + "socialgraph.bin", socialGraph)
    cb.writeMetaBin(prefix + "metalist.bin", metaList)
    cb.writeIdMapBin(prefix + "idmap.bin", idMap)
    #cb.writeNetworksBin(prefix + "networks.bin", networks)


if __name__ == "__main__":
    main()
