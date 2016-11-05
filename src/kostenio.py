import json
import subprocess
import pprint
import datetime 

class Kostenio():


    def __init__(self, path, typ, month='curr'):
        now = datetime.datetime.now()
        self.path = path
        if typ == 'ausgaben':
            self.filename = path + datetime.datetime.now().strftime('%m-%Y') + '.json'
        else:
            self.filename = path + 'konten.json'

    def listAusgaben(self):
        ausgaben = subprocess.check_output(['ls', '%s' %(self.path)]) 
        ausgaben = ausgaben.decode('utf-8')
        ausgaben = ausgaben.split('\n')
        ret = list()
        for b in ausgaben:
            if "-" in b:
               ret.append(b) 
        pprint.pprint(ret)
        return ret

    def loadValues(self, filename=''):
        if filename == '':
            filename = self.filename
        else:
            filename = self.path + filename
        try:
            print("Filename")
            pprint.pprint(filename)
            f = open(filename, 'r')
            JSON = f.read()
            f.close()
            x = json.loads(JSON)
        except FileNotFoundError:
            x = -1

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

    def storeValues(self, values, filename=''):
        if filename == '':
            filename = self.filename
        else:
            filename = self.path + filename

        try:
            f = open(filename, 'w')
            f.write(json.dumps(values,False,True,True,True,None,3))
            f.close()
            success = 1
        except:
            success = -1

        return success

