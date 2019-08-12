import math
import minhash_2 as mh
import numpy as np
from hashfunc import sha1_hash32

colors_ranges = (((0, 0, 180), (180, 20, 255), 1),
                 ((0, 0, 0), (0, 0, 65), 2),
                 ((0, 50, 50), (15, 255, 255), 3),
                 ((15, 50, 50), (25, 255, 255), 4),
                 ((25, 50, 50), (34, 255, 255), 5),
                 ((34, 50, 50), (44, 255, 255), 6),
                 ((44, 50, 50), (60, 255, 255), 7),
                 ((60, 50, 50), (80, 255, 255), 8),
                 ((80, 50, 50), (95, 255, 255), 9),
                 ((95, 50, 50), (110, 255, 255), 10),
                 ((110, 180, 50), (130, 255, 255), 11),
                 ((130, 50, 50), (158, 255, 255), 12),
                 ((158, 50, 50), (180, 255, 255), 3)
                 )


def HSV_p2num_3d(p_3d):
    for color in colors_ranges:
        if color[0][0] < p_3d[0] and color[1][0] > p_3d[0] and \
           color[0][1] < p_3d[1] and color[1][1] > p_3d[1] and \
           color[0][2] < p_3d[2] and color[1][2] > p_3d[2]:
            return color[2]
    else:
        return 0


def p2num_2d(p_2d, w, h):
    p = list([int(p_2d[0] / w), int(p_2d[1] / h)])
    s = f's{p[0]}s{p[1]}'
    print(s)
    return hash(s)


def p2num_3d(p_3d, w, h, l):
    r, g, b = int(p_3d[0] / w), int(p_3d[1] / h), int(p_3d[2] / l)
    x = int(255 / w)
    s = r + g * x + b * x ^ 2

    return s


# def p2num_3d(p_3d, w, h, l):
#     p = list([int(p_3d[0] / w), int(p_3d[1] / h), int(p_3d[2] / l)])
#     s = f's{p[0]}s{p[1]}s{p[2]}'

#     return sha1_hash32(s)


def p2num_2d_shift(point_2d, w, h, shift):
    p = []
    p = list([int((point_2d[0] - shift * w) / w),
              int((point_2d[1] - shift * h) / h)])
    s = f's{p[0]}s{p[1]}'
    return sha1_hash32(s)


def p2num_3d_shift(point_3d, w, h, l, shift):
    p = list([int((point_3d[0] - shift * w) / w),
              int((point_3d[1] - shift * h) / h),
              int((point_3d[2] - shift * l) / l)])
    s = f's{p[0]}s{p[1]}s{p[2]}'
    return sha1_hash32(s)


def points3d_gen(num):
    # arr = np.random.uniform(size=num*3)
    arr = np.random.randint(low=0, high=255, size=num * 3)
    arr1 = arr.reshape((num, 3))
    return arr1.tolist()


def main():
    p1 = ([1, 2], [3, 4], [5, 6])
    num1 = [p2num_2d(p, 1, 1) for p in p1]
    print(num1)
    p2 = ([9, 10, 11], [12, 13, 14], [1.5, 2, 4], [3, 4.6, 6], [5.3, 6, 8])
    num2 = [p2num_3d(p, 1, 1, 1) for p in p2]
    print(num2)

    shift = 0.5
    num1_s = [p2num_2d_shift(p, 1, 1, 0.5) for p in p1]
    print(num1)
    num2_s = [p2num_3d_shift(p, 1, 1, 1, 0.5) for p in p2]
    print(num2_s)

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

    print(f'points p2 is hashed to number of:\n ({num2_s}) with shift of {shift}')
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

    jacs = cs / mh.num_perm
    print("Jaccard similarity for num1s and num2s is calculated:\n", jacs)

#############################################################################
#   randomly generate 3d points sets
#############################################################################

    a1 = points3d_gen(100)
    a2 = points3d_gen(100)
    print(a1)
    print(a2)

    ap1 = [p2num_3d(p, 1, 2, 4) for p in a1]
    ap2 = [p2num_3d(p, 1, 2, 4) for p in a2]

    a, b = mh.permuations()
    c = 0
    print(ap1)
    print(ap2)
    for x, y in zip(a, b):
        ma1 = mh.minhash(ap1, x, y)
        ma2 = mh.minhash(ap2, x, y)

        print("MinHash signature for ap1 is calculated:\n", ma1)
        print("MinHash signature for ap2 is calculated:\n", ma2)

        if ma1 == ma2:
            c = c + 1

    jaca = c / mh.num_perm
    print("Jaccard similarity for num1s and num2s is calculated:\n", jaca)


if __name__ == '__main__':
    main()
