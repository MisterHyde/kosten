function deleteLine(pId){
	if(window.confirm('Wirklich löschen?')){
		$("#line" + pId).remove();	
	}
}
