from scipy.optimize import fsolve

def func(i):
    x1,x2, x3,x4,x5,x6 = i[0], i[1], i[2],i[3],i[4],i[5]
    return [
        -220*x1+ 220*x2 - 220*x3+ 220*x4 +0*x5 - 220*x6,
             0*x1 - 440*x2+ 440*x3+ 0*x4 +0*x5 +220*x6,
             - 220*x1+ 220*x2 - 220*x3+ 220*x4 +0*x5 - 220*x6,
             - 630*x1 - 850*x2 - 850*x3 - 1070*x4 +330*x5+ 110*x6,
        220*x1+ 0*x2 +220*x3 +0*x4 - 220*x5 +220*x6,
        x1+x2+x3+x4+x5+x6-1

    ]

r = fsolve(func,[0, 0, 0,0,0,0])
print(r)
