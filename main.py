import argparse
import sys
from progress.bar import IncrementalBar
#обработка аргументов командной строки
def parse_args(args):
    parsed_args = {
        'g': "lc",
        'n': 10000,
        'f': 'rnd.dat',
        'i': []
    }


    i = 0
    while i < len(args):
        if args[i].startswith('/g:') and args[i][3:]!="":
            parsed_args['g'] = args[i][3:]
        elif args[i].startswith('/n:') and args[i][3:]!="":
            parsed_args['n'] = args[i][3:]
        elif args[i].startswith('/f:') and args[i][3:]!="":
            parsed_args['f'] = args[i][3:]
        elif args[i].startswith('/i:') and args[i][3:]!="":
            items = args[i][3:].split(',')
            parsed_args['i'].extend([int(i) for i in items])
        i += 1

    return parsed_args

def main():
    args = sys.argv[1:]
    parsed_args = parse_args(args)
    lc(parsed_args['n'], parsed_args['i'], parsed_args['f'])
    print(f"g: {parsed_args['g']}")
    print(f"n: {parsed_args['n']}")
    print(f"f: {parsed_args['f']}")
    print(f"i: {parsed_args['i']}")
def writeOutput(f, res):
    with open(f, 'w') as f:
        f.write(" ".join(map(str, res)))
def lc(n,args,f):
    if len(args)<4:
        print("Недостаточное количество аргументов")
        return
    bar = IncrementalBar('Генерация:', max=int(n))
    res =[]
    m,a,c,x = args
    for i in range(int(n)):
        x = (a * x + c) % m
        res.append(x)
        bar.next()
    bar.finish()
    writeOutput(f, res)

def add():
    pass

def fiveP():
    pass

def lfsr():
    pass

def nfsr():
    pass

def mt():
    pass

def rc4():
    pass

def rsa():
    pass

def bbs():
    pass

if __name__ == '__main__':
    main()
