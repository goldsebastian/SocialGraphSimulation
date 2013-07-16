import convertSNAP as cs
import sys

#main function
def main():
    identifiers = sys.argv[1:]
    for name in identifiers:
        cs.convertSnap(name, -1)


if __name__ == "__main__":
    main()
