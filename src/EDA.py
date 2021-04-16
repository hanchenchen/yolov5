import pandas as pd
import json

data = json.load(open('./PANDA_IMAGE/image_annos/person_bbox_train.json'))
print(len(data), type(data))

head_size = []
visible_body_size = []
full_body_size = []


for name, image in data.items():
    print(name)
    if "objects list" in image:
        for object in image["objects list"]:
            if object['category'] != "person":
                continue
            object = object["rects"]

            bbox = object['head']
            a = bbox['br']['x'] - bbox['tl']['x'] # w
            b = bbox['br']['y'] - bbox['tl']['y'] # h
            head_size.append([b*image["image size"]['height'], a*image["image size"]['width'], a/b])

            bbox = object['visible body']
            a = bbox['br']['x'] - bbox['tl']['x']  # w
            b = bbox['br']['y'] - bbox['tl']['y']  # h
            visible_body_size.append([b * image["image size"]['height'], a * image["image size"]['width'], a / b])

            bbox = object['full body']
            a = bbox['br']['x'] - bbox['tl']['x']  # w
            b = bbox['br']['y'] - bbox['tl']['y']  # h
            full_body_size.append([b * image["image size"]['height'], a * image["image size"]['width'], a / b])

            # print(head_size)
            # print(pd.DataFrame(head_size, columns=['h', 'w', 'ratio']).describe())
            # exit()
print('head_size')
print(pd.DataFrame(head_size, columns=['h', 'w', 'ratio']).describe())
print( 'visible_body_size')
print(pd.DataFrame(visible_body_size, columns=['h', 'w', 'ratio']).describe())
print('full_body_size')
print(pd.DataFrame(full_body_size, columns=['h', 'w', 'ratio']).describe())


data = json.load(open('./PANDA_IMAGE/image_annos/vehicle_bbox_train.json'))
print(len(data), type(data))

vehicle_size = []


for name, image in data.items():
    # print(name)
    if "objects list" in image:
        for object in image["objects list"]:

            bbox = object["rect"]
            a = bbox['br']['x'] - bbox['tl']['x'] # w
            b = bbox['br']['y'] - bbox['tl']['y'] # h
            vehicle_size.append([b*image["image size"]['height'], a*image["image size"]['width'], a/b])

            # print(head_size)
            # print(pd.DataFrame(head_size, columns=['h', 'w', 'ratio']).describe())
            # exit()
print('vehicle_size')
print(pd.DataFrame(vehicle_size, columns=['h', 'w', 'ratio']).describe())
