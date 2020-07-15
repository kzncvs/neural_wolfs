import pandas as pd
import json

import config

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

toloka_result = pd.read_csv(config.toloka_result_tsv, delimiter='\t')

del toloka_result['GOLDEN:output']
del toloka_result['GOLDEN:is_wolf']
del toloka_result['HINT:text']
del toloka_result['ACCEPT:verdict']
del toloka_result['ACCEPT:comment']

approved = toloka_result.loc[
    (toloka_result['ASSIGNMENT:status'] == 'APPROVED')
]
del approved['ASSIGNMENT:status']
approved = approved.rename(
    columns={
        "INPUT:image": "link",
        "OUTPUT:output": "text",
        "OUTPUT:is_wolf": "is_wolf"
    }
)
print(approved)
approved_dict = approved.to_dict(orient='records')
with open(config.toloka_result_json, 'w') as file:
    file.write(json.dumps(approved_dict, ensure_ascii=False, indent=2))
