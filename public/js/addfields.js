function addFields(){
	// Number of inputs to create
	var number = document.getElementById("counter").value;
	// Container <div> where dynamic content will be placed
	var container = document.getElementById("container");
	// Clear previous contents of the container
	number =  parseInt(number) + 1;
	document.getElementById("counter").value = number;

	var table = document.getElementById("table").getElementsByTagName("tbody")[0];
	var newRow = table.insertRow();
	newRow.setAttribute('id', 'line' + number);
	
	var newCell = newRow.insertCell();
	var betrag = newCell.appendChild(document.createElement("input"));
	betrag.setAttribute('type', 'text');
	betrag.setAttribute('name', "betrag" + number);
	betrag.setAttribute('class', 'betrag');
	betrag.setAttribute('form', 'werte');

	var newCell = newRow.insertCell();
	var bezeichnung = newCell.appendChild(document.createElement("input"));
	bezeichnung.setAttribute('type', 'text');
	bezeichnung.setAttribute('name', "bezeichnung" + number);
	bezeichnung.setAttribute('class', 'bezeichnung');
	bezeichnung.setAttribute('form', 'werte');

	var newCell = newRow.insertCell();
	var typ = newCell.appendChild(document.createElement("input"));
	typ.setAttribute('type', 'text');
	typ.setAttribute('name', 'typ' + number);
	typ.setAttribute('class', 'typ');
	typ.setAttribute('form', 'werte');

	var newCell = newRow.insertCell();
	var datum = newCell.appendChild(document.createElement("input"));
	datum.setAttribute('type', 'text');
	datum.setAttribute('name', 'datum' + number);
	datum.setAttribute('class', 'datepicker');
	datum.setAttribute('form', 'werte');

	var newCell = newRow.insertCell();
	var button = newCell.appendChild(document.createElement("button"));
	button.setAttribute('type', 'button');
	button.setAttribute('id', 'button' + number);
	button.setAttribute('onclick', 'deleteLine(' + number + ')');
	button.appendChild(document.createTextNode('Delete'));

	$( ".datepicker" ).datepicker({
		altFormat: "dd-mm-yy"
	});
	$.datepicker.setDefaults( $.datepicker.regional["de"]);
}
