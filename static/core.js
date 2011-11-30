function Init()
{
	if(navigator.geolocation)
	{
		navigator.geolocation.getCurrentPosition(
												function(position) {
												 g_Lat = new Number(position.coords.latitude);
												 g_Lat = g_Lat.toFixed(3);
												 g_Long = new Number(position.coords.longitude);
												 g_Long = g_Long.toFixed(3);
												
												 var latlng = new google.maps.LatLng(g_Lat, g_Long);
												 var myOptions = {
												     zoom: 12,
												     center: latlng,
												     mapTypeId: google.maps.MapTypeId.ROADMAP
											     };
												 var map = new google.maps.Map(
																			document.getElementById("map_canvas"),
																			myOptions);
												 
												 var marker = new google.maps.Marker({
																					  position: latlng,
																					  map: map,
																					  title: "You're posting here!"
																					 });
												 
												 if(window.location.search == undefined ||
												    window.location.search == "")
												 {
													 var location = "/?airnotebook_location=" + escape(g_Lat + "," + g_Long);
													 window.location.assign(location);
												 }
												});
	}
	else
	{
		alert("Geolocation is not supported by " + navigator.userAgent);
	}
}

function WriteNote()
{
	var elmContent = document.getElementById("txtAreaContent");
	if(elmContent != undefined)
	{
		var location = g_Lat + "," + g_Long;
		PostToUrl("/note", {"airnotebook_location":location, "content":elmContent.value});
	}
}

function PostToUrl(path, params, method) {
    method = method || "post"; // Set method to post by default, if not specified.
	
    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);
	
    for(var key in params) {
        var hiddenField = document.createElement("input");
        hiddenField.setAttribute("type", "hidden");
        hiddenField.setAttribute("name", key);
        hiddenField.setAttribute("value", params[key]);
		
        form.appendChild(hiddenField);
    }
	
    document.body.appendChild(form);
    form.submit();
}

var g_Lat;
var g_Long;
window.onload=Init;