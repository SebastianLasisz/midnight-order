//Removing not avaiable pictures from Chrome and IE
(function(){
	var allimgs = document.images;
	for(var i=0; i<allimgs.length; i++){
		allimgs[i].onerror = function () {
			this.style.visibility = "hidden";
 }}})();