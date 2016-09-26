import json
import subprocess
import pprint
import datetime 

class Kostenio():


    def __init__(self, filename):
        now = datetime.datetime.now()
        self.filename = filename + datetime.datetime.now().strftime('%m-%Y') + '.json'

    def loadValues(self, date=''):
        try:
            f = open(self.filename, 'r')
            # almostJSON = f.read()
            JSON = f.read()
            f.close()
            # almostJSON = almostJSON[:-2]
            # pp = pprint.PrettyPrinter(indent=4)
            # pp.pprint(almostJSON)
            # JSON = '{' + almostJSON + '}'
            x = json.loads(JSON)
        except FileNotFoundError:
            x = '<p>Datei nicht gefunden</p>'

        return x

    def getKey(self):
        try:
            line = subprocess.check_output(['tail', '-1', self.filename])
            print('{' + str(line)[2:-4] + '}')
            x = json.loads('{' + str(line)[2:-4] + '}')
            key = int(list(x).pop()) + 1
        except subprocess.CalledProcessError:
            key = 1
        except IndexError:
            key = 1

        return key;

    def storeValues(self, values):
        # try:
            # f = open(self.filename, 'r')
            # old = json.loads(f.read())
            # # Append new data to the existing ones
            # for k,v in old.items():
                # count = len(v)
                # for k2,v2 in v.items():
                    # values[k][count] = v2
            # f.close()
        # except FileNotFoundError:
            # # Nothing
            # k=1;

        f = open(self.filename, 'w')
        f.write(json.dumps(values))
        f.close()

