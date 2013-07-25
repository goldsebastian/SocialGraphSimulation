import array
#import numpy as np
from bitarray import bitarray
import random
import sys
import convertBIN as cb

# Takes the pointers to the bitarrays to be modified, and those to read
# And the list of ids, Connections, both merits, and both entry costs
def step(p1New, p1Old, p2New, p2Old, social, meta, m1, m2, e1, e2):
   for uid in range(len(social)):
      cum1 = 0
      cum2 = 0
      fcount = 0
      uthresh = meta[uid][0]
      for friendId in social[uid]:
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

# random seeding.  Takes 2 bitarrays and desired concentration
def seedRand(pa, pb, c):
   for x in range(len(pa)):
      pa[i] = (random.random() < c)
      pb[i] = pa[i]

# set seeding.  Takes bitarrays and desired id range to seed
def seedRange(pa, pb, rl, rh):
    for i in range(rl, rh):
        pa[i] = True
        pb[i] = True

# seed based on communities
def seedCom(coms, prob, pa, pb, comlist):
    for comid in coms:
        for uid in comlist[comid]:
            p = random.random() < prob
            pa[uid] = p
            pb[uid] = p

# set seed based on initial node friends, prob, and rounds
def seedLeader(user, graph, prob, pa, pb, rounds):
    joined = [user]
    for x in range(rounds):
        for node in joined:
            if (random.random() < prob) and not pa[node]:
                for friend in graph[node]:
                    pa[friend] = True
                    pb[friend] = True
                    joined.append[node]

# function to run 2 different network groups sim
def sim2coms(com1, com2, prob1, prob2, merit1, merit2, entry1, entry2, name, ident, stillthresh, socialgraph, com, meta, dist, limit):
    length = len(socialgraph)
    p1a = bitarray(length)
    p1a.setall(False)
    p2a = bitarray(length)
    p2a.setall(False)
    p1b = bitarray(length)
    p1b.setall(False)
    p2b = bitarray(length)
    p2b.setall(False)
    seedCom(com1, prob1, p1a, p1b, com)
    seedCom(com2, prob2, p2a, p2b, com)
    stillcount = 0
    p1o = 0
    p20 = 0
    i = 0
    cb.assureDir('./results/' + name + '/')
    fil = open('./results/' + name + '/' + ident + '-counts.txt', 'w')
    fil.write('simulation with networks ' + str(com1) + ' and ' + str(com2) + ';' + ' with sizes ' + str(len(com[com1[0]])) + ' and ' + str(len(com[com2[0]])) + '\n')
    fil.write('merit1 = ' + str(merit1) + '\n')
    fil.write('merit2 = ' + str(merit2) + '\n')
    fil.write('entry1 = ' + str(entry1) + '\n')
    fil.write('entry2 = ' + str(entry2) + '\n')
    fil.write('threshold to stop sim = ' + str(stillthresh) + '\n')
    fil.write('initial seeding density for first net = ' + str(prob1) + '\n')
    fil.write('initial seeding density for second net = ' + str(prob2) + '\n')
    fil.write('Pairwise intersection between communities = ' + str(dist) + '\n')
    while stillcount < 5:
        step(p1a, p1b, p2a, p2b, socialgraph, meta, merit1, merit2, entry1, entry2)
        fil.write(str(i) + ',' + str(p1a.count(True)) + ',' + str(p2a.count(True)) + '\n')
        i += 1
        if i > limit:
            break
        if (p1a.count(True) - p1o < stillthresh) and (p1o - p1a.count(True) < stillthresh) and (p2a.count(True) - p2o < stillthresh) and (p2o - p2a.count(True) < stillthresh):
            stillcount += 1
        else:
            p1o = p1a.count(True)
            p2o = p2a.count(True)
            stillcount = 0
        step(p1b, p1a, p2b, p2a, socialgraph, meta, merit1, merit2, entry1, entry2)
        fil.write(str(i) + ',' + str(p1b.count(True)) + ',' + str(p2b.count(True)) + '\n')
        i += 1
        if (p1b.count(True) - p1o < stillthresh) and (p1o - p1b.count(True) < stillthresh) and (p2b.count(True) - p2o < stillthresh) and (p1o - p2b.count(True) < stillthresh):
            stillcount += 1
        else:
            p1o = p1b.count(True)
            p2o = p2b.count(True)
            stillcount = 0
   

# function to set thresholds uniformly at random
def uniformRandomThresh(meta):
   for user in meta:
      user[0] = random.random()

# function to set thresholds all at same value
def uniformThresh(meta, thresh):
    for user in meta:
        user[0] = thresh

# main operating code
def main():
   #socialGraph, length, users, N = readGraph(sys.argv[1], int(sys.argv[2]))
   socialGraph = readGraphBin(sys.argv[1])
   length = len(socialGraph)
   N = length
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
   p1a[0] = True
   p1b[0] = True
   p2a[3] = True
   p2b[3] = True
   #seedRange(users, p1a, p1b, 1, 100000)
   #seedRange(users, p2a, p2b, 100000, 200000)
   # print initial values
   print p1a.count(True)/float(N), p2a.count(True)/float(N)
   print p1a.count(True), p2a.count(True)
   for i in range(0, int(sys.argv[2])/2):
   	  step(p1a, p1b, p2a, p2b, users, socialGraph, merit1, merit2, entry1, entry2)
   	  print p1a.count(True)/float(N), p2a.count(True)/float(N)
   	  #and again
   	  step(p1b, p1a, p2b, p2a, users, socialGraph, merit1, merit2, entry1, entry2)
   	  print p1b.count(True)/float(N), p2b.count(True)/float(N)

if __name__ == "__main__":
   main()
