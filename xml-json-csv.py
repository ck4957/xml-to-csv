import json
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import xmltodict

file_name = 'fest251.xml'
op_json = 'xml_to_json.json'


def flatten_json(nested_json: dict, exclude: list=['']) -> dict:
    """
    Flatten a list of nested dicts.
    """
    out = dict()
    def flatten(x: (list, dict, str), name: str='', exclude=exclude):
        if type(x) is dict:
            for a in x:
                if a not in exclude:
                    flatten(x[a], f'{name}{a}_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, f'{name}{i}_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out

def convert_to_json():
    with open(file_name, encoding='utf-8') as xml_file:
        data_dict = xmltodict.parse(xml_file.read())

    json_data = json.dumps(data_dict)
    with open(op_json, "w") as json_file:
        json_file.write(json_data)

def convert_to_csv():
    # First convert_to_json
    convert_to_json()
    # read json
    with open(op_json, encoding='utf-8') as f:
        data = json.loads(f.read())

    # create dataframe
    main_set = data["FEST"]
    for item in main_set:
        sub_item = main_set[item]
        if type(sub_item) is dict:
            for key in sub_item.keys():
                df = pd.DataFrame(flatten_json(x) for x in sub_item[key])    
                df.to_csv(f"Output_{item}.csv", index=False)
convert_to_csv()
#start()