import yaml
import os
import glob
import random
import xml.dom.minidom as xmldom
from tqdm import tqdm
import shutil
images = []
brand_id = {}
dataset_name = "Openbrand"
random.seed(1)

def get_brand_names(categories):
    brand_id = {cate["name"]: cate["id"] for cate in categories }
    brand_id["none_zero"] = 0
    brand_names = ['' for i in range(len(brand_id))]
    for brand,id in brand_id.items():
        brand_names[id] = brand

    print('nc:', len(brand_names))
    print('names:', brand_names)
    print(brand_id)
    for i in range(len(brand_names)):
        assert brand_id[brand_names[i]] == i


def split_train_val_test(images):
    # images = ['./' + '/'.join(i.split('/')[3:]) for i in images]
    random.shuffle(images)
    print('the number of images:', len(images), '(', images[0], '...)')
    train = open('../'+ dataset_name + '/train.txt', 'w')
    val = open('../'+ dataset_name + '/val.txt', 'w')
    train.write('\n'.join(images[:int(len(images) * 0.9)]))
    val.write('\n'.join(images[int(len(images) * 0.9):]))
    train.close()
    val.close()

def get_test():
    # images = ['./' + '/'.join(i.split('/')[3:]) for i in images]
    images = glob.glob('../' + dataset_name + '/test/*.jpg')
    images = [i.replace('\\', '/') for i in images]
    random.shuffle(images)
    print('the number of test images:', len(images), '(', images[0], '...)')
    test_dev = open('../'+ dataset_name + '/test-dev.txt', 'w')
    test_dev.write('\n'.join(images))
    test_dev.close()

def move_images():
    images = glob.glob('../' + dataset_name + '/data/*/*.jpg')
    images = [i.replace('\\', '/') for i in images]
    for img in tqdm(images):
        shutil.move(img, '../' + dataset_name + '/images')


def get_label(labels):
    # remove the ../Openbrand/labels/
    id_name = {i['id']: i['file_name'] for i in labels['images']}
    id_w = {i['id']: i['width'] for i in labels['images']}
    id_h = {i['id']: i['height'] for i in labels['images']}

    for i in tqdm(range(len(labels['annotations']))):
        anno = labels['annotations'][i]
        id = anno['image_id']
        if not os.path.exists('../' + dataset_name + '/images/' + id_name[id]):
            continue
        # print('../' + dataset_name + '/images/' + id_name[id])

        txt = open('../' + dataset_name + '/labels/' + id_name[id][:-3] + 'txt', 'a')
        x, y, w, h = anno['bbox']
        width = id_w[id]
        height = id_h[id]
        x = (x + w/2)/width
        y = (y + h/2)/height
        w /= width
        h /= height
        txt.write(' '.join((str(anno['category_id']), str(x), str(y), str(w), str(h))) + '\n')
        txt.close()
def filename2id():
    dataset_name = "Openbrand"
    labels = json.load(open('../' + dataset_name + '/Openbrand_train.json', 'r'))['images']
    file_id = {i['file_name']: str(i['id']) for i in labels}
    images = glob.glob('../' + dataset_name + '/images/*.jpg')[:10]
    images = [i.replace('\\', '/') for i in images]
    for img in tqdm(images):
        shutil.move(img, '../' + dataset_name + '/images_id/' +file_id[img.split('/')[-1]] + ".jpg")
    dataset_name = "Openbrand"
    labels = json.load(open('../' + dataset_name + '/openBrand_testA_list.json', 'r'))
    file_id = {i['file_name']: str(i['id']) for i in labels}
    images = glob.glob('../' + dataset_name + '/test/*.jpg')[:10]
    images = [i.replace('\\', '/') for i in images]
    for img in tqdm(images):
        shutil.move(img, '../' + dataset_name + '/test_id/' + file_id[img.split('/')[-1]] + ".jpg")
 # -- yolov5
 # -- Openbrand
 #    | -- data
 #          | --

import json
if __name__ == '__main__':
    # move_images()
    # labels = json.load(open('../' + dataset_name + '/openbrand_train.json', 'r'))
    # get_brand_names(labels['categories'])
    #
    # images = glob.glob('../' + dataset_name + '/images/*.jpg')
    # images = [i.replace('\\', '/') for i in images]
    # print(len(images))
    #
    # split_train_val_test(images)
    #
    # get_label(labels)
    # get_test()
    filename2id()
