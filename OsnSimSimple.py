import array
import numpy as np
from bitarray import bitarray
import random
import sys

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



# Takes the name of the file to be read.
# Returns an array, length of array (ID space size), and list of Ids
def readGraph(gFile, limit):
    graph = open(gFile, 'r')
    connections = []
    idList = []
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
          connections.append(array.array('I', []))
          
       connections.append(array.array('I', idi[2:]))
       if len(idi) > 2:
          idList.append([idi[0], 0])
          n += 1
       if (size % 10000) == 0:
          print connections[n][:6]
          print size
       size += 1
    return connections, size, idList, n

# Takes the pointers to the bitarrays to be modified, and those to read
# And the list of ids, Connections, both merits, and both entry costs
def step(p1New, p1Old, p2New, p2Old, idl, con, m1, m2, e1, e2):
   for node in idl:
      cum1 = 0
      cum2 = 0
      fcount = 0
      uid = node[0]
      uthresh = node[1]
      for friendId in con[uid]:
         cum1 += p1Old[friendId]
         cum2 += p2Old[friendId]
         fcount += 1
      
      # Try to vectorize all of this, if test proves successful.
      if not p1Old[uid] and not p2Old[uid]:
         update = [(m1*cum1/float(fcount) > uthresh), (m2*cum2/float(fcount) > uthresh)]
         if update[0] and update[1]:
            update[random.sample(xrange(2), 1)[0]] = False # don't add both
            
         p1New[uid] = update[0]
         p2New[uid] = update[1]
      elif not p1Old[uid] and p2Old[uid]:
         p1New[uid] = (m1*cum1/float(fcount) > uthresh*e1)
         p2New[uid] = True
      elif p1Old[uid] and not p2Old[uid]:
         p1New[uid] = True
         p2New[uid] = (m2*cum2/float(fcount) > uthresh*e2)
      elif p1Old[uid] and p2Old[uid]:
         update = [(m1*cum1/float(fcount) > uthresh*e1), (m2*cum2/float(fcount) > uthresh*e2)]
         if not update[0] and not update[1]:
            update[random.sample(xrange(2), 1)[0]] = True # don't drop both
            
         p1New[uid] = update[0]
         p2New[uid] = update[1]

def stepCum(p1New, p1Old, p2New, p2Old, idl, con, m1, m2, e1, e2):
   for node in idl:
      cum1 = 0
      cum2 = 0
      fcount = 0
      uid = node[0]
      uthresh = node[1]
      for friendId in con[uid]:
         cum1 += p1Old[friendId]
         cum2 += p2Old[friendId]
         fcount += 1

def stepUpdate(p1New, p1Old, p2New, p2Old, idl, con, m1, m2, e1, e2):
   for node in idl:
      cum1 = 0
      cum2 = 0
      fcount = 1
      uid = node[0]
      uthresh = node[1]
      
      # Try to vectorize all of this, if test proves successful.
      if not p1Old[uid] and not p2Old[uid]:
         update = [(m1*cum1/float(fcount) > uthresh), (m2*cum2/float(fcount) > uthresh)]
         if update[0] and update[1]:
            update[random.sample(xrange(2), 1)[0]] = False # don't add both
            
         p1New[uid] = update[0]
         p2New[uid] = update[1]
      elif not p1Old[uid] and p2Old[uid]:
         p1New[uid] = (m1*cum1/float(fcount) > uthresh*e1)
         p2New[uid] = True
      elif p1Old[uid] and not p2Old[uid]:
         p1New[uid] = True
         p2New[uid] = (m2*cum2/float(fcount) > uthresh*e2)
      elif p1Old[uid] and p2Old[uid]:
         update = [(m1*cum1/float(fcount) > uthresh*e1), (m2*cum2/float(fcount) > uthresh*e2)]
         if not update[0] and not update[1]:
            update[random.sample(xrange(2), 1)[0]] = True # don't drop both
            
         p1New[uid] = update[0]
         p2New[uid] = update[1]

# random seeding.  Takes user list, graph, bitarrays, desired concentration
def seedRand(idl, con, pa, pb, c, n):
   plist = random.sample(idl, int(c*n))
   for node in plist:
      pa[node[0]] = True
      pb[node[0]] = True

# set seeding.  Takes bitarrays, user list, and desired id range to seed
def seedRange(idl, pa, pb, rl, rh):
    for node in idl:
        if node[0] > rl and node[0] < rh:
            pa[node[0]] = True
            pb[node[0]] = True

# function to set thresholds uniformly at random
def uniformRandomThresh(idl):
   for user in idl:
      user[1] = random.random()

# function to set thresholds all at same value
def uniformThresh(idl, thresh):
    for user in idl:
        user[1] = thresh

# main operating code
def main():
   #socialGraph, length, users, N = readGraph(sys.argv[1], int(sys.argv[2]))
   socialGraph = readGraphBin("fbgraph.bin")
   length = len(socialGraph)
   N = length-1
   users = []
   for i in range(length):
   	  if len(socialGraph[i]) > 0:
   	  	 users.append([i, 0])
   	  	 
   merit1 = float(1)
   merit2 = float(2)
   entry1 = 1
   entry2 = 1
   # set the bitarrays
   p1a = bitarray(length)
   p1a.setall(False)
   p2a = bitarray(length)
   p2a.setall(False)
   p1b = bitarray(length)
   p1b.setall(False)
   p2b = bitarray(length)
   p2b.setall(False)
   # set up other parts
   uniformThresh(users, 0.3)   
   seedRange(users, p1a, p1b, 1, 100000)
   seedRange(users, p2a, p2b, 100000, 200000)
   # print initial values
   print p1a.count(True)/float(N), p2a.count(True)/float(N)
   print p1a.count(True), p2a.count(True)
   for i in range(0, int(sys.argv[1])/2):
   	  step(p1a, p1b, p2a, p2b, users, socialGraph, merit1, merit2, entry1, entry2)
   	  print p1a.count(True)/float(N), p2a.count(True)/float(N)
   	  #and again
   	  step(p1b, p1a, p2b, p2a, users, socialGraph, merit1, merit2, entry1, entry2)
   	  print p1b.count(True)/float(N), p2b.count(True)/float(N)

if __name__ == "__main__":
   main()
