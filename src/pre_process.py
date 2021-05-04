import json
from tqdm import tqdm
dataset_name = "Openbrand"
labels = json.load(open('../' + dataset_name + '/Openbrand_train.json', 'r'))['images']
file_id = {i['file_name']:str(i['id']) for i in labels}

# exit()

old_train = open('../'+ dataset_name + '/train.txt', 'r').read().split('\n')
old_val = open('../'+ dataset_name + '/val.txt', 'r').read().split('\n')

for i in tqdm(range(len(old_train))):
    old_train[i] = file_id[old_train[i][20:]] + ".jpg"

for i in tqdm(range(len(old_val))):
    old_val[i] = file_id[old_val[i][20:]] + ".jpg"

new_train = open('../'+ dataset_name + '/new_train.txt', 'w')
new_val = open('../'+ dataset_name + '/new_val.txt', 'w')
new_train.write('\n'.join(old_train))
new_val.write('\n'.join(old_val))


new_train.close()
new_val.close()

