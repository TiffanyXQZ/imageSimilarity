import matplotlib.pyplot as plt
import numpy as np
import cv2
import time

######################################################
# Constants
######################################################

RESIZE_RATIO = (0.1, 0.1)
W = 25.5  # This means total 1000 colors. 10*10*10
IMAGE_MODE = cv2.IMREAD_UNCHANGED

######################################################
# Reading Image as original size as BGR mode
######################################################


def duration():
    time.sleep(1)
    # k = cv2.waitKey(0)


def reading_image(images, tim):
    t1 = time.time()
    ims = {}
    reading_time = {}
    print('\nPress any key to exit OpenCV image_show and continue!')
    print('======================================================================')
    for im in images:
        t2 = time.time()
        ims[im] = cv2.imread(images[im], IMAGE_MODE)
        reading_time[im] = time.time() - t2
        cv2.imshow(im, ims[im])
    tim['reading_data'] = time.time() - t1
    duration()
    cv2.destroyAllWindows()
    return ims, reading_time


######################################################
# Image Resize
######################################################


def resize(ims_bgr, RESIZE_RATIO):
    ims_resize = {}
    print('\nPress any key to exit OpenCV image_show and continue!')
    print('======================================================================')
    for im in ims_bgr:
        shape_minhash = (int(ims_bgr[im].shape[0] * RESIZE_RATIO[0]),
                         int(ims_bgr[im].shape[1] * RESIZE_RATIO[1]))
        ims_resize[im] = cv2.resize(ims_bgr[im], shape_minhash)
        cv2.imshow(im, ims_resize[im])
        cv2.imwrite('resize_images/{}.jpg'.format(im), ims_bgr[im])
    duration()
    cv2.destroyAllWindows()
    return ims_resize


######################################################
# Hash RGB to scaler value
######################################################


def convert_image(im):
    import hash2num as h2
    im1 = np.empty(im.shape[:2], dtype=np.int16)
    for i in range(0, im.shape[0]):
        for j in range(0, im.shape[1]):
            im1[i, j] = h2.p2num_3d(im[i, j], W, W, W)
    return im1


def convert_images(ims, tim):
    t1 = time.time()
    ims_hash = {}
    color_stats = {}
    hashing_time = {}
    for im in ims:
        t2 = time.time()
        ims_hash[im] = convert_image(ims[im])
        hashing_time[im] = time.time() - t2
        print('=============One pic hashed!================')
        print('Time is:', hashing_time[im])
        colors, counts = np.unique(ims_hash[im], return_counts=True)
        color_stats[im] = dict(zip(colors, counts))

    tim['coverting_image'] = time.time() - t1
    return ims_hash, color_stats, hashing_time


######################################################
# Color Statistics
######################################################
def bar(name, im):
    x, y = list(im.keys()), list(im.values())
    plt.bar(x, y, facecolor='g', alpha=0.75)
    plt.xlabel('Colors')
    plt.ylabel('Counts')
    plt.title('Bar of {}'.format(name))
    plt.grid(True)
    plt.savefig('bar/{}.jpg'.format(name), dpi=150)
    plt.show()


def frequecy(im, shape):
    total = shape[0] * shape[1]
    color_freq = {}
    for co in im:
        color_freq[co] = im[co] / total
    return color_freq


def freq(col_s, ims):
    color_freqs = {}
    for im in ims:
        color_freqs[im] = frequecy(col_s[im], ims[im].shape)
    return color_freqs


def sort_dic(dic):
    di = {}
    for key, value in sorted(dic.items(), key=lambda kv: kv[1]):
        di[key] = value
    return di


def sort_dicts(dics):
    sorted_dics = {}
    for im in dics:
        sorted_dics[im] = sort_dic(dics[im])
    return sorted_dics


def top(im, n):
    top_n = {}
    for i in range(0, n):
        key, val = im.popitem()
        top_n[key] = val
    return top_n


def top_dics(ims, n):
    top_ims = {}
    for im in ims:
        top_ims[im] = top(ims[im], n)
    return top_ims
