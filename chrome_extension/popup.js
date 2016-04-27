var encode_url ='';

chrome.tabs.getSelected(null, function(tab) {
    url = tab.url;
    encode_url = encodeURIComponent(url);    
});


$(document).ready(function(){
	
	function hide_img() 
	{
	$("#wrapper").hide();
	}
    hide_img();
    
    $("#reset").click(function(){
        $('#columns').empty();
        $('#wrapper').hide();
    });

    $("#btn").click(function(){

    var server = "http://127.0.0.1:8000/extension";
    $.getJSON(server+'?url='+encode_url, function(data) {
    
    // $.getJSON('http://api.geonames.org/citiesJSON?north=44.1&south=-9.9&east=-22.4&west=55.2&lang=de&username=demo', function(data) {
    // var string_val = JSON.stringify(data);
    // console.log(string_val);
    // data = '{"images": [\
    // "http://img.timeinc.net/time/daily/2007/0706/a_arat_0618.jpg",\
    // "http://cssdeck.com/uploads/media/items/2/2v3VhAp.png",\
    // "http://cssdeck.com/uploads/media/items/1/1swi3Qy.png",\
    // "http://cdn.wegotthiscovered.com/wp-content/uploads/WALL-E.jpg",\
    // "http://cssdeck.com/uploads/media/items/6/6f3nXse.png",\
    // "http://www.metrohnl.com/wp-content/uploads/2015/03/metro-040115-scenestealers-pixar1.jpg",\
    // "http://cssdeck.com/uploads/media/items/8/8kEc1hS.png",\
    // "http://www.ctvnews.ca/polopoly_fs/1.2089627.1415286735!/httpImage/image.jpg_gen/derivatives/landscape_620/image.jpg",\
    // "http://img.timeinc.net/time/daily/2007/0706/a_arat_0618.jpg",\
    // "http://img.timeinc.net/time/daily/2007/0706/a_arat_0618.jpg",\
    // "http://cssdeck.com/uploads/media/items/2/2v3VhAp.png",\
    // "http://cssdeck.com/uploads/media/items/1/1swi3Qy.png",\
    // "http://cdn.wegotthiscovered.com/wp-content/uploads/WALL-E.jpg",\
    // "http://cssdeck.com/uploads/media/items/6/6f3nXse.png",\
    // "http://www.metrohnl.com/wp-content/uploads/2015/03/metro-040115-scenestealers-pixar1.jpg",\
    // "http://cssdeck.com/uploads/media/items/8/8kEc1hS.png",\
    // "http://www.ctvnews.ca/polopoly_fs/1.2089627.1415286735!/httpImage/image.jpg_gen/derivatives/landscape_620/image.jpg",\
    // "http://img.timeinc.net/time/daily/2007/0706/a_arat_0618.jpg"]}';
              
    //document.getElementById('encodedLink').innerHTML = data;
    // json_data =  jQuery.parseJSON(data)
    // data.addHeader("Access-Control-Allow-Origin", "*");
    jQuery.each(data.images, function(index, value)
    {
        $("#wrapper #columns").append('<div class="pin"><img src="' + value + '" /></h3><p> image,image </p></div>');
                        // $("#image-container").append('<img src="' + value + '" />');
                        // $("#image-container").append('</h3><p> image,image </p></div></div></div>');
    
    
    });
    
    });
              
    $("#wrapper").show();
    //data is the JSON string
    });

});
