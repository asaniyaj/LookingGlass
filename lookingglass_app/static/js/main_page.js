$(document).ready(function() {
	$("#quest-form").submit(function(e){
		e.preventDefault();
  		serializedData = $("#quest-form").serialize();
  		if (typeof $('#main_text').val() === undefined) {
  			alert("No text entered");
  		}
  		else{
	  		var text_to_send = $('#main_text').val();
	  		$.ajax({
	    		type:"POST",
	    		url: "/",
	    		data: serializedData,
	    		dataType: "json",
	    		success: function(data) {
	    			$("#quest-box").addClass("col-lg-6");
	    			$("#main_text").css("height", "800px");
	    			$("#quest-box").css("height", "1000px");
	    			// $("#image-container").addClass("col-lg-5");
	    			$("#quest-image").html('');
	    			$("#quest-image").append('<div id="wrapper"><div id="columns">');
	    			jQuery.each(data.images, function(index, value){
            			$("#quest-image #wrapper #columns").append('<div class="pin"><img src="' + value + '" /></h3><p> image,image </p></div>');
    					// $("#image-container").append('<img src="' + value + '" />');
    					// $("#image-container").append('</h3><p> image,image </p></div></div></div>');
        			});
	    			// alert( data.images );
	    			// $("#image-container #test-wrap").append('here');
	    			// $("#image-container #test-wrap").append(data.images);
	    			$('.pin').dblclick(function(){
						// alert('here');
  						alert($(this).children('img').attr('src'));
					});
	    		}
	 		});
		
		}
	});

	$('.pin').dblclick(function(){
		alert('here');
  		// alert($(this).children('img').attr('src'));
	});
});