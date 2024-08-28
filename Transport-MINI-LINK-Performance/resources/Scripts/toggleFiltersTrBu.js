MutationObserver = window.MutationObserver || window.WebKitMutationObserver;

var targetDomId = "aggregation"
var onLoadVal=$('#'+targetDomId+' .ComboBoxTextDivContainer').text();
 
if(onLoadVal=="ROP Data (No Aggregation)"){
	console.log("word")
	console.log(onLoadVal)
	$(".date").hide()
	$(".dateAndTime").show()
	$(".dayFilter").hide()
	$(".rawFilter").show()
	$(".dayFilterNodes").hide()
	$(".rawFilterNodes").show()
	$(".dayFilterNetworkType").hide()
	$(".rawFilterNetworkType").show()
	$(".dayFilterKPI").hide()
	$(".rawFilterKPI").show()}
	else if(onLoadVal=="DAY"){
		$(".date").show()
		$(".dateAndTime").hide()
		$(".dayFilter").show()
	    $(".rawFilter").hide()
		$(".dayFilterNodes").show()
	    $(".rawFilterNodes").hide()
		$(".dayFilterNetworkType").show()
	    $(".rawFilterNetworkType").hide()
		$(".rawFilterKPI").hide()
		$(".dayFilterKPI").show()
		}	

var myFunction = function(oldValue,newValue){
  if(newValue=="ROP Data (No Aggregation)"){
	console.log("word")
	console.log(newValue)
	value=$('#dataflag input').val()
	$(".date").hide()
	$(".dateAndTime").show()
	$(".dayFilter").hide()
	$(".rawFilter").show()
	$(".dayFilterNodes").hide()
	$(".rawFilterNodes").show()
	$(".dayFilterNetworkType").hide()
	$(".rawFilterNetworkType").show()
	$(".dayFilterKPI").hide()
	$(".rawFilterKPI").show()}
	else if(newValue=="DAY"){
		$(".date").show()
		$(".dateAndTime").hide()
		$(".dayFilter").show()
	    $(".rawFilter").hide()
		$(".dayFilterNodes").show()
	    $(".rawFilterNodes").hide()
		$(".dayFilterNetworkType").show()
	    $(".rawFilterNetworkType").hide()
		$(".rawFilterKPI").hide()
		$(".dayFilterKPI").show()
	    }	
}

var target = document.getElementById(targetDomId)
var oldVal = target.innerText.trim()

var callback = function(mutations) {
 newVal=$('#'+targetDomId+' .ComboBoxTextDivContainer').text()
 if(newVal!=oldVal) myFunction(oldVal,newVal)
 oldVal = newVal;
}

var observer = new MutationObserver(callback);

var opts = {
    childList: true, 
    attributes: true, 
    characterData: true, 
    subtree: true
}

observer.observe(target,opts);