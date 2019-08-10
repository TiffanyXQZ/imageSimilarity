import numpy as np
import cv2
import matplotlib.pyplot as plt
import time

# Constants
IMAGE_SHAPE = (256, 64)
_IMAGE_SHAPE = IMAGE_SHAPE[::-1]
IMAGE_CHANNELS = 3
IMAGE_MODE = cv2.IMREAD_UNCHANGED
W = 5

images = {'original': '11.jpg',
          'test': '22.jpg',
          'dummy_1': '44.jpg',
          'dummy_2': '55.jpg',
          'dummy_3': '33.jpg',
          }


tim = {'reading_data': -1, 'coverting_image': -1, 'minhashing_table': -1,
       'jacard_similarity': -1, 'simhashing_table': -1, 'simhashing_similarity': -1}


######################################################
# Reading Image
######################################################

def reading_image(images, tim):
    t1 = time.time()
    ims = {}
    for im in images:
        ims[im] = cv2.resize(cv2.cvtColor(cv2.imread(images[im], IMAGE_MODE), cv2.COLOR_BGR2RGB), _IMAGE_SHAPE)
    tim['reading_data'] = time.time() - t1
    return ims


ims_rgb = reading_image(images, tim)

######################################################
# Hash RGB to scaler value
######################################################


def convert_image(im):
    import hash2num as h2
    im1 = np.empty(IMAGE_SHAPE)
    for i in range(0, im.shape[0]):
        for j in range(0, im.shape[1]):
            im1[i, j] = h2.p2num_3d(im[i, j], W, W, W)
    return im1


def convert_images(ims, tim):
    t1 = time.time()
    ims_single = {}
    for im in ims:
        ims_single[im] = convert_image(ims[im])
    tim['coverting_image'] = time.time() - t1
    return ims_single


ims_single = convert_images(ims_rgb, tim)


######################################################
# Calulate minhash
######################################################

from minhash_2 import *
from collections import defaultdict

t1 = time.time()
min_hashs = defaultdict(list)
jacs = defaultdict(int)

a, b = permuations()

for x, y in zip(a, b):
    for im in ims_single:
        min_hashs[im].append(minhash(list(ims_single[im].flatten()), x, y))
tim['minhashing_table'] = time.time() - t1

t1 = time.time()
for i in range(0, len(a)):
    for im in ims_single:
        if min_hashs[im][i] == min_hashs['original'][i]:
            jacs[im] += 1
        else:
            jacs[im] += 0
else:
    for im in jacs:
        jacs[im] = jacs[im] / num_perm
        print('Jaccard similarity of minhash for the original pic and the {} pic is calculated: \n {}'.format(im, jacs[im]))
tim['jacard_similarity'] = time.time() - t1

print('===================================')


######################################################
# Calculate simhash
######################################################

t1 = time.time()
from simhash import *
k = 50
hs = reference_gen(IMAGE_SHAPE[0] * IMAGE_SHAPE[1], k)
pss = {}
sim_hashs = {}
for im in ims_single:
    pss[im] = k_simhash(list(ims_single[im].flatten()), hs)
tim['simhashing_table'] = time.time() - t1
t1 = time.time()
for im in pss:
    sim_hashs[im] = sim_dis(pss['original'], pss[im])
    print(f"SimHash similarity for the original pic and the {im} pic is calculated:\n", sim_hashs[im])
tim['simhashing_similarity'] = time.time() - t1

print('===================================')


def display_time(ti):
    for event, tim in ti.items():
        print('The time for {} is : {}s'.format(event, tim))


display_time(tim)
