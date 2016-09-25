import os.path
from src.kostenio import Kostenio
import pprint as pprint

import cherrypy

class Page():
    def header(self):
        title = 'Kostenrechner'
        return """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>%s</title>
    <link rel="stylesheet" href="/static/css/main.css";
    <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
    <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
    <script src="/static/js/addfields.js"></script> 
    <script src="/static/js/datepicker.js"></script>
    <script src="/static/js/deleteline.js"></script>
</head>
<body>
<!--<script>$.session.set("counter", 1)</script>-->
""" % (title)

    def footer(self):
        return """
</body>
</html>
"""

    def back(self, path):
        return '<a href=' + path + '>back</a>'


class Kosten(Page):

    localDir = os.path.dirname(__file__)
    absDir = os.path.join(os.getcwd(), localDir)
    kostenio = Kostenio(absDir+"/src/test")

    @cherrypy.expose
    def index(self, **kwargs):
        self.title = 'Start'
        counter = 0
        # Start
        form2 = '<form action="save" method="GET" id="werte">'
        form2 += '<fieldset id="container">'
        vals = self.kostenio.loadValues()
        # for i in range(1, len(vals['bezeichnung'])):
        for i in vals['bezeichnung'].keys():
            counter += 1
            betrag = vals['betrag'][str(i)]
            bezeichnung = vals['bezeichnung'][str(i)]
            datum = vals['datum'][str(i)]
            form2 += '<div id="line%s">' % (counter)
            form2 += '<input type="text" name="betrag%s" value="%s" id="betrag%s" class="line%s">' % (counter,betrag,counter,counter)
            form2 += '<input type="text" name="bezeichnung%s" value="%s" id="bezeichnung%s" class="line%s">' % (counter,bezeichnung, counter,counter)
            form2 += '<input type="text" class="datepicker" name="datum%s" value="%s" id="date%s" class="line%s">' % (counter,datum,counter,counter)
            form2 += '<button type="button" id="deletebutton" onclick="deleteLine(%s) class="line%s"">Delete</button><br>' % (counter,counter)
            form2 += '</div>'

        form2 +='</fieldset>'
        form2 +='<label for="betrag1"></label>'
        form2 +='<label for="bezeichnung1"></label>'
        form2 +='<label for="date1"></label>'
        form2 += '<input type="submit" value="submit">'
        form2 += '<button type="button" onclick="addFields()">Neue Zeile</button>'
        form2 += '</form>'

        # End
        hiddencounter = '<input type="hidden" value="%s" id="counter">' % (counter)
        form = '<form action="save" method="GET" id="werte">'
        form += '<fieldset id="container">'
        form += '<input type="text" name="betrag1" value="" id="betrag1">'
        form += '<input type="text" name="bezeichnung1">'
        form += '<input type="text" class="datepicker" name="datum1"><br>'
        form +=' </fieldset>'
        form += '<input type="submit" value="submit">'
        form += '<button type="button" onclick="addFields()">Neue Zeile</button>'
        form += '</form>'

        content = self.header() + hiddencounter
        # content += form
        content += form2 + self.footer()
        
        return content + self.footer()

    @cherrypy.expose
    def save(self, **kwargs):
        content = ''
        cont = {}
        betrag = {}
        bezeichnung = {}
        datum = {}
        for k in kwargs:
            content += '%s => %s<br>' % (k,kwargs[k])
            # cont[k[:-1]].update({k[-1:]: kwargs[k]})
            if k[:-1] == 'bezeichnung' and kwargs[k] != '':
                bezeichnung[k[-1:]] = kwargs[k]
            if k[:-1] == 'datum' and kwargs[k] != '':
                datum[k[-1:]] = kwargs[k]
            if k[:-1] == 'betrag' and kwargs[k] != '':
                betrag[k[-1:]] = kwargs[k]

            cont['bezeichnung'] = bezeichnung
            cont['datum'] = datum
            cont['betrag'] = betrag

        self.kostenio.storeValues(cont)
        # Leitet einen direkt wieder weiter zu startseite
        return '<html><head><meta http-equiv="refresh" content="0;  /"/></head></html>'

    @cherrypy.expose
    def displayPie(self):
        import matplotlib.pyplot as plt
        import numpy as np
        entries = self.kostenio.loadValues()
        categorys = list()
        tmp = dict()

        for i in entries['bezeichnung'].keys():
            print("\n\n");
            pprint.pprint(entries['bezeichnung']);
            print("\n\n");
            if entries['bezeichnung'][str(i)] in tmp.keys():
                tmp[entires['bezeichnung'][str(i)]] += float(entries['betrag'][str(i)])
            else:
                tmp[entries['bezeichnung'][str(i)]] = float(entries['betrag'][str(i)])

            categorys.append(entries['bezeichnung'][str(i)])
            
        vals = list()
        labels = list()
        for key, values in tmp.items():
            vals.append(tmp[key])
            labels.append(key)
        v = np.array(vals)
        l = np.char.array(labels)
        procent = (100.*v)/v.sum()
        patches, texts = plt.pie(v, startangle=90, radius=1.2)
        labels = ['{0} - {1:1.2f}% - {2}€'.format(i,j,k) for i,j,k in zip(l, procent, v)]
        patches, labels, dummy = zip(*sorted(zip(patches, labels, v), key=lambda l: l[2], reverse=True))
        plt.legend(patches, labels, loc='center left', bbox_to_anchor=(-0.1, 1.), fontsize=10)
        plt.savefig(self.absDir + '/public/img/tmp.png');
        content = '<!DOCTYPE html><html><body><img src="/static/img/tmp.png">'
        content += self.back('/')+'</body></html>'
        return content

tutconf = os.path.join(os.path.dirname(__file__), 'hallo.conf')

if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    config = {'global':
        {
            'server.socket_host': "127.0.0.1",
            'server.socket_port': 8080,
            'server.thread_pool': 10,
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static':
        {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': "./public"
        }
    }
    cherrypy.quickstart(Kosten(), '/', config=config)
