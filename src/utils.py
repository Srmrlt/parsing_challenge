import json
import os

import requests
from lxml import etree


class ScanXML:
    def __init__(self):
        self.response = None
        self.file_path = "temp.xml"
        self.json_file_path = 'xml_structure.json'

    def get_data(self):
        url = os.getenv("URL")
        headers = {'Accept-Encoding': 'identity'}
        self.response = requests.get(url, stream=True, headers=headers)
        print(f"{self.response.status_code=}")

    def save_data(self, chunk_size_mb=1):
        self.get_data()
        if self.response.status_code == 200:
            with open(self.file_path, 'wb') as temp_file:
                for chunk in self.response.iter_content(chunk_size=1024 * 1024 * chunk_size_mb):
                    temp_file.write(chunk)

    def list_xml_structure_from_file(self):
        stack = []
        root_structure = {}
        context = etree.iterparse(self.file_path, events=('start', 'end'))

        for event, elem in context:
            if event == 'start':
                new_structure = {}

                if not stack:
                    root_structure[elem.tag] = new_structure
                else:
                    # Добавляем новый элемент к последнему элементу в стеке
                    stack[-1][1][elem.tag] = new_structure

                stack.append((elem.tag, new_structure))
            elif event == 'end':
                # Проверяем, не закончился ли текущий элемент
                if stack and stack[-1][0] == elem.tag:
                    stack.pop()

        self.save_json(root_structure)

    def save_json(self, data):
        with open(self.json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
