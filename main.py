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
            parsed_args['n'] = int(args[i][3:])
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
    #lc(parsed_args['n'], parsed_args['i'], parsed_args['f'])
    functions = {"lc":lc,"add":add,"5p":fiveP,"lfsr":lfsr,"nfsr":nfsr,"mt":mt,"rc4":rc4,"rsa":rsa, "bbs":bbs}
    res = functions[parsed_args['g']](parsed_args['n'], parsed_args['i'])
    writeOutput( parsed_args['f'], res)
    #add(parsed_args['n'], parsed_args['i'], parsed_args['f'])
    print(f"g: {parsed_args['g']}")
    print(f"n: {parsed_args['n']}")
    print(f"f: {parsed_args['f']}")
    print(f"i: {parsed_args['i']}")

def writeOutput(f, res):
    with open(f, 'w') as f:
        f.write(" ".join(map(str, res)))

def lc(n,args):
    if len(args)!=4:
        print("Некорректное количество аргументов")
        return
    bar = IncrementalBar('Генерация:', max=int(n))
    m,a,c,x = args
    res = [x]
    for i in range(int(n)):
        x = (a * x + c) % m
        res.append(x)
        bar.next()
    bar.finish()
    return res

def add(n,args):
    if len(args)<4:
        print("Недостаточное количество аргументов")
        return
    elif args[1]>args[2] or args[1] < 1 or args[2] < 1:
        print("Должно выполняться условие j>k>=1")
        return
    elif len(args)-3<args[2]:
        print("Длина последовательности начальных значений должна быть >= старшему индексу")
        return
    bar = IncrementalBar('Генерация:', max=int(n))    
    xList = args
    m = xList.pop(0)
    k = xList.pop(0)
    j = xList.pop(0)
    for i in range(len(xList), int(n)+len(xList)):
        x = (xList[i-j]+xList[i-k]) % m
        xList.append(x)
        bar.next()
    bar.finish()
    return xList


def fiveP(n,args):
    if len(args)!=6:
        print("Некорректное количество аргументов")
        return
    print(args)
    p,q1,q2,q3,w,default = args
    bar = IncrementalBar('Генерация:', max=int(n))
    res = [default]
    default = str(default)
    while len(str(default)) < p:
        default = '0' + default
    counter = 0
    for _ in range(n):
        x_bin = ''
        for _ in range(w):
            x = int(default[counter + q1]) + int(default[counter +q2]) + int(default[counter + q3]) + int(default[counter])
            counter += 1
            x = x % 2
            default += str(x)
            x_bin += str(x)
        res.append(int(x_bin, 2))
        bar.next()
    bar.finish()
    return res

def lfsr(n,args):
    if len(args)!=2:
        print("Некорректное количество аргументов")
        return
    elif checkBinVector(str(args[0])):
        print("Вектор должен состоять только из 0 и 1")
        return
    a,default = args
    a=str(a)
    bar = IncrementalBar('Генерация:', max=int(n))
    res = [default]
    default = bin(default)[2:]
    lenDefault = len(default)
    while len(default) < len(a)+lenDefault:
        default = '0' + default
    counter = 0
    for _ in range(n):
        x_bin = ''
        for _ in range(len(a)+lenDefault):
            x=0
            for p in range(len(a)-1, 1, -1):
                x += int(a[p])+int(default[counter+p])
            #x = int(default[counter + q1]) + int(default[counter +q2]) + int(default[counter + q3]) + int(default[counter])
            counter += 1
            x = x % 2
            default += str(x)
            x_bin += str(x)
        res.append(int(x_bin, 2))
        bar.next()
    bar.finish()
    return res
def nfsr(n, args):
    if len(args)!=7:
        print("Некорректное количество аргументов")
        return
    elif checkBinVector(args[0]) or checkBinVector(args[1]) or checkBinVector(args[2]):
        print("Вектор должен состоять только из 0 и 1")
        return
    vec1,vec2,vec3,x1,x2,x3,w = args
    res1 = lfsr(n, [vec1,x1])
    res2 = lfsr(n, [vec2,x2])
    res3 = lfsr(n, [vec3,x3])
def mt():
    pass

def rc4():
    pass

def rsa():
    pass

def bbs():
    pass

def checkBinVector(vec):
    return any(char not in '01' for char in str(vec[0]))

if __name__ == '__main__':
    print(bin(13)[2:])
    main()
