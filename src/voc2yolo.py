import yaml
import os
import glob
import random
import xml.dom.minidom as xmldom

images = []
brand_id = {}

random.seed(1)

def get_brand_names():
    brand_names = []
    for dir in os.listdir('../LogoDet-3K/images/'):
        brands = os.listdir('../LogoDet-3K/images/' + dir)
        brand_names += brands
        print(dir, brands)
        for brand in brands:
            if not os.path.exists('../LogoDet-3K/labels/' + dir + '/' + brand):
                os.makedirs('../LogoDet-3K/labels/' + dir + '/' + brand)
            brand_id[brand] = len(brand_id)
    print('nc:', len(brand_names))
    print('names:', brand_names)
    print(brand_id)
    for i in range(len(brand_names)):
        assert brand_id[brand_names[i]] == i


def split_train_val_test(images):
    # images = ['./' + '/'.join(i.split('/')[3:]) for i in images]
    random.shuffle(images)
    print('the number of images:', len(images), '(', images[0], '...)')
    train = open('../LogoDet-3K/train.txt', 'w')
    val = open('../LogoDet-3K/val.txt', 'w')
    test_dev = open('../LogoDet-3K/test-dev.txt', 'w')
    train.write('\n'.join(images[:int(len(images) * 0.8)]))
    val.write('\n'.join(images[int(len(images) * 0.8):int(len(images) * 0.9)]))
    test_dev.write('\n'.join(images[int(len(images) * 0.9):]))
    train.close()
    val.close()
    test_dev.close()


def parse_xml(fn):
    xml_file = xmldom.parse(fn)
    eles = xml_file.documentElement
    objects = eles.getElementsByTagName("object")
    width = float(eles.getElementsByTagName("width")[0].firstChild.data)
    height = float(eles.getElementsByTagName("height")[0].firstChild.data)
    labels = []
    for object in objects:
        name = brand_id[object.getElementsByTagName("name")[0].firstChild.data]
        xmin = float(object.getElementsByTagName("xmin")[0].firstChild.data)
        xmax = float(object.getElementsByTagName("xmax")[0].firstChild.data)
        ymin = float(object.getElementsByTagName("ymin")[0].firstChild.data)
        ymax = float(object.getElementsByTagName("ymax")[0].firstChild.data)
        x = (xmax + xmin) /2 / width
        w = (xmax - xmin) / width
        y = (ymax + ymin) /2/ height
        h = (ymax - ymin) / height
        labels.append(' '.join((str(name), str(x), str(y), str(w), str(h))))
        # if len(objects)>1:
        #     print(fn ,xmin, xmax, ymin, ymax)
    # print(labels)
    txt = open(fn.replace('images', 'labels',1)[:-3]+'txt', 'w')
    txt.write('\n'.join(labels))
    txt.close()


def get_label():
    for img in images:
        print(img)
        parse_xml(img[:-3] + 'xml')


if __name__ == '__main__':
    images = glob.glob('../LogoDet-3K/images/*/*/*.jpg')
    images = [i.replace('\\', '/') for i in images]
    get_brand_names()
    split_train_val_test(images)
    get_label()
