import numpy as np
import cv2
import matplotlib.pyplot as plt
import time

# Constants
IMAGE_SHAPE = (128, 128)
IMAGE_CHANNELS = 3
IMAGE_ORIGINAL = '1.jpg'
IMAGE_TEST = '2.jpg'
IMAGE_IRRELAVENT = '4.jpg'
IMAGE_MODE = cv2.IMREAD_UNCHANGED


tim = {'reading_data': -1, 'coverting_image': -1, 'minhashing': -1, 'simhashing': -1}

# Reading Image
t1 = time.time()
original = cv2.resize(cv2.cvtColor(cv2.imread(IMAGE_ORIGINAL, IMAGE_MODE), cv2.COLOR_BGR2RGB), IMAGE_SHAPE)
test = cv2.resize(cv2.cvtColor(cv2.imread(IMAGE_TEST, IMAGE_MODE), cv2.COLOR_BGR2RGB), IMAGE_SHAPE)
dummy = cv2.resize(cv2.cvtColor(cv2.imread(IMAGE_IRRELAVENT, IMAGE_MODE), cv2.COLOR_BGR2RGB), IMAGE_SHAPE)
tim['reading_data'] = time.time() - t1

# Hash RGB to scaler value


def hash_image(im):
    import hash2num as h2
    im1 = np.empty(IMAGE_SHAPE)
    for i in range(0, im.shape[0]):
        for j in range(0, im.shape[1]):
            im1[i, j] = h2.p2num_3d(im[i, j], 10, 10, 10)
    return im1


t1 = time.time()
test_hash = hash_image(test)
original_hash = hash_image(original)
dummy_hash = hash_image(dummy)
tim['coverting_image'] = time.time() - t1

# Calulate minhash
t1 = time.time()

from minhash_2 import *
a, b = permuations()

c = 0
for x, y in zip(a, b):
    min1 = minhash(list(original_hash.flatten()), x, y)
    min2 = minhash(list(test_hash.flatten()), x, y)
    min3 = minhash(list(dummy_hash.flatten()), x, y)

    if min1 == min2:
        c1 = c + 1
    if min1 == min3:
        c2 = c + 1
jac1 = c1 / num_perm
print("Jaccard similarity for original pic and test pic is calculated:\n", jac1)

jac2 = c2 / num_perm
print("Jaccard similarity for original pic and irrelavent pic is calculated:\n", jac2)
tim['minhashing'] = time.time() - t1


# Calculate simhash

t1 = time.time()

from simhash import *
k = 50
hs = reference_gen(IMAGE_SHAPE[0] * IMAGE_SHAPE[1], k)

pss1 = k_simhash(list(original_hash.flatten()), hs)
pss2 = k_simhash(list(test_hash.flatten()), hs)
pss3 = k_simhash(list(dummy_hash.flatten()), hs)
# print(pss1)
# print(pss2)
# print(pss3)
dis1 = sim_dis(pss1, pss2)
print("SimHash similarity for original pic and test pic is calculated:\n", dis1)
dis2 = sim_dis(pss1, pss3)
print("SimHash similarity for original pic and dummy pic is calculated:\n", dis2)
tim['simhashing'] = time.time() - t1


def display_time(ti):
    for event, tim in ti.items():
        print('The time for {} is : {}s'.format(event, tim))


display_time(tim)
