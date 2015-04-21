$(document).ready(function(){
	var url = window.location;
	$('ul.nav a').filter(function() {
    	return this.href == url;
	}).parent().addClass('active');

	currentUrl = url.href;
	currentUrl = currentUrl.split('/');
	len = currentUrl.length;
	currentUrl = currentUrl[len-1];
	$("#left").on('click', function(){
		curr = parseInt(currentUrl);
		if(currentUrl == "01"){
			window.location.href = "/video/14"
		}
		else if(currentUrl == "15"){
			window.location.href = "/video/13"
		}
		else if(currentUrl == "14"){
			window.location.href = "/video/15"
		}	
		else{
			curr -= 1;
			if(curr < 10){
				curr = "0" + curr.toString();
			}
			else{
				curr = curr.toString();
			} 
			window.location.href = "/video/" + curr;
		}
	});
	$("#right").on('click', function(){
		curr = parseInt(currentUrl);
		if(currentUrl == "14"){
			window.location.href = "/video/01"
		}
		else if(currentUrl == "13"){
			window.location.href = "/video/15"
		}
		else if(currentUrl == "15"){
			window.location.href = "/video/14"
		}	
		else{
			curr += 1;
			if(curr < 10){
				curr = "0" + curr.toString();
			}
			else{
				curr = curr.toString();
			}
			window.location.href = "/video/" + curr;
		}
	});
});