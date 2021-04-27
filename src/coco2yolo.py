import yaml
import os
import glob
import random
import xml.dom.minidom as xmldom

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
    test_dev = open('../'+ dataset_name + '/test-dev.txt', 'w')
    train.write('\n'.join(images[:int(len(images) * 0.8)]))
    val.write('\n'.join(images[int(len(images) * 0.8):int(len(images) * 0.9)]))
    test_dev.write('\n'.join(images[int(len(images) * 0.9):]))
    train.close()
    val.close()
    test_dev.close()

from tqdm import tqdm
def get_label(labels):
    # remove the ../Openbrand/labels/
    id_name = {i['id']: i['file_name'] for i in labels['images']}
    id_w = {i['id']: i['width'] for i in labels['images']}
    id_h = {i['id']: i['height'] for i in labels['images']}

    for i in tqdm(range(len(labels['annotations']))):
        anno = labels['annotations'][i]
        id = anno['image_id']
        txt = open('../' + dataset_name + '/labels/' + id_name[id][:-3] + 'txt', 'a')
        x, y, w, h = anno['bbox']
        width = id_w[id]
        height = id_h[id]
        x = (x + w/2)/width
        y = (y + y/2)/height
        w /= width
        h /= height
        txt.write(' '.join((str(anno['category_id']), str(x), str(y), str(w), str(h))) + '\n')
        txt.close()


import json
if __name__ == '__main__':

    labels = json.load(open('../' + dataset_name + '/openbrand_train.json', 'r'))
    get_brand_names(labels['categories'])

    images = glob.glob('../' + dataset_name + '/images/*.jpg')
    images = [i.replace('\\', '/') for i in images]
    split_train_val_test(images)

    get_label(labels)
