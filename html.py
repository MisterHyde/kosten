class Page():
    tabs = 0
    listNames = ''
    listContent = ''
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
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>%s</title>
    <link rel="stylesheet" href="/static/css/main.css";
    <link rel="stylesheet" href="/static/css/jquery-ui.css">
    <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
    <script src="/static/js/addfields.js"></script> 
    <script src="/static/js/datepicker.js"></script>
    <script src="/static/js/deleteline.js"></script>
    <script type="text/javascript">%s</script> <!-- Insert autocomplete here -->
    <script type="text/javascript">
	$( function() {
	    $( "#tabs").tabs();
	});
    </script> 
</head>
<body>
<div class="main">
""" % (self.title, self.autocomplete)


    def tabsDiv(self):
        return """
        <div id="tabs">
            <ul>
            %s
            </ul>
            %s
        </div>
        """ %( self.listNames, self.listContent )


    def footer(self):
        return """
</div>
</body>
</html>
"""


    def back(self, path):
        return '<a href=' + path + '>back</a>'


    def addEntry(self, content, name):
        self.tabs += 1
        self.listNames += """<li><a href="#tabs-%u">%s</a></li>
        """ %(self.tabs, name)
        self.listContent += """<div id="tabs-%u">
        %s
        </div>
        """ %(self.tabs, content)

    def emptyEntries(self):
        self.tabs = 0
        self.listNames = ''
        self.listContent = ''



# class Ausgaben():
    # def __init__(self, cnames, cdatas):
        # self.table = """<table style="width:100%">
        # <tr>
            # <th>Betrag</th>
            # <th>Was</th>
            # <th>Typ</th>
            # <th>Datum</th>
            # <th> </th>
        # </tr>
        # """
        # for i in range(1, len(cdatas['betrag'])+1):
            # self.table += """<tr>
            # <td>%s</td>
            # <td>%s</td>
            # <td>%s</td>
            # <td>%s</td>
            # <td><button type="button" id="deletebutton" onclick"deleteLine(%s)">Delete</button></td>
            # </tr>
            # """ %(cdatas['betrag'][i], cdatas['bezeichnung'][i], cdatas['typ'][i], cdatas['datum'][i], i)

        # self.table += "</table"
        



