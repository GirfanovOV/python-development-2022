from inspect import getmembers, isclass, isfunction, getsource
from ast import parse, unparse, walk
from textwrap import dedent
from difflib import SequenceMatcher
from importlib import __import__
import sys

def make_list(obj, c : list) :
    mems = getmembers(obj)
    for mem in mems :
        if isclass(mem[1]) and not mem[0].startswith('__') :
            make_list(mem[1], c)
        if isfunction(mem[1]) : 
            source = parse(dedent(getsource(mem[1])))
            
            for inst in walk(source) :
                if hasattr(inst, 'id') :
                    setattr(inst, 'id', '_')
                if hasattr(inst, 'name') :
                    setattr(inst, 'name', '_')
                if hasattr(inst, 'arg') :
                    setattr(inst, 'arg', '_')
                if hasattr(inst, 'attr') :
                    setattr(inst, 'attr', '_')

            # c.append((mem[1].__qualname__, unparse(source)))
            name = mem[1].__qualname__
            name = mem[1].__module__ + '.' + '.'.join(name.split('.')[:-1])
            if name[-1] != '.' :
                name += '.'
            name += mem[0]
            c.append(( name, unparse(source) ))

c = []
res = []

m = __import__(sys.argv[1])

make_list(m, c)

if len(sys.argv) > 2 :
    m = __import__(sys.argv[2])
    make_list(m, c)


for i in range(len(c) - 1) :
    for j in range(i+1, len(c)) :
        curr = tuple(sorted([c[i][0], c[j][0]]))
        # if max(SequenceMatcher(None, c[i][1], c[j][1]).ratio(), SequenceMatcher(None, c[j][1], c[i][1]).ratio()) > .95 :
        if SequenceMatcher(None, c[i][1], c[j][1]).ratio() > .95 :
            res.append(curr)


for r in res :
    print(r[0], r[1])