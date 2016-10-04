# -*- coding: utf-8 -*-
import os 
import os.path
from src.kostenio import Kostenio

import cherrypy

class Page():
    def header(self):
        try:
            da = self.title
        except AttributeError:
            self.title = 'Kostenuebersicht'
        try:
            da = self.autocomplete
        except AttributeError:
            self.autocomplete = ''
            
        return """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>%s</title>
    <link rel="stylesheet" href="/static/css/main.css";
    <link rel="stylesheet" href="https://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
    <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
    <script src="/static/js/addfields.js"></script> 
    <script src="/static/js/datepicker.js"></script>
    <script src="/static/js/deleteline.js"></script>
    <script type"text/javascript">%s</script>
</head>
<body>
<div class="main">
""" % (self.title, self.autocomplete)

    def footer(self):
        return """
</div>
</body>
</html>
"""

    def back(self, path):
        return '<a href=' + path + '>back</a>'


class Kosten(Page):

    localDir = os.path.dirname(__file__)
    absDir = os.path.join(os.getcwd(), localDir)
    kostenio = Kostenio(absDir+"/src/data/")

    @cherrypy.expose
    def index(self, **kwargs):
        self.createAutocomplete()
        self.title = 'Start'
        counter = 0
        # Start
        form2 = '<div id="content">'
        form2 += '<table id="table"><tr>'
        form2 += '<th>Betrag</th>'
        form2 += '<th>Bezeichnung</th>'
        form2 += '<th>Typ</th>'
        form2 += '<th>Datum</th>'
        form2 += '<th> </th>'
        form2 += '</tr>'
        # form2 += '<fieldset id="container">'
        vals = self.kostenio.loadValues()

        if vals == -1:
            vals = {'betrag': {'1':''}, 'bezeichnung': {'1':''}, 'datum': {'1':''}, 'typ': {'1':''}}

        for i in vals['betrag'].keys():
            counter += 1
            value = dict()
            for k in vals.keys():
                try:
                    value[k] = vals[k][str(i)]
                except:
                    value[k] = ''

            # form2 += '<section id="line%d">' % (counter)
            form2 += '<tr id="line%d">' % (counter)
            for l in ['betrag', 'bezeichnung', 'typ']:
                form2 += '<td>'
                form2 += '<input type="text"'
                form2 += 'name="%s%s"' %(l, counter)
                form2 += 'value="%s"' %(value[l])
                form2 += 'id="%s%s"' %(l,counter)
                form2 += 'class="%s"' %(l)
                form2 += 'form="werte"'
                form2 += '></td>'
            # form2 += '<input type="text" name="betrag%s" value="%s" id="betrag%s" class="betrag" form=>' % (
                    # counter,value['betrag'],counter)
            # form2 += '<input type="text" name="bezeichnung%s" value="%s" id="bezeichnung%s" class="bezeichnung">' % (
                    # counter,value['bezeichnung'], counter)
            form2 += '<td><input type="text" class="datepicker" name="datum%s" value="%s" id="date%s" form="werte"></td>' % (counter,value['datum'],counter)
            # form2 += '<input type="text" name="typ%s" value="%s" id="typ%s" class="typ">' % (
                    # counter,value['typ'], counter)
            form2 += '<td><button type="button" id="deletebutton" onclick="deleteLine(%s)">Delete</button></td>' % (
                    counter)
            # form2 += '</section>'
            form2 += '</tr>'

        # form2 +='</fieldset>'
        form2 += '</table>'
        form2 += '<form action="save" method="GET" id="werte">'
        form2 += '<input type="submit" value="submit">'
        form2 += '<button type="button" onclick="addFields()">Neue Zeile</button>'
        form2 += '</form>'
        form2 += '</div>'

        hiddencounter = '<input type="hidden" value="%s" id="counter">' % (counter)
        content = self.header() + hiddencounter + form2 + self.sidebar() + self.footer()
        
        return content

    def sidebar(self):
        aside = '<aside></aside'
        sidebar = '<div id="sidebar">'
        sidebar += '<a href="/">Input</a><br>'
        sidebar += '<a href="/displayPie">Statistik</a><br>'
        sidebar += '</div>'

        return sidebar

    @cherrypy.expose
    def save(self, **kwargs):
        print("save")
        import pprint
        pprint.pprint(kwargs)
        content = ''
        cont = {}
        betrag = {}
        bezeichnung = {}
        datum = {}
        typ = {}
        for k in kwargs:
            content += '%s => %s<br>' % (k,kwargs[k])
            # cont[k[:-1]].update({k[-1:]: kwargs[k]})
            if k[:-1] == 'bezeichnung' and kwargs[k] != '':
                bezeichnung[k[-1:]] = kwargs[k]
            if k[:-1] == 'datum' and kwargs[k] != '':
                datum[k[-1:]] = kwargs[k]
            if k[:-1] == 'betrag' and kwargs[k] != '':
                betrag[k[-1:]] = kwargs[k]
            if k[:-1] == 'typ' and kwargs[k] != '':
                typ[k[-1:]] = kwargs[k]

            cont['bezeichnung'] = bezeichnung
            cont['datum'] = datum
            cont['betrag'] = betrag
            cont['typ'] = typ

        self.kostenio.storeValues(cont)
        # Leitet einen direkt wieder weiter zu startseite
        return '<html><head><meta http-equiv="refresh" content="0;  /"/></head></html>'

    @cherrypy.expose
    def displayPie(self, pie='', date=''):
        import matplotlib.pyplot as plt
        import numpy as np
        self.title = 'Select Graph'
        dates = os.listdir(self.absDir + '/src/data/')

        content = '<section id="selectPie">'
        content += '<table>'
        for dt in dates:
            if date[-5:] == '.json':
                content += '<tr><td>'
                content += '%s: ' %(dt[:-5])
                content += '''<button type="button" onclick="location.href = '/displayPie?pie=lines&date=%s'">
                Lines</button>''' %(dt[:-5])
                content += '''<button type="button" onclick="location.href = '/displayPie?pie=typ&date=%s'">
                Typ</button>''' %(dt[:-5])
                content += '''</td></tr>'''
        content += '</table></section>'

        pieType = ''
        if pie == 'lines' :
            pieType = 'bezeichnung'
        elif pie == 'typ':
            pieType = 'typ'

        if pieType != '':
            content = self.createPie(plt, np, pieType, date)
        

        return self.header() + self.sidebar() + content + self.footer()

    # Creates a pie chart for the given name values
    def createPie(self, plt, np, name, date):
        entries = self.kostenio.loadValues(date + '.json')

        categorys = list()
        tmp = dict()

        for i in entries[name].keys():
            if entries[name][str(i)] in tmp.keys():
                tmp[entries[name][str(i)]] += float(entries['betrag'][str(i)].replace(',','.'))
            else:
                tmp[entries[name][str(i)]] = float(entries['betrag'][str(i)].replace(',','.'))

            categorys.append(entries[name][str(i)])
            
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
        content += self.back('/displayPie')+'</body></html>'

        return content

    # Create JS autocomplete Lists and Functions
    def createAutocomplete(self):
        vals = self.kostenio.loadValues()
        self.autocomplete = ''
        tags = dict()
        for u in ['typ']:
            li = []
            try:
                for v in vals[u].values():
                    w = v.split(',')
                    for x in w:
                        y = '"%s"' % (x)
                        if not y in li:
                            li.append(y)
                            print(y)

                tags[u] = ','.join(li)
            except:
                tags[u] = ''

            self.autocomplete += '''
            $(function() {
                var %sTags = [
                    %s
                ];
                $(".%s").autocomplete({
                    source: %sTags
                });
            });
            ''' % ( u, tags[u], u, u )

        # li = []
        # try:
            # for v in vals['typ'].values():
                # w = '"%s"' % (v)
                # if not w in li:
                    # li.append(w)
                    # print(w)

            # typTags = ','.join(li)
        # except:
            # typTags = ''


        # self.autocomplete += '''
        # $(function() {
            # var typTags = [
                # %s
            # ];
            # $(".typ").autocomplete({
                # source: typTags
            # });
        # });
        # ''' % ( typTags )

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
