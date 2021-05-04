import json
from tqdm import tqdm
dataset_name = "Openbrand"
labels = json.load(open('../' + dataset_name + '/openBrand_testA_list.json', 'r'))
file_id = {i['file_name']:i['id'] for i in labels}
path = "../"
results = json.load(open(path + 'best_predictions_epoch5.json', 'r'))
print(len(results))
# exit()
new_results = []
for i in tqdm(range(len(results))):
    if results[i]['score'] < 0.02:
        continue

    results[i]['image_id'] = file_id[results[i]['image_id']+'.jpg']
    results[i]['bbox'] = [round(i) for i in results[i]['bbox']]
    new_results.append(results[i])

json.dump(new_results, open(path + 'best_predictions_epoch5_id_round.json','w'))