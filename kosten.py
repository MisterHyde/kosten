# -*- coding: utf-8 -*-
import re
import os 
import os.path
import pprint
import datetime
from src.kostenio import Kostenio
from html import Page

import cherrypy

# TODO Cover also the amount on the bank account
# TODO A better way to insert and display datas ( maybe like an excel sheet with different tabs and a table )


class Kosten(Page):

    def __init__(self):
        self.localDir = os.path.dirname(__file__)
        self.absDir = os.path.join(os.getcwd(), self.localDir)
        self.ausgabenDB = Kostenio(self.absDir+"src/data/", 'ausgaben')
        self.kontenDB = Kostenio(self.absDir+"src/data/", 'konten')
        self.debug = True

    def tabAusgaben(self, monat=''):
        # self.emptyEntries()
        vals = self.ausgabenDB.loadValues(monat)
        self.log(vals)
        table = """<table id='table'>
        <tr>
            <th class=bord>Betrag</th>
            <th class=bord>Was</th>
            <th class=bord>Typ</th>
            <th class=bord>Datum</th>
            <th> </th>
        </tr>
        """
        # TODO linebreak if the content of the 'Was' row cell is to long
        # TODO Sort entries by date
        # Counter is an index for the rows because the javascript function which inserts new lines isn't
        # consistent in the creation of new indices
        counter = 1
        # If no file exists then create an empty row else fill the table with the entries
        if isinstance(vals, dict) or (not isinstance(vals, int) and (len(vals['betrag']) == 0)):
            for i in vals['betrag'].keys():
                table += """<tr id=line%s>""" %(counter)
                table += """
                <td class=bord><input class="betrag" name="betrag%s" type="text" value="%s"></td>""" %(
                        counter, vals['betrag'][i])
                table += """
                <td class=bord><input class="bezeichnung" name="bezeichnung%s" type="text" value="%s"></td>""" %(
                        counter, vals['bezeichnung'][i])
                table += """
                <td class=bord><input class="typ" name="typ%s" type="text" value="%s"></td>""" %(counter, vals['typ'][i])
                table += """
                <td class=bord><input type="text" class="datepicker" name="datum%s" value="%s" id="date%s"></td>""" %(
                        counter, vals['datum'][i], counter)
                table += """
                <td><button type="button" id="deletebutton" onclick"deleteLine(%s)">Delete</button></td>
                </tr>""" %(counter)
                counter += 1

        else:
            table += """<tr id=line%s>""" %(counter)
            table += """
            <td class=bord><input class="betrag" name="betrag%s" type="text"></td>""" %(
                    counter)
            table += """
            <td class=bord><input class="bezeichnung" name="bezeichnung%s" type="text"></td>""" %(
                    counter)
            table += """
            <td class=bord><input class="typ" name="typ%s" type="text"></td>""" %(counter)
            table += """
            <td class=bord><input type="text" class="datepicker" name="datum%s" id="date%s"></td>""" %(
                    counter, counter)
            table += """
            <td><button type="button" id="deletebutton" onclick"deleteLine(%s)">Delete</button></td>
            </tr>""" %(counter)

        table += "</table>"

        buttons = '<button type="button" onclick="addRow()">Neue Zeile</button>'
        buttons += '<input type="submit" value="submit" form="werte">'
        # Create dropdown menu for choosing another month
        buttons += '<select style="margin-left:20px" form="monat" name="monat">'
        last = len(self.ausgabenDB.listAusgaben())
        count = 1
        if last != 0:
            for b in self.ausgabenDB.listAusgaben():
                buttons += '<option value="%s" form="monat" name="monat"' %(b)
                # Select the fitting select entry
                if (b == monat) or ((monat == '') and (count == last)):
                    buttons += ' selected="selected" '
                buttons += '>%s</option>' %(b)
                count += 1
        # If no entry available use the current month
        else:
            buttons += '<option value="%s.json" form="monat" name="monat">%s</option>' %(
                    datetime.datetime.now().strftime('%m-%Y'), datetime.datetime.now().strftime('%m-%Y'))
        buttons += '</select>'
        buttons += '<input type="submit" value="refresh" form="monat">'
        if monat == '':
            monat = datetime.datetime.now().strftime('%m-%Y') + ".json"
        hiddencounter = '<input type="hidden" value="%s" id="counter">' % (counter)
        forms = '<form action="save" method="POST" name="werte"><input type="hidden" value="%s" id="werte">%s</form>' %(monat, hiddencounter)
        forms += '<form action="index" method="POST" id="monat">%s</form>' %(hiddencounter)

        return buttons + hiddencounter + forms + table


    def tabKonten(self):
        vals = self.kontenDB.loadValues()
        edit = '<div id="edit">'
        edit += '<button id="newDepo" onclick="newDepo()"></button>'
        edit += '</div>'

        uebersicht = edit
        auszug = ''

        konten = Page()
        konten.addEntry(uebersicht, "Übersicht")
        konten.addEntry(auszug, "Auszüge")

        return konten.tabsDiv()

    def tabGraphen(self):
        blub = 'Sonnenblumen verhangene Genitalien.'
        return blub

    @cherrypy.expose
    def index(self, **kwargs):
        self.log('index()')
        self.log(kwargs)
        self.emptyEntries()

        if kwargs == {}:
            self.addEntry(self.tabAusgaben(), "Ausgaben")
        else:
            self.addEntry(self.tabAusgaben(kwargs['monat']), "Ausgaben")
        
        self.addEntry(self.tabKonten(), "Konten")
        self.addEntry(self.tabGraphen(), "Graphen")
        
        return self.header() + self.tabsDiv() + self.footer()


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
        content = ''
        cont = {'bezeichnung':{}, 'datum':{}, 'betrag':{}, 'typ':{}}
        betrag = {}
        bezeichnung = {}
        datum = {}
        typ = {}
        for k in kwargs:
            content += '%s => %s<br>' % (k,kwargs[k])
            for typename in ['bezeichnung', 'datum', 'betrag', 'typ']:
                if (typename in k) and (kwargs[k] != ''):
                    cont[typename][re.sub(typename, '', k)] = (kwargs[k])

        self.ausgabenDB.storeValues(cont,kwargs['monat'])
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
        entries = self.ausgabenDB.loadValues(date + '.json')

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
        vals = self.ausgabenDB.loadValues()
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

    def log(self, msg):
        if self.debug:
            pprint.pprint(msg)

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

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
