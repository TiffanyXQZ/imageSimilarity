
import numpy as np
import cv2
import matplotlib.pyplot as plt
import time

# Constants
RESIZE_RATIO = (1, 1)
IMAGE_MODE = cv2.IMREAD_UNCHANGED
W = 25.5  # This means total 1000 colors. 10*10*10

images = {'original': 'images/11.jpg',
          'test': 'images/22.jpg',
          'dummy_1': 'images/44.jpg',
          'dummy_2': 'images/55.jpg',
          'dummy_3': 'images/33.jpg'
          }


tim = {'reading_data': -1, 'coverting_image': -1, 'minhashing_table': -1,
       'jacard_similarity': -1, 'simhashing_table': -1, 'simhashing_similarity': -1}

print('\n\nPress any key to exit OpenCV image_show and continue!')
print('======================================================================')

######################################################
# Reading Image as original size as BGR mode
######################################################


def reading_image(images, tim):
    t1 = time.time()
    ims = {}
    reading_time = {}
    for im in images:
        t2 = time.time()
        ims[im] = cv2.imread(images[im], IMAGE_MODE)
        reading_time[im] = time.time() - t2
        cv2.imshow(im, ims[im])
    tim['reading_data'] = time.time() - t1
    return ims, reading_time


ims_bgr, reading_time = reading_image(images, tim)

for item in ims_bgr:
    print('The picture {}\'s shape is : {}'.format(item, ims_bgr[item].shape))

print('======================================================================')


k = cv2.waitKey(0)
cv2.destroyAllWindows()


######################################################
# Image Resize as proportion for Minhash
######################################################

ims_minhash = {}
for im in ims_bgr:
    shape_minhash = (int(ims_bgr[im].shape[0] * RESIZE_RATIO[0]),
                     int(ims_bgr[im].shape[1] * RESIZE_RATIO[1]))
    ims_minhash[im] = cv2.resize(ims_bgr[im], shape_minhash)
    cv2.imshow(im, ims_minhash[im])
    cv2.imwrite('resize_images/{}.jpg'.format(im), ims_bgr[im])
k = cv2.waitKey(0)
cv2.destroyAllWindows()

######################################################
# Hash RGB to scaler value for minhash
######################################################


def convert_image(im):
    import hash2num as h2
    im1 = np.empty(im.shape[:2])
    for i in range(0, im.shape[0]):
        for j in range(0, im.shape[1]):
            im1[i, j] = h2.p2num_3d(im[i, j], W, W, W)
    return im1


def convert_images(ims, tim):
    t1 = time.time()
    ims_hash = {}
    color_nums = {}
    hashing_time = {}
    for im in ims:
        t2 = time.time()
        ims_hash[im] = convert_image(ims[im])
        hashing_time[im] = time.time() - t2
        print('=============One pic hashed!================')
        print('Time is:', hashing_time[im])
        color_nums[im] = len(np.unique(ims_hash[im]))
    tim['coverting_image'] = time.time() - t1
    return ims_hash, color_nums, hashing_time


print('Begin hashing each picture...')
ims_hash, color_nums, hashing_time = convert_images(ims_minhash, tim)
print('=============Hash completed!================')

for item in color_nums:
    print('The number of colors of {} is : {}'.format(item, color_nums[item]))

print('======================================================================')


for item in ims_hash:
    print('The hashed picture {}\'s shape is : {}'.format(item, ims_hash[item].shape))

print('======================================================================\n\n')


######################################################
# Calculate the exact Jaccard similarity
######################################################
print('Calculate the exact Jaccard similarity .... ')


def jaccard(a, b):
    m = len(set(a) & set(b))
    n = len(set(a) | set(b))
    return m / n


time_ej = {}
tt_ej = 0
for im in ims_hash:
    t1 = time.time()
    jac = jaccard(list(ims_hash[im].flatten()), list(ims_hash['original'].flatten()))
    time_ej[im] = time.time() - t1
    tt_ej += time_ej[im]
    print('The exact Jaccard similarity for the original pic and the {} pic is : \n {}'.format(im, jac))
    print('The time used is: {}s'.format(time_ej[im]))

print('The total time of calculating exact jaccard values of {} pairs is : {}s \n and the average time is: {}s'.format(len(time_ej), tt_ej, tt_ej / len(time_ej)))


######################################################
# Calulate minhash
######################################################

from minhash_2 import *
from collections import defaultdict

t1 = time.time()
min_hashs = defaultdict(list)
jacs = defaultdict(int)

a, b = permuations()

minhashing_time = {}
print('Begin minhashing each picture...')

for x, y in zip(a, b):
    for im in ims_hash:
        t2 = time.time()
        min_hashs[im].append(minhash(list(ims_hash[im].flatten()), x, y))
        minhashing_time[im] = time.time() - t2
tim['minhashing_table'] = time.time() - t1

t1 = time.time()
for i in range(0, len(a)):
    for im in ims_hash:
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
# Image Resize for Simhash
######################################################

ims_simhash = {}
shape_simhash = (128, 256)
for im in ims_bgr:
    ims_simhash[im] = cv2.resize(ims_bgr[im], shape_simhash)
    cv2.imshow(im, ims_simhash[im])
    cv2.imwrite('resize_images/{}.jpg'.format(im), ims_bgr[im])
k = cv2.waitKey(0)
cv2.destroyAllWindows()


######################################################
# Hash RGB to scaler value for minhash
######################################################


print('Begin hashing each picture...')
ims_hash, color_nums, hashing_time = convert_images(ims_simhash, tim)
print('=============Hash completed!================')

for item in color_nums:
    print('The number of colors of {} is : {}'.format(item, color_nums[item]))

print('======================================================================')


for item in ims_hash:
    print('The hashed picture {}\'s shape is : {}'.format(item, ims_hash[item].shape))

print('======================================================================\n\n')


######################################################
# Calculate simhash
######################################################


from simhash import *
t1 = time.time()
k = 50
hs = reference_gen(shape_simhash[0] * shape_simhash[1], k)
pss = {}
sim_hashs = {}
simhashing_time = {}
for im in ims_hash:
    t2 = time.time()
    pss[im] = k_simhash(list(ims_hash[im].flatten()), hs)
    simhashing_time[im] = time.time() - t2
tim['simhashing_table'] = time.time() - t1
t1 = time.time()
for im in pss:
    sim_hashs[im] = sim_dis(pss['original'], pss[im])
    print(f"SimHash similarity for the original pic and the {im} pic is calculated:\n", sim_hashs[im])
tim['simhashing_similarity'] = time.time() - t1

print('===================================\n\n')


def display_time(ti):
    for event, tim in ti.items():
        print('The time for {} is : {}s'.format(event, tim))


def display_reading_time(ti):
    print('The time for reading each picture:')
    for event, tim in ti.items():
        print('The time for reading {} is : {}s'.format(event, tim))


def display_hashing_time(ti):
    print('The time for hashing each picture:')
    for event, tim in ti.items():
        print('The time for hashing {} is : {}s'.format(event, tim))


def display_minhashing_time(ti):
    print('The time for minhashing each picture:')
    for event, tim in ti.items():
        print('The time for minhashing the {} is : {}s'.format(event, tim))


def display_simhashing_time(ti):
    print('The time for simhashing each picture:')
    for event, tim in ti.items():
        print('The time for simhashing the {} is : {}s'.format(event, tim))


display_time(tim)
print('===================================')
display_reading_time(reading_time)
print('===================================')
display_hashing_time(hashing_time)
print('===================================')
display_minhashing_time(minhashing_time)
print('===================================')
display_simhashing_time(simhashing_time)

print('===================================')
print('The average time for calculating the exact Jaccard similarity of a pair is: ', tt_ej / len(time_ej))

print('===================================')
print('The average time for calculating minhash approximate Jaccard similarity of a pair is: ', tim['jacard_similarity'] / len(images))
print('===================================')
print('The average time for calculating Simhash similarity of a pair is: ', tim['simhashing_similarity'] / len(images))
