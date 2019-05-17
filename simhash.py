import hash2num as hn
import numpy as np
import minhash_2 as mh


def points3d_gen(num):
    # arr = np.random.uniform(size=num*3)
    arr = np.random.randint(low=0, high=255, size=num * 3)
    arr1 = arr.reshape((num, 3))
    return arr1.tolist()

def reference_gen(num, k):
    # arr = np.random.uniform(size=num*3)
    arr = np.random.uniform(low=-1, high=1, size=num*k )
    arr1 = arr.reshape((k, num))
    return arr1.tolist()
s
#This step is calculating SimHash
def simhash(t, h):
    sum = 0
    for i in range(0, len(t)):
        sum = sum + (t[i] * h[i])
    if sum>0:
        return 1
    elif sum==0:
        return 0
    else:
        return -1

#k_simhash calculates signature
def k_simhash(t, hs):
    return [simhash(t ,h) for h in hs]

#Compare simHash distannce
def sim_dis(sim1, sim2):
    num = 0
    for i in range(0, len(sim1)):
        if sim1[i]==sim2[i]:
            num += 1
    return (num/len(sim1))

def main():

#Composing Artifitial Data ps1 and ps2
    ps1 = ([255,255,255], [255,255,255],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[245,245,245])
    ps2 = ([255,255,255], [255,255,255],[245,245,245],[240,255,255],[252,230,201],[252,230,201],[252,230,201])

#Hash 3D ps1 and ps2 to 1D
    pn1 = [hn.p2num_3d(p, 1, 2, 4) for p in ps1]
    pn2 = [hn.p2num_3d(p, 1, 2, 4) for p in ps2]
    print(pn1)
    print(pn2)

#Calculate SimHash
    k = 5
    hs = reference_gen(len(pn1), k)
    for h in hs:
        print(h)
        print(simhash(pn1,h))
#Calculate SimHash Signature
    pss1 = k_simhash(pn1, hs)
    pss2 = k_simhash(pn2,hs)
    print(pss1)
    print(pss2)

#Compare SimHash distance, aka similarity of SimHash
    dis = sim_dis(pss1, pss2)
    print(dis)

#Calculate Jaccard Similarity between ps1 and ps2.
# However this is not right, since the hashed numberr from
# 3D is too big for minhashing. the minhash program we wrote
# can only calculate numbers smaller than 2147483647
# but the number we get is 19 digits long.


    a, b = mh.permuations()
    c, cs = 0, 0
    for x, y in zip(a, b):
        m1 = mh.minhash(pn1, x, y)
        m2 = mh.minhash(pn2, x, y)

        # print("MinHash signature for num1 is calculated:\n", m1)
        # print("MinHash signature for num2 is calculated:\n", m2)

        if m1 == m2:
            c = c + 1

    jac = c / mh.num_perm
    print("Jaccard similarity for num1 and num2 is calculated:\n", jac)






if __name__ == '__main__':
    main()

