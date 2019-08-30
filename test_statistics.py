from utils import *
import numpy as np
import cv2
import time


######################################################
# Constants
######################################################

RESIZE_RATIO = (1, 1)


######################################################
# Inputs
######################################################
images = {'original': 'images/11.jpg',
          'test': 'images/22.jpg',
          'dummy_1': 'images/44.jpg',
          'dummy_2': 'images/55.jpg',
          'dummy_3': 'images/33.jpg'
          }

tim = {'reading_data': -1, 'coverting_image': -1,
       'minhashing_table': -1, 'jacard_similarity': -1,
       'simhashing_table': -1, 'simhashing_similarity': -1}

######################################################
# Reading Image as original size as BGR mode
######################################################

ims_bgr, reading_time = reading_image(images, tim)

for item in ims_bgr:
    print('The picture {}\'s shape is : {}'.format(item, ims_bgr[item].shape))

print('======================================================================')


######################################################
# Image resize
######################################################

ims = resize(ims_bgr, RESIZE_RATIO)

######################################################
# Hash RGB to scaler value
######################################################

print('Begin hashing each picture...')

ims_hash, color_counts, hashing_time = convert_images(ims, tim)

print('=============Hash completed!================')

for item in color_counts:
    print('The number of colors of {} is : {}'.format(item, len(color_counts[item])))

print('======================================================================')


######################################################
# Color statistics analysis
######################################################
for im in color_counts:
    bar(im, color_counts[im])  # histogram of color counts

n = 20
sorted_counts = sort_dicts(color_counts)
top_n_counts = top_dics(color_counts, 20)
for im in top_n_counts:
    name = '{} with top {} counts'.format(im, n)
    bar(name, top_n_counts[im])  # histogram of color counts

sorted_freqs = freq(sorted_counts, ims_hash)
top_n_freqs = top_dics(sorted_freqs, n)
print('Top {} colors with their proportions of each pic'.format(n))
for im in top_n_freqs:
    import pprint
    print('======', im)
    pp = pprint.PrettyPrinter()
    pp.pprint(top_n_freqs[im])

    name = '{} with top {} color frequency'.format(im, n)
    bar(name, top_n_freqs[im])  # histogram of color counts
