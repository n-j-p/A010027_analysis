### Exploration of A010027:

from scipy.special import comb
binom = lambda a,b: comb(a,b,exact=True)
from math import factorial
from fractions import Fraction
import itertools as it
from collections import Counter

def get_subs(sequence):
    starts = []
    lens = []
    insub = False
    for i,x in enumerate(sequence[1:],start=0):
        if x-sequence[i]==1:
            if not insub:
                insub = True
                starts.append(i)
                lens.append(2)
            else:
                lens[-1] += 1
        else:
            insub = False
    return starts, lens

def split(sequence, starts, lens):
    sp = []
    ix = 0
    while ix < len(sequence):
        if ix in starts:
            L = lens[starts.index(ix)]
            sp.append(tuple(sequence[ix:ix+L]))
            ix += L
        else:
            sp.append((sequence[ix],))
            ix += 1
    return sp

def splitit(sequence):
    return split(sequence, *get_subs(sequence))


def UBF_alt(n,k):
    ctot = 0 
    for perm in it.permutations(range(1,n+1)):
        if len(splitit(perm)) == k:
            ctot += 1
    return ctot
def UBF_alt_generator():
    for n in it.count(1):
        ct = Counter()
        ct.update([len(splitit(perm)) for perm in it.permutations(range(1,n+1))])
        yield [x[1] for x in sorted(ct.items())]

def UBF(n,k):
    assert k >= 0
    assert k < n
    assert n >= 1

    ctot = 0 
    for perm in it.permutations(range(1,n+1)):
        ctot_i = 0
        for x,y in it.pairwise(perm):

            if y == x + 1:
                ctot_i += 1
        if ctot_i == k:
            ctot += 1
    return ctot

# Derrangement numbers: A000166
def derangement_numbers_generator():
    fn = 0
    n = 2
    while True:
        yield fn
        fn = n*fn + pow(-1,n)
        n += 1 
def d(k):
    assert k > 0
    return next(it.islice(derangement_numbers_generator(),
                          k-1,k))

def U1(n,k):
    assert n > 0
    assert k > 0
    assert k <= n
    summand = [pow(-1,k-j-1)*(j+1) * Fraction(1,factorial(k-j-1)) for j in range(k)]

    sigma = sum(summand)
    ans = binom(n-1,k-1) * factorial(k-1) * sigma
    assert ans.denominator == 1

    return ans.numerator

def U2(n,k):
    assert n > 0
    assert k > 0
    assert k <= n
    summand = [Fraction(pow(-1,i),factorial(i)) for i in range(k+2)]
    sigma = sum(summand)

    ans = factorial(k+1)*binom(n,k)*sigma
    ans *= Fraction(1,n)

    assert ans.denominator == 1

    return ans.numerator

def U3(n,k):
    assert n > 0
    assert k > 0
    assert k <= n
    
    ans = Fraction(binom(n-1,k-1) * d(k+1), k)
    assert ans.denominator == 1
    return ans.numerator

if __name__ == '__main__':
    import tqdm
    print('testing against A010027 list...', end= ' ')
    # From https://oeis.org/A010027/list:
    A010027=[1,1,1,1,2,3,1,3,9,11,1,4,18,44,53,1,5,30,110,265,
     309,1,6,45,220,795,1854,2119,1,7,63,385,1855,6489,
     14833,16687,1,8,84,616,3710,17304,59332,133496,
     148329,1,9,108,924,6678,38934,177996,600732,
     1334961,1468457]
    assert list(it.chain.from_iterable(it.islice(UBF_alt_generator(),10))) == \
        A010027
    testvals = [(10,7),(5,5),(4,1),(7,6),(9,7)]
    print('Done')
    print('testing bf...', end=' ',flush=True)
    for n,k in tqdm.tqdm(testvals):
        bf1 = UBF_alt(n, k)
        assert bf1 == U1(n, k)
        assert U1(n, k) == U2(n, k)
        assert U3(n, k) == U2(n, k)
    print('done')
    nonBF_testvals = [(123,97),(234,230), (999,999), (998,997), (1234,12)]
    print('testing non-bf...', end=' ',flush=True)
    for n,k in tqdm.tqdm(nonBF_testvals):
        U1_ = U1(n,k)
        U2_ = U2(n,k)
        U3_ = U3(n,k)
        assert U1_ == U2_
        assert U3_ == U1_
    print('done')