var url ='';


chrome.tabs.getSelected(null, function(tab) {
    //url = tab.url;
    //document.getElementById('currentLink').innerHTML = 'URL = '+tab.url;
    //encode_url = encodeURIComponent(url);
    //document.getElementById('encodedLink').innerHTML = 'Encoded URL = '+encode_url;

});



$(document).ready(function(){
	
	function hide_img() 
	{
	$("#wrapper").hide();
	}
    $("#reset").click(function(){
        //document.getElementById('test123').innerHTML = 'Search..... ';
		$("#wrapper").hide();
    });
    $("#btn").click(function(){
    //document.getElementById('test123').innerHTML = 'Call URI = '+encode_url;
	$("#wrapper").show();
    });
    hide_img();
});


