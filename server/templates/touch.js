$(document).ready(function(){

	var obj1 = document.getElementById('g1');
	
	obj1.addEventListener('touchstart', function(event) {
		event.preventDefault();
                if (event.targetTouches.length == 1) {
			obj1.style.backgroundColor = "#F9D654";
		}
	}, false);

	obj1.addEventListener('touchend', function(event) {
		event.preventDefault();
		obj1.style.backgroundColor = "#F9E5CC";		
        }, false);

        var obj2 = document.getElementById('g2');

        obj2.addEventListener('touchstart', function(event) {
                event.preventDefault();
                if (event.targetTouches.length == 1) {
                        obj2.style.backgroundColor = "#F9D654";
                }
        }, false);

        obj2.addEventListener('touchend', function(event) {
                event.preventDefault();
                obj2.style.backgroundColor = "#F9E5CC";
        }, false);

        var obj3 = document.getElementById('g3');

        obj3.addEventListener('touchstart', function(event) {
                event.preventDefault();
                if (event.targetTouches.length == 1) {
                        obj3.style.backgroundColor = "#F9D654";
                }
        }, false);

        obj3.addEventListener('touchend', function(event) {
                event.preventDefault();
                obj3.style.backgroundColor = "#F9E5CC";
        }, false);


});

