function addFields(){
	// Number of inputs to create
	var number = document.getElementById("counter").value;
	// Container <div> where dynamic content will be placed
	var container = document.getElementById("container");
	// Clear previous contents of the container
	number =  parseInt(number) + 1;
	document.getElementById("counter").value = number;

	var betrag = document.getElementById("container").appendChild(document.createElement("input"));
	betrag.setAttribute('type', 'text');
	betrag.setAttribute('name', "betrag" + number);

	var bezeichnung = document.getElementById("container").appendChild(document.createElement("input"));
	bezeichnung.setAttribute('type', 'text');
	bezeichnung.setAttribute('name', "bezeichnung" + number);

	var datum = document.getElementById("container").appendChild(document.createElement("input"));
	datum.setAttribute('type', 'text');
	datum.setAttribute('name', 'datum' + number);
	datum.setAttribute('class', 'datepicker');

	document.getElementById("container").appendChild(document.createElement("br"));

	$( ".datepicker" ).datepicker({
		altFormat: "dd-mm-yy"
	});
	$.datepicker.setDefaults( $.datepicker.regional["de"]);
}
