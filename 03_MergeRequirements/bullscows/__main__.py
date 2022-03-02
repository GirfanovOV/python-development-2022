import sys
import os 
from .bullscows import gameplay, ask, inform
import urllib.request

if __name__ == '__main__' :
    words = []
    if os.path.exists(sys.argv[1]) and os.path.isfile(sys.argv[1]):
        
        with open(sys.argv[1]) as f :
            for line in f :
                if len(line[:-1]) == int(sys.argv[2]) :
                    words.append(line[:-1])
    else :
        urllib.request.urlretrieve(sys.argv[1], "tmp.txt")
        with open('tmp.txt') as f :
            for line in f :
                if len(line[:-1]) == int(sys.argv[2]) :
                    words.append(line[:-1])
        os.remove('tmp.txt')

    print(gameplay(ask, inform, words))