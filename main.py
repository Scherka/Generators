import argparse
import sys
import math
#обработка аргументов командной строки
def parse_args(args):
    parsed_args = {
        'd': "st",
        'f': 'rnd.dat',
        'p1': 0,
        'p2': 0,
        'p3': 0
    }
    i = 0
    while i < len(args):
        if args[i].startswith('/h'):
            print_usage()
        elif args[i].startswith('/d:') and args[i][3:]!="":
            parsed_args['d'] = args[i][3:]
        elif args[i].startswith('/f:') and args[i][3:]!="":
            parsed_args['f'] = args[i][3:]
        elif args[i].startswith('/p1:') and args[i][3:]!="":
            parsed_args['p1'] = float(args[i][4:])
        elif args[i].startswith('/p2:') and args[i][3:]!="":
            parsed_args['p2'] = int(args[i][4:])
        elif args[i].startswith('/p3:') and args[i][3:]!="":
            parsed_args['p3'] = int(args[i][4:])
        i += 1

    return parsed_args
def print_usage():
    print("/d - код распределения для преоборазования последовательности")
    print("/f - имя файла с входгой последовательностью")
    print("/p1 - 1-й параметр")
    print("/p2 - 2-й параметр")
    print("/p3 - 3-й параметр")

def writeOutput(f, res):
    with open(f, 'w') as f:
        f.write(" ".join(map(str, res)))

def readInput(f):
    try:
        res = []
        with open(f) as f:
            for line in f:
                for a in line.split():
                    res.append(int(a))
        return res
    except:
        print("Не удалось прочитать входной файл")
        return'Error'



def main():
    args = sys.argv[1:]
    parsed_args = parse_args(args)
    print(f"d: {parsed_args['d']}")
    print(f"f: {parsed_args['f']}")
    print(f"p1: {parsed_args['p1']}")
    print(f"p2: {parsed_args['p2']}")
    print(f"p3: {parsed_args['p3']}")
    functions = {"st":st,"tr":tr,"ex":ex,"nr":nr, "gm":gm, "ln":ln, "ls":ls, "bi":bi}
    if parsed_args['d']=="gm":
        res = functions[parsed_args['d']](parsed_args['p1'], parsed_args['p2'], parsed_args['p3'], readInput(parsed_args['f']))
    else:
        res = functions[parsed_args['d']](parsed_args['p1'], parsed_args['p2'], readInput(parsed_args['f']))
    if res != 'Error':
        writeOutput(f"distr-{parsed_args['d']}.dat", res)

def st(p1, p2, x):
    if x == 'Error':
        return x
    res = []
    left_border = 0
    right_border = len(x)
    for i in range(left_border, right_border):
        u = x[i] % 1024
        y = p2 * u + p1
        y = format(y, '.4f')
        res.append(y)
    return res

def tr(p1, p2, x):
    if x == 'Error':
        return x
    res = []
    left_border = 1
    right_border = len(x)
    for i in range(left_border, right_border):
        u1 = x[i - 1] % 1024
        u2 = x[i] % 1024
        y = p1 + p2 * (u1 + u2 - 1)
        y = format(y, '.4f')
        res.append(y)
    return res

def ex(p1, p2, x):
    if x == 'Error':
        return x
    res = []
    left_border = 0
    right_border = len(x)
    for i in range(left_border, right_border):
        u = x[i] % 1024
        y = math.log1p(u) * (-p2) + p1
        y = format(y, '.4f')
        res.append(y)
    return res

def nr(p1, p2, x):
    if x == 'Error':
        return x
    res = []
    left_border = 0
    right_border = len(x)
    step = 2
    for i in range(left_border, right_border, step):
        u1 = x[i] % 1024
        u2 = x[i + 1] % 1024
        z1 = p1 + p2 * math.sqrt(math.fabs((-2) * math.log1p(math.fabs(1 - u1)))) * math.cos(2 * math.pi * u2)
        z2 = p1 + p2 * math.sqrt(math.fabs((-2) * math.log1p(math.fabs(1 - u1)))) * math.sin(2 * math.pi * u2)
        z1 = format(z1, '.4f')
        z2 = format(z2, '.4f')
        res.append(z1)
        res.append(z2)
    return res

def gm(p1, p2, p3, x):
    if x == 'Error':
        return x
    res = []
    left_border = 1
    right_border = len(x)
    for i in range(left_border, right_border):
        u = []
        for j in range(p3):
            u.append(x[i - j] % 1024)
        u_mult = 1
        for j in range(len(u)):
            u_mult = u_mult * (1 - u[j])
        y = p1 - p2 * math.log1p(math.fabs(u_mult))
        y = format(y, '.4f')
        res.append(y)
    return res

def ln(p1, p2, x):
    if x == 'Error':
        return x
    res = []
    left_border = 0
    right_border = len(x)
    for i in range(left_border, right_border):
        u = x[i] % 1024
        y = math.exp(p2 - u) + p1
        y = format(y, '.4f')
        res.append(y)
    return res

def ls(p1, p2, x):
    if x == 'Error':
        return x
    res = []
    left_border = 0
    right_border = len(x)
    for i in range(left_border, right_border):
        u = x[i] % 1024
        y = p1 + p2 * math.log1p(math.fabs(u / (1 - u)))
        y = format(y, '.4f')
        res.append(y)
    return res

def bi(p1, p2, x):
    res = []
    left_border = 0
    right_border = len(x)
    for i in range(left_border, right_border):
        u = x[i] / 1024
        y = 0
        s = 0
        k = 0
        while (True):
            s = s + (math.factorial(p2) / (math.factorial(k) * math.factorial(p2 - k))) * (p1 ** k) * ((1 - p1) ** (p2 - k))
            if s > u:
                y = k
                break
            if k < p2 - 1:
                k = k + 1
                continue
            y = p2
            break
        res.append(y)
    return res

if __name__ == '__main__':
    main()