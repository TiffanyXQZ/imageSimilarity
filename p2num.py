import math
import minhash_2 as mh
import numpy as np


def pairing_2d(point_2d, w, h):
    p = list([int(point_2d[0] / w), int(point_2d[1] / h)])
    try:
        num = math.pow(2, p[0]) * (2 * p[1] + 1) - 1
    except OverflowError:
        print("too big")
        num = 10000
    return num


def pairing_3d(point, w, h, l):
    p_2d = pairing_2d(point[:2], w, h)
    p_3d = pairing_2d([point[2], p_2d], 1, l)
    return p_3d


def pairing_2d_shift(point_2d, w, h, shift):
    p = []
    p = list([int((point_2d[0] - shift * w) / w), int((point_2d[1] - shift * h) / h)])
    num = math.pow(2, p[0]) * (2 * p[1] + 1) - 1
    return int(num)


def _pairing_3d_2d__shift(point_2d, h, shift):
    p = list([int(point_2d[0]), int((point_2d[1] - shift * h) / h)])
    num = math.pow(2, p[0]) * (2 * p[1] + 1) - 1
    return int(num)


def pairing_3d_shift(point, w, h, l, shift):
    p_2d = pairing_2d_shift(point[:2], w, h, shift)
    p_3d = _pairing_3d_2d__shift([point[2], p_2d], l, shift)
    return p_3d

def points3d_gen(num):
    # arr = np.random.uniform(size=num*3)
    arr = np.random.randint(low=0, high=255, size=num * 3)
    arr1 = arr.reshape((num, 3))
    return arr1.tolist()


def main():
###############################################
#   Input: two sets of 3D points here
###############################################
    p1 = ([1, 2, 4], [3, 4, 6], [5, 6, 8])
    p2 = ([9, 10, 11], [12, 13, 14], [1.5, 2, 4], [3, 4.6, 6], [5.3, 6, 8])

##########################################################
#   Output: two hashed sets of points to sets of numbers
##########################################################
    num1 = [pairing_3d(p, 1,2,4) for p in p1]
    num2 = [pairing_3d(p, 1,2,4) for p in p2]

    print(f'points p1 is hashed to number of:\n {num1}')
    print(f'points p2 is hashed to number of:\n {num2}')
####################################################
#   jaccard similarity of these two sets of numbers
####################################################
    a, b = mh.permuations()
    c, cs = 0, 0
    for x, y in zip(a, b):
        m1 = mh.minhash(num1, x, y)
        m2 = mh.minhash(num2, x, y)

        print("MinHash signature for num1 is calculated:\n", m1)
        print("MinHash signature for num2 is calculated:\n", m2)

        if m1 == m2:
            c = c + 1

    jac = c / mh.num_perm
    print("Jaccard similarity for num1 and num2 is calculated:\n", jac)

#############################################################################
#   hash the above input two sets of 3D points to sets of numbers with shift
#############################################################################
    shift = 0.5
    num1s = [pairing_3d_shift(p, 1, 2, 4, shift) for p in p1]
    num2s = [pairing_3d_shift(p, 1, 2, 4, shift) for p in p2]
    print(f'points p1 is hashed to number of:\n ({num1s}) with shift of {shift}')
    print(f'points p2 is hashed to number of:\n ({num2s}) with shift of {shift}')
##############################################################
#   jaccard similarity of these two shifted sets of numbers
##############################################################
    a, b = mh.permuations()
    c, cs = 0, 0
    for x, y in zip(a, b):
        m1s = mh.minhash(num1, x, y)
        m2s = mh.minhash(num2, x, y)

        print("MinHash signature for num1s is calculated:\n", m1s)
        print("MinHash signature for num2s is calculated:\n", m2s)

        if m1s == m2s:
            cs = cs + 1

    jacs = cs/ mh.num_perm
    print("Jaccard similarity for num1s and num2s is calculated:\n", jacs)

#############################################################################
#   randomly generate 3d points sets
#############################################################################

    # a1 = points3d_gen(1000)
    # a2 = points3d_gen(10)
    #
    # ap1 = [pairing_3d(p, 1, 2, 4) for p in a1]
    # ap2 = [pairing_3d(p, 1, 2, 4) for p in a2]
    #
    # a, b = mh.permuations()
    # c = 0
    # for x, y in zip(a, b):
    #     ma1 = mh.minhash(ap1, x, y)
    #     ma2 = mh.minhash(ap2, x, y)
    #
    #     print("MinHash signature for ap1 is calculated:\n", ap1)
    #     print("MinHash signature for ap2 is calculated:\n", ap2)
    #
    #     if ma1 == ma2:
    #         c = c + 1
    #
    # jaca = c/ mh.num_perm
    # print("Jaccard similarity for num1s and num2s is calculated:\n", jaca)




if __name__ == '__main__':
    main()
