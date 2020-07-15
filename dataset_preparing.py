import pandas as pd
import json
import re

import config

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

def normalize(text):
    text_lower = text.lower()
    text_cpecial_characterless = re.sub("""[^0-9a-zA-ZА-Яа-я]+""", ' ', text_lower)
    text_spaceless = re.sub('\\s+', ' ', text_cpecial_characterless)
    return text_spaceless


toloka_result = pd.read_json(config.toloka_result_json)
del toloka_result['link']

toloka_result['text'] = toloka_result['text'].apply(normalize)
toloka_result = toloka_result.loc[
    (toloka_result['text'] != '') & (toloka_result['text'] is not None) & (toloka_result['is_wolf'])
].drop_duplicates()

del toloka_result['is_wolf']

dataset = toloka_result.to_dict(orient='records')
with open(config.dataset_json, 'w') as file:
    file.write(json.dumps(dataset, ensure_ascii=False, indent=2))
