$(document).ready(function(){

	var obj = document.getElementById('g1');
	
	obj.addEventListener('touchstart', function(event) {
		event.preventDefault();
                if (event.targetTouches.length == 1) {
			obj.style.backgroundColor = "#F9D654";
		}
	}, false);

	obj.addEventListener('touchend', function(event) {
		event.preventDefault();
		obj.style.backgroundColor = "#F9E5CC";		
        }, false);
/*
	obj.addEventListener('touchmove', function(event) {
		event.preventDefault();
		if (event.targetTouches.length == 1) {
			//alert("bkj");
			var touch = event.targetTouches[0];
			obj.style.left = touch.pageX + 'px';
			obj.style.top = touch.pageY + 'px';
		}
	}, false);
*/

});

