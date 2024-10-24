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
        if args[i].startswith('/h'):
            print_usage()
        elif args[i].startswith('/g:') and args[i][3:]!="":
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
    print(f"g: {parsed_args['g']}")
    print(f"n: {parsed_args['n']}")
    print(f"f: {parsed_args['f']}")
    print(f"i: {parsed_args['i']}")
    functions = {"lc":lc,"add":add,"5p":fiveP,"lfsr":lfsr,"nfsr":nfsr,"mt":mt,"rc4":rc4,"rsa":rsa, "bbs":bbs}
    res = functions[parsed_args['g']](parsed_args['n'], parsed_args['i'])
    if res != 'Error':
        writeOutput( parsed_args['f'], res)

def print_usage():
    print("/g - метод генерации ПСЧ")
    print("/n - количество генерируемых ПСЧ")
    print("/f - файл вывода")
    print("/i - парметры генератора")
def writeOutput(f, res):
    with open(f, 'w') as f:
        f.write(" ".join(map(str, res)))

def lc(n,args):
    if len(args)!=4:
        print("Некорректное количество аргументов")
        return 'Error'
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
        return 'Error'
    elif args[1]>args[2] or args[1] < 1 or args[2] < 1:
        print("Должно выполняться условие j>k>=1")
        return 'Error'
    elif len(args)-3<args[2]:
        print("Длина последовательности начальных значений должна быть >= старшему индексу")
        return 'Error'
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
    if len(args)!=5:
        print("Некорректное количество аргументов")
        return 'Error'
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
        return 'Error'
    elif checkBinVector(str(args[0])):
        print("Вектор должен состоять только из 0 и 1")
        return 'Error'
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
        return 'Error'
    elif checkBinVector(str(args[0])) or checkBinVector(str(args[1])) or checkBinVector(str(args[2])):
        print("Вектор должен состоять только из 0 и 1")
        return 'Error'
    bar = IncrementalBar('Генерация:', max=int(n))
    res=[]
    vec1,vec2,vec3,x1,x2,x3,w = args
    res1 = lfsr(n, [vec1,x1])
    res2 = lfsr(n, [vec2,x2])
    res3 = lfsr(n, [vec3,x3])
    for i in range(n):
        x1,x2,x3 = res1[i],res2[i],res3[i]
        resultTemp = (x1 & x2) ^ (x2 &x3) ^ x3
        res.append(resultTemp)
        bar.next()
    bar.finish()
    return res

def mt(n, args):
    if len(args) < 1:
        p = 624
    else:
        p = args.pop(0)
    if len(args) < p:
        x = [5, 28, 14, 27, 18, 17, 23, 1, 24, 17, 5, 11, 1,
            1, 19, 13, 21, 7, 2, 11, 8, 23, 21, 15, 24, 4, 7, 11, 29, 7, 24,
            15, 13, 9, 26, 3, 12, 9, 8, 17, 2, 2, 28, 6, 30, 14, 29, 21, 13,
            1, 27, 9, 18, 26, 8, 14, 22, 15, 9, 7, 21, 10, 12, 6, 23, 17,
            13, 18, 3, 29, 29, 17, 5, 14, 18, 18, 17, 12, 5, 3, 18, 26, 29,
            29, 7, 17, 1, 23, 16, 9, 26, 28, 4, 21, 6, 30, 29, 15, 14, 26,
            24, 30, 23, 26, 22, 22, 26, 9, 2, 16, 11, 16, 30, 3, 7, 30, 8,
            11, 9, 10, 25, 12, 1, 22, 11, 5, 22, 12, 24, 18, 17, 6, 10, 15,
            21, 24, 26, 12, 13, 4, 19, 26, 26, 22, 15, 10, 1, 18, 25, 28, 1,
            24, 18, 27, 3, 5, 15, 27, 21, 17, 5, 29, 16, 28, 30, 10, 26, 6,
            22, 6, 4, 4, 8, 5, 2, 4, 17, 22, 5, 12, 15, 11, 8, 7, 5, 5, 8,
            18, 23, 28, 19, 2, 18, 6, 2, 3, 9, 17, 9, 4, 29, 6, 29, 17, 25,
            11, 18, 28, 12, 6, 13, 8, 14, 14, 7, 13, 9, 22, 28, 20, 30, 3,
            8, 1, 28, 10, 28, 7, 12, 26, 14, 27, 18, 30, 7, 18, 2, 30, 13,
            12, 11, 17, 9, 24, 23, 10, 18, 4, 15, 29, 3, 19, 15, 24, 13, 15,
            7, 12, 3, 7, 21, 17, 24, 3, 14, 22, 9, 29, 2, 7, 27, 29, 18, 26,
            4, 12, 6, 25, 21, 8, 20, 11, 10, 23, 8, 4, 26, 28, 12, 19, 11,
            13, 1, 3, 22, 12, 16, 11, 6, 26, 28, 17, 25, 29, 5, 12, 27, 25,
            11, 7, 13, 5, 27, 12, 19, 25, 11, 5, 3, 5, 9, 26, 28, 25, 18,
            18, 22, 16, 17, 29, 2, 20, 2, 7, 2, 26, 29, 6, 6, 23, 8, 20, 6,
            26, 24, 28, 22, 15, 7, 28, 26, 7, 24, 21, 28, 16, 27, 8, 2, 3,
            19, 23, 6, 20, 19, 27, 16, 16, 1, 20, 10, 8, 8, 8, 28, 21, 8,
            11, 4, 13, 29, 29, 8, 24, 22, 3, 2, 26, 13, 19, 8, 17, 25, 6, 2,
            7, 4, 20, 24, 26, 2, 23, 9, 15, 22, 19, 20, 24, 29, 2, 29, 24,
            3, 28, 30, 2, 22, 28, 21, 28, 9, 12, 30, 18, 13, 2, 9, 17, 20,
            10, 24, 30, 20, 23, 6, 30, 21, 8, 26, 13, 30, 9, 30, 1, 14, 19,
            16, 6, 18, 9, 15, 1, 27, 4, 12, 4, 26, 6, 24, 19, 24, 4, 15, 6,
            13, 10, 24, 2, 29, 5, 12, 24, 14, 24, 11, 1, 23, 24, 12, 2, 2,
            18, 27, 30, 11, 26, 28, 20, 20, 8, 11, 23, 4, 26, 19, 17, 21,
            11, 29, 11, 30, 2, 9, 12, 17, 18, 18, 13, 14, 12, 19, 20, 7, 15,
            2, 17, 15, 26, 12, 24, 22, 3, 4, 22, 16, 9, 12, 16, 13, 30, 14,
            24, 1, 10, 21, 16, 6, 1, 30, 27, 19, 25, 27, 7, 12, 17, 24, 29,
            12, 20, 4, 21, 12, 16, 13, 21, 23, 29, 2, 29, 21, 12, 13, 23,
            12, 22, 16, 12, 19, 22, 6, 20, 11, 28, 16, 7, 26, 14, 17, 17, 4,
            22, 29, 6, 27, 14, 16, 28, 18, 11, 25, 2, 13, 27, 14, 23, 27,
            14, 30, 21, 6, 6, 4, 12, 15, 17, 27, 3, 6, 5, 2, 19, 9, 12, 24,
            20, 11, 21, 13, 8, 26, 16, 18, 1]
    else:
        x = args
    bar = IncrementalBar('Генерация:', max=int(n))
    w = 32
    r = 31
    q = 397
    a = 2567483615
    u = 11
    s = 7
    t = 15
    l = 18
    b = 2636928640
    c = 4022730752
    res = []
    value1 = ''
    value2 = ''
    
    for i in range(w - r):
        value1 += '1'
        value2 += '0'
    for i in range(r):
        value1 += '0'
        value2 += '1'
    value1Int = int(value1, 2)
    value2Int = int(value2, 2)
    for i in range(n + 1500):
        t12 = int(x[i]) & value1Int
        t13 = int((x[i + 1])) & value2Int
        Y = t12 | t13
        if (Y % 2 != 0):
            valuex = (int(x[i + q]) % 2 ** w) ^ (Y >> 1) ^ a
        else:
            valuex = (int(x[i + q]) % 2 ** w) ^ (Y >> 1) ^ 0
        Y = valuex
        Y = (Y ^ (Y >> u))
        Y = Y ^ ((Y << s) & b)
        Y = Y ^ ((Y << t) & c)
        Z = (Y ^ (Y >> l))
        x.append(valuex)
        res.append(Z % p)
        bar.next()
    bar.finish()
    return res

def rc4(n, args):
    if len(args)!=256:
        x = [73,25,169,67,200,69,83,93,19,100,141,85,207,66,71,236,194,239,167,
            32,101,135,213,35,89,112,188,178,82,33,206,54,249,51,255,102,164,155,133,46,
            16,231,152,42,122,15,41,14,208,244,230,6,8,245,217,124,227,185,184,248,37,59,
            31,191,120,111,26,253,140,63,125,242,3,136,27,36,186,95,220,94,243,49,70,15,
            0,79,118,117,176,172,247,24,65,241,238,174,55,114,21,2,129,162,17,210,254,22,
            60,62,251,91,215,0,109,223,156,97,11,127,123,130,250,192,1,138,52,113,160,1,
            81,229,105,47,44,40,180,116,168,153,154,201,72,234,128,224,5,161,197,134,13,
            2,190,177,29,56,12,77,50,58,74,131,146,246,68,166,96,216,219,212,13,115,211,
            157,144,203,20,232,9,45,34,23,151,195,237,196,80,57,7,205,43,182,193,106,87,
            104,119,38,218,148,48,187,221,226,159,145,202,110,228,173,209,10,108,75,84,
            139,53,61,18,103,183,98,179,165,81,126,137,171,170,252,147,78,214,163,158,2,
            33,149,142,175,121,76,90,4,92,199,30,107,88,99,189,222,225,143,235,39,240,20,
            4,28,86,198]
    else:
        x = args
    bar = IncrementalBar('Выполнение:', max=n)
    res = []
    length = 256
    sBox = [0] * length
    key = [0] * length
    for i in range(length):
        sBox[i] = i
    for i in range(length):
        key[i] = int(x[i % len(x)])
    j = 0
    for i in range(length):
        j = (j + sBox[i] + key[i]) % length
        sBox[i], sBox[j] = sBox[j], sBox[i]
    j = 0
    for i in range(n, 0, -1):
        i = (i + 1) % length
        j = (j + sBox[i]) % length
        sBox[i], sBox[j] = sBox[j], sBox[i]
        t = (sBox[i] + sBox[j]) % length
        res.append(sBox[t])
        bar.next()
    bar.finish()
    return res

def rsa(n_, args):
    if len(args)!=5:
        print("Некорректное количество аргументов")
        return 'Error'
    p, q, e, x, l = int(args[0]), int(args[1]), int(args[2]), int(args[3]), int(args[4])
    res = []
    bar = IncrementalBar('Выполнение:', max=n_)
    n = p * q
    for i in range(n_):
        counter = l - 1
        seqElem = 0
        for j in range(l):
            x = x ** e % n
            bit = x & 1
            seqElem = seqElem | (bit << counter)
            counter -= 1
        res.append(seqElem)
        bar.next()
    bar.finish()
    return res

def bbs(n_, args):
    if len(args)!=1:
        print("Некорректное количество аргументов")
        return 'Error'
    x = int(args[0])
    bar = IncrementalBar('Выполнение:', max=n_)
    res = []
    n, w = 50621, 10
    for i in range(n_):
        x_bin = ''
        for j in range(w):
            x = (x * x) % n
            x_bin += str(x % 2)
        res.append(int(x_bin, 2))
        bar.next()
    bar.finish()
    return res

def checkBinVector(vec):
    return any(char not in '01' for char in str(vec[0]))

if __name__ == '__main__':
    main()
