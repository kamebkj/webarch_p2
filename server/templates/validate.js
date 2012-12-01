$(document).ready(function(){

	$("#custom").bind('input', function() {
		if ($("#custom").val().match(/^[a-zA-Z]*$/)==null) {
			$("#button").attr('disabled', true);
                	$("#warnmsg").text("Please enter only letters");
        	}
        	else {
               	 	$("#button").attr('disabled', false);
               	 	$("#warnmsg").text("");
        	}
	});

	$("#button").on("click", function() {
		var origin = $("#origin").val();
		if (origin.length==0) {
			alert("Please enter a URL.");
			return false;
		}	
	});

});

