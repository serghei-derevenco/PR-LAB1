import csv
import json
import yaml
import requests
import xmltodict
from request_data import get_data

def parse_data():
    results = get_data()
    server_data = []

    for element in results:
        if 'mime_type' in element:
            if element['mime_type'] == 'application/xml':
                xml_data = element["data"]
                xml_reader = json.loads(json.dumps(xmltodict.parse(xml_data, process_namespaces=True)))
                server_data.append(xml_reader["dataset"]["record"])

            elif element['mime_type'] == 'application/x-yaml':
                yaml_data = element["data"]
                server_data.append(json.loads(json.dumps(yaml.safe_load(yaml_data))))

            elif element['mime_type'] == 'text/csv':
                csv_data = element["data"]
                csv_reader = csv.DictReader(csv_data.split('\n'), delimiter=',')
                server_data.append(json.loads(json.dumps([row for row in csv_reader])))
        else:
            if ',]' in element["data"]:
                replace = str(element["data"]).replace(',]', ']')
                server_data.append(json.loads(replace))
            else:
                server_data.append(json.loads(element["data"]))

    with open('data.json', 'w') as f:
        json.dump(server_data, f)

def select_from_file(query):
    with open('data.json') as json_file:
        data = json.load(json_file)

    if 'select' in query:
        query_values = query.replace('select', '').split()
        results = []
        for element in data:
            for row in element:
                result_row = dict()
                for query in query_values:
                    if query in row:
                        result_row[query] = row[query]
                if result_row:
                    results.append(result_row)
        return json.dumps(results)
    else:
        return json.dumps(data)
                    