_prime = 19    #2147483647 # this is the prime number bigger than _max_hash
_max_hash = (1 << 64) - 1

num_perm = 10 # the length of the signature

import numpy as np



def randomArr(seed, len):
    generator = np.random.RandomState(seed)
    arrs = np.array([generator.randint(0, _prime, dtype=np.uint64)
                                          for _ in range(len)], dtype=np.uint64).T
    return arrs



def permuations():
    generator = np.random.RandomState(101)
    permus = np.array([(generator.randint(0, _prime, dtype=np.uint64),
                                           generator.randint(0, _prime, dtype=np.uint64))
                                          for _ in range(num_perm)], dtype=np.uint64).T
    return permus[0], permus[1]

def minhash(arr,a,b):

    hashvalues=_max_hash
    for num in arr:
        hashv = (a * num + b) % _prime
        if hashv<hashvalues: 
            hashvalues=hashv 

    return hashvalues

def jaccard(m1, m2):
    return np.float(np.count_nonzero(m1==m2)) /\
                np.float(len(m1))


def main():
    arr1= randomArr(1, 5)
    print("random array arr1 is created:\n", arr1)
    arr2 = randomArr(99,3 )
    print("random array arr2 is created:\n", arr2)

    a, b  = permuations()

    c=0
    for x,y in zip(a,b):
        min1 = minhash(arr1,x,y)
        print("MinHash signature for arr1 is calculated:\n", min1)
        min2 = minhash(arr2,x,y)
        print("MinHash signature for arr2 is calculated:\n", min2)
        if min1==min2:
            c=c+1
    jac=c/num_perm
    print("Jaccard similarity for arr1 and arr2 is calculated:\n", jac)

if __name__ == '__main__':
    main()
