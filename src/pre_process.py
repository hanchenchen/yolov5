import json
from tqdm import tqdm
dataset_name = "Openbrand"
labels = json.load(open('../' + dataset_name + '/Openbrand_train.json', 'r'))
file_id = {i['file_name']:i['id'] for i in labels}
path = "runs/test/epoch1/"
results = json.load(open(path + 'best_predictions.json', 'r'))
print(len(results))
# exit()
for i in tqdm(range(len(results))):
    results[i]['image_id'] = file_id[results[i]['image_id']+'.jpg']
    results[i]['bbox'] = [int(i) for i in results[i]['bbox']]

json.dump(results, open(path + 'best_predictions_id.json','w'))