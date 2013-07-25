import array, sys, random, os, pickle
import convertBIN as cb

# Function to calculate community pairwise intersection. c is the number of communities.
# Takes the communities listed by user.
# returns a 2 dimensional list with the value of list[i][j] being the intersection of communities i and j
def intersectionCalc(com, ucom):
    n = len(ucom)
    c = len(com)
    overlap = [array.array('d', [0 for x in xrange(c)]) for x in xrange(c)]
    for ucl in ucom:
        for i in range(len(ucl)):
            for j in range(len(ucl)):
                overlap[ucl[i]][ucl[j]] += 1
                
    for i in range(c):
        for j in range(c):
            overlap[i][j] = (float)(overlap[i][j])/(len(com[i]) + len(com[j]) - overlap[i][j])
    
    return overlap

# takes a grid of intersection scores and ranks them.
# returns a list in ascending order of ordered tuples(score, com 1, com 2)
def intersectionRank(overlap):
    c = len(overlap)
    rank = []
    for i in range(c):
        for j in range(c):
            rank.append(array.array('d', [overlap[i][j], i, j]))
    
    ranksort = sorted(rank, key=lambda arr: arr[0])
    return ranksort

# takes a list of communities and returns a list of nets by user, not com.
def comByUser(com, n):
    ucom = [array.array('i') for x in xrange(n)]
    for i in range(len(com)):
        clist = com[i]
        for cid in clist:
            ucom[cid].append(i)
    
    return ucom

# main function runs both of these and dumps them for all identifiers
def main():
    for ident in sys.argv[1:]:
        social = cb.readGraphBin('./' + ident + '-binary/' + ident + '-socialgraph.bin')
        com = cb.readNetsBin('./' + ident + '-binary/' + ident + '-networksTop.bin')
        ucom = comByUser(com, len(social))
        igrid = intersectionCalc(com, ucom)
        irank = intersectionRank(igrid)
        cb.writeGraphBin('./' + ident + '-binary/' + ident + '-ucom.bin', ucom)
        cb.writeMetaBin('./' + ident + '-binary/' + ident + '-igrid.bin', igrid)
        cb.writeMetaBin('./' + ident + '-binary/' + ident + '-irank.bin', irank)

if __name__ == "__main__":
   main()
