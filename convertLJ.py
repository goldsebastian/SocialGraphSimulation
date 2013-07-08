import array
import sys
import random
import os
import convertSNAP as cs

#main function
def main():
    socialGraph, idSpace = cs.readGraph("lj-undirgraph.txt", -1)
    metaList = cs.getMeta(socialGraph, idSpace)
    #writeGraphBin("testSocial.bin", socialGraph)
    networks = cs.readNet("lj-communities.txt")
    cs.assureDir("./liveJournal/lj-socialgraph.bin")
    cs.writeGraphBin("./liveJournal/lj-socialgraph.bin", socialGraph)
    cs.assureDir("./liveJournal/lj-metalist.bin")
    cs.writeMetaBin("./liveJournal/lj-metalist.bin", metaList)
    cs.assureDir("./liveJournal/lj-networks.bin")
    cs.writeNetworksBin("./liveJournal/lj-networks.bin", networks)


if __name__ == "__main__":
    main()
