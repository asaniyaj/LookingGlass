$(document).ready(function() {
	// jQuery.noConflict();
	// var jq = jQuery;
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
	    			$("#main_text").css("height", "250px");
	    			$("#quest-box").css("height", "400px");
	    			// $("#image-container").addClass("col-lg-5");
	    			$("#quest-image").html('');
	    			$("#quest-image").append('<div id="wrapper"><div id="columns">');
	    			jQuery.each(data.images, function(index, value){
            			$("#quest-image #wrapper #columns").append('<div class="pin"><a href="' + value + '" ></a><img src="' + value + '" /></h3><p> image,image </p></div>');
    					// $("#image-container").append('<img src="' + value + '" />');
    					// $("#image-container").append('</h3><p> image,image </p></div></div></div>');
        			});	
     //    			$('.pin').click(function(){
					// 	alert($(this).children('img').attr('src'));
					// });

					$('.pin').click(function() {
						event.preventDefault();
						var url = $(this).children('img').attr('src');
						serurl = {"url": url};
						$.ajax({
							type:"POST",
				    		url: "reco/",
				    		data: serurl,
				    		dataType: "json",
				    		success: function(result) {
				    			$(".overlay .container #sign-image").append('<div class="pin"><a href="' + url + '" ></a><img src="' + url + '" /></h3></div>');
				    			jQuery.each(result.rimages, function(index, value){
            						$(".overlay .container #rem-image #wrapper1 #columns1").append('<div class="pin"><a href="' + value + '" ></a><img src="' + value + '" /></h3></div><a href="http://www.glamquotes.com/wp-content/uploads/2011/11/smile.jpg" download="Download.jpg"><input type="submit" id="download_btn" class=" btn btn-info" value="Download" /></a>');

    							});	
    							// $("div.overlay").toggle("slow");
    							$("div.overlay").fadeToggle({left: '250px'});
				    			// alert(result.rimages);
				    		}
						});
						
						// $("div.overlay").fadeToggle("fast");
					 //    $(this).animate({width: "400px"}, 'slow');
		
					});

				}
			});
	  	}
	});
	$('#close').click(function(){
		$("div.overlay").fadeToggle("slow");
		$(".overlay .container #rem-image #wrapper1 #columns1").empty();
		$(".overlay .container #sign-image").empty();
	});
    
	// $('.pin').dblclick(function(){
	// 	alert('here');
 //  		// alert($(this).children('img').attr('src'));
	// });
});