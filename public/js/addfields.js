function addFields(){
	// Number of inputs to create
	var number = document.getElementById("counter").value;
	// Container <div> where dynamic content will be placed
	var container = document.getElementById("container");
	// Clear previous contents of the container
	number =  parseInt(number) + 1;
	document.getElementById("counter").value = number;

	var section = document.getElementById("container").appendChild(document.createElement("section"));
	section.setAttribute('id', 'line' + number);
	
	var betrag = section.appendChild(document.createElement("input"));
	betrag.setAttribute('type', 'text');
	betrag.setAttribute('name', "betrag" + number);
	betrag.setAttribute('class', 'betrag');

	var bezeichnung = section.appendChild(document.createElement("input"));
	bezeichnung.setAttribute('type', 'text');
	bezeichnung.setAttribute('name', "bezeichnung" + number);
	bezeichnung.setAttribute('class', 'bezeichnung');

	var datum = section.appendChild(document.createElement("input"));
	datum.setAttribute('type', 'text');
	datum.setAttribute('name', 'datum' + number);
	datum.setAttribute('class', 'datepicker');

	var typ = section.appendChild(document.createElement("input"));
	typ.setAttribute('type', 'text');
	typ.setAttribute('name', 'typ' + number);
	typ.setAttribute('class', 'typ');

	var button = section.appendChild(document.createElement("button"));
	button.setAttribute('type', 'button');
	button.setAttribute('id', 'button' + number);
	button.setAttribute('onclick', 'deleteLine(' + number + ')');
	button.appendChild(document.createTextNode('Delete'));

	//document.getElementById("container").appendChild(document.createElement("br"));
	section.appendChild(document.createElement("br"));

	$( ".datepicker" ).datepicker({
		altFormat: "dd-mm-yy"
	});
	$.datepicker.setDefaults( $.datepicker.regional["de"]);
}
