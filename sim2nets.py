import sys
import convertBIN as cb
import SimFunc as sf

# function to run sim
def runSim(ident, thresh):
    social = cb.readGraphBin('./' + ident + '-binary/' + ident + '-socialgraph.bin')
    com = cb.readNetsBin('./' + ident + '-binary/' + ident + '-networksTop.bin')
    meta = cb.readMetaBin('./' + ident + '-binary/' + ident + '-metalist.bin')
    irank = cb.readMetaBin('./' + ident + '-binary/' + ident + '-irank.bin')
    trials = 0
    for pair in irank:
        if len(com[int(pair[1])]) < thresh or len(com[int(pair[2])]) < thresh:
            continue
        if trials > 10:
            break
        
        limit = 100
        sf.sim2coms([int(pair[1])], [int(pair[2])], 0.8, 0.8, 1, 1, 1, 1, ident, 'main' + str(trials), 100, social, com, meta, pair[0], limit)
        trials += 1
        
        

# main function
def main():
    for ident in sys.argv[1:]:
        runSim(ident, 1000)

if __name__ == "__main__":
   main()
