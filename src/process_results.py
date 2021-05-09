import json
import glob
from tqdm import tqdm
dataset_name = "Openbrand"
labels = json.load(open('../' + dataset_name + '/openBrand_testA_list.json', 'r'))
file_id = {i['file_name']:i['id'] for i in labels}
paths = glob.glob('../test/*/')
for path in paths:
    # path = "../baseline_5x_epoch_11_val_0.506/"
    results = json.load(open(path + 'best_predictions.json', 'r'))
    print(len(results))
    # exit()
    new_results = []
    for i in tqdm(range(len(results))):
        # if results[i]['score'] < 0.04:
        #     continue

        results[i]['image_id'] = file_id[results[i]['image_id']+'.jpg']
        results[i]['bbox'] = [round(i) for i in results[i]['bbox']]
        new_results.append(results[i])

    json.dump(new_results, open(path + 'submit_result.json','w'))