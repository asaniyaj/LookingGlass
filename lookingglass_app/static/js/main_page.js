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
	    			$("#main_text").css("height", "280px");
	    			$("#quest-box").css("height", "430px");
	    			// $("#image-container").addClass("col-lg-5");
	    			$("#quest-image").html('');
	    			$("#quest-image").append('<div id="wrapper"><div id="columns">');
	    			jQuery.each(data.images, function(index, value){
            			$("#quest-image #wrapper #columns").append('<div class="pin"><img src="' + value + '" /><a href="' + value + '" ></a></div>');
    				});	
	    			reco_init();
 
				    			
				    	// 		$('.overlay .container #rem-image #wrapper1 #columns1 .pin').click(function() {
				    	// 			event.preventDefault();
				    	// 			var url = $(this).children('img').attr('src');
				    	// 			serurl = {"url": url};
				    	// 			$(".overlay .container #rem-image #wrapper1 #columns1").empty();
									// $(".overlay .container #sign-image").empty();
									// $.ajax({
									// 	type:"POST",
				    	// 				url: "reco/",
				    	// 				data: serurl,
				    	// 				dataType: "json",
				    	// 				success: function(result) {
				    	// 					$(".overlay .container #sign-image").append('<div class="pin"><img src="' + url + '" width=500px/><a href="' + url + '"  download="Download.jpg"><div><input type="submit" class=" download_btn btn btn-info center-block" value="Download" /></div></a></div>');
				    	// 					jQuery.each(result.rimages, function(index, value){
         //    									$(".overlay .container #rem-image #wrapper1 #columns1").append('<div class="pin"><img src="' + value + '" /><a href="' + value + '" ></a></div>');
    					// 					});
				    	// 				}
				    	// 			});

				    	// 		});
							// }	
						// });
					// });
				}
			});
	  	}
	});
	$('#close').click(function(){
		$("div.overlay").fadeToggle("slow");
		$(".overlay .container #rem-image #wrapper1 #columns1").empty();
		$(".overlay .container #sign-image").empty();
	});
    
  //   $('.overlay .container #rem-image #wrapper1 #columns1 .pin').click(function() {
  //   	event.preventDefault();
		// var url = $(this).children('img').attr('src');
		// serurl = {"url": url};
		// $(".overlay .container #rem-image #wrapper1 #columns1").empty();
		// $(".overlay .container #sign-image").empty();
		// ajaxd(serurl);
  //   });
    
});

function reco_init(){
	$('#quest-image #wrapper #columns .pin').click(function() {
		event.preventDefault();
		var url = $(this).children('img').attr('src');
		serurl = {"url": url};
		recod(url, serurl);
	});
}

function recod(url, serurl) {
		$.ajax({
		type:"POST",
		url: "reco/",
		data: serurl,
		dataType: "json",
		success: function(result) {
			$(".overlay .container #sign-image").append('<div class="pin"><img src="' + url + '" width=500px/><a href="' + url + '"  download="Download.jpg"><div><input type="submit" class=" download_btn btn btn-info center-block" value="Download" /></div></a></div>');
			jQuery.each(result.rimages, function(index, value){
				$(".overlay .container #rem-image #wrapper1 #columns1").append('<div class="pin"><img src="' + value + '" /><a href="' + value + '" ></a></div>');

			});	
			// $("div.overlay").toggle("slow");
			$("div.overlay").fadeToggle({left: '250px'});
			chain_reco_init();
			}
		});
}

function chain_reco_init() {
	$('.overlay .container #rem-image #wrapper1 #columns1 .pin').click(function() {
		event.preventDefault();
		var url = $(this).children('img').attr('src');
		serurl = {"url": url};
		$(".overlay .container #rem-image #wrapper1 #columns1").empty();
		$(".overlay .container #sign-image").empty();
		ajaxd(url, serurl);
	});
}

function ajaxd(url, serurl) {
		$.ajax({
			type:"POST",
			url: "reco/",
			data: serurl,
			dataType: "json",
			success: function(result) {
				$(".overlay .container #sign-image").append('<div class="pin"><img src="' + url + '" width=500px/><a href="' + url + '"  download="Download.jpg"><div><input type="submit" class=" download_btn btn btn-info center-block" value="Download" /></div></a></div>');
				jQuery.each(result.rimages, function(index, value){
					$(".overlay .container #rem-image #wrapper1 #columns1").append('<div class="pin"><img src="' + value + '" /><a href="' + value + '" ></a></div>');
				});
			}
	});			    		
}

