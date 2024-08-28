MutationObserver = window.MutationObserver || window.WebKitMutationObserver;
console.log("toggleFilters")
var targetDomId = "aggregation"
var targetDomIdKpiGroup = "kpiGroup"
var onLoadVal=$('#'+targetDomId+' .ComboBoxTextDivContainer').text();
var onLoadValKpiGroup=$('#'+targetDomIdKpiGroup+' .ComboBoxTextDivContainer').text();
 
if(onLoadVal=="ROP Data (No Aggregation)"){
	console.log("RAW from toggle filter")
	value=$('#dataflag input').val()
	$(".date").hide()
	$(".dateAndTime").show()
	$(".dayFilter").hide()
	$(".rawFilter").show()
	$(".dayFilterNodes").hide()
	$(".rawFilterNodes").show()
	$(".dayFilterNetworkType").hide()
	$(".rawFilterNetworkType").show()
	$(".dayFilterKpiCalculated").hide()
	$(".dayFilterKpiFetched").hide()
	$(".rawFilterKpiCalculated").show()
	if (value=="calculated"){
		$(".rawFilterKpiCalculated").show()
		$(".rawFilterKpiFetched").hide()
		$(".dayFilterKpiCalculated").hide()
		$(".dayFilterKpiFetched").hide()
	}
	else if (value=="fetched"){
		$(".rawFilterKpiCalculated").hide()
		$(".rawFilterKpiFetched").show()
		$(".dayFilterKpiCalculated").hide()
		$(".dayFilterKpiFetched").hide()
	}}
	else if(onLoadVal=="DAY"){
		console.log("DAY")
		$(".date").show()
		$(".dateAndTime").hide()
		$(".dayFilter").show()
	    $(".rawFilter").hide()
		$(".dayFilterNodes").show()
	    $(".rawFilterNodes").hide()
		$(".dayFilterNetworkType").show()
	    $(".rawFilterNetworkType").hide()
		$(".rawFilterKpiCalculated").hide()
		value=$('#dataflag input').val()
		if (value=="calculated"){
			$(".rawFilterKpiCalculated").hide()
		    $(".rawFilterKpiFetched").hide()
			$(".dayFilterKpiCalculated").show()
			$(".dayFilterKpiFetched").hide()
		}
		else if (value=="fetched"){
			$(".rawFilterKpiCalculated").hide()
		    $(".rawFilterKpiFetched").hide()
			$(".dayFilterKpiCalculated").hide()
			$(".dayFilterKpiFetched").show()
		}
		}	

var myFunction = function(oldValue,newValue,flagValue,onLoadValKpiGroup){
  if(newValue=="ROP Data (No Aggregation)"){
	console.log("RAW from toggle filter")
	value=$('#dataflag input').val()
	$(".date").hide()
	$(".dateAndTime").show()
	$(".dayFilter").hide()
	$(".rawFilter").show()
	$(".dayFilterNodes").hide()
	$(".rawFilterNodes").show()
	$(".dayFilterNetworkType").hide()
	$(".rawFilterNetworkType").show()
	$(".dayFilterKpiCalculated").hide()
	$(".rawFilterKpiCalculated").show()
	if (value=="calculated"){
		$(".rawFilterKpiCalculated").show()
		$(".rawFilterKpiFetched").hide()
		$(".dayFilterKpiCalculated").hide()
		$(".dayFilterKpiFetched").hide()
	}
	else if (value=="fetched"){
		$(".rawFilterKpiCalculated").hide()
		$(".rawFilterKpiFetched").show()
		$(".dayFilterKpiCalculated").hide()
		$(".dayFilterKpiFetched").hide()
	}
	}
	else if(newValue=="DAY"){
		console.log("DAY")
		$(".date").show()
		$(".dateAndTime").hide()
		$(".dayFilter").show()
	    $(".rawFilter").hide()
		$(".dayFilterNodes").show()
	    $(".rawFilterNodes").hide()
		$(".dayFilterNetworkType").show()
	    $(".rawFilterNetworkType").hide()
		$(".rawFilterKpiCalculated").hide()
		if (flagValue=="calculated"){
			$(".rawFilterKpiCalculated").hide()
		    $(".rawFilterKpiFetched").hide()
			$(".dayFilterKpiCalculated").show()
			$(".dayFilterKpiFetched").hide()
		}
		else if (flagValue=="fetched"){
			$(".rawFilterKpiCalculated").hide()
		    $(".rawFilterKpiFetched").hide()
			$(".dayFilterKpiCalculated").hide()
			$(".dayFilterKpiFetched").show()
		}
	    }	
}

var target = document.getElementById(targetDomId)
var oldVal = target.innerText.trim()

var callback = function(mutations) {
 flagValue=$('#dataflag input').val()
 newVal=$('#'+targetDomId+' .ComboBoxTextDivContainer').text()
 onLoadValKpiGroup=$('#'+targetDomIdKpiGroup+' .ComboBoxTextDivContainer').text();
 if(newVal!=oldVal) myFunction(oldVal,newVal,flagValue,onLoadValKpiGroup)
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