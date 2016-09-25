$( function() {
	$( ".datepicker" ).datepicker({
		altFormat: "dd-mm-yy"
	});
	$.datepicker.setDefaults( $.datepicker.regional["de"]);
});
//$('body').on('click', '.datepicker', function() {
	//var counter = document.getElementById("counter").value;
	//counter = parseInt(counter) + 1
	//var bezeichnung = "bezeichnung" + $counter
	//var betrag = "betrag" + $counter
	//var datum = "datum" + $counter
	//$(`<input type='text' name="$betrag"><input type="text" name="$bezeichnung"><input type="text"
		//name="$datum">`)
		//.appendTo("#werte");
//});
