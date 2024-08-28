#!/bin/bash
 
if [ "$2" == "" ]; then
    	echo usage: "$0" \<Branch\> \<RState\>
    	exit 1
else
	export versionProperties=install/version.properties
	theDate=\#$(date +"%c")
	export theDate
	module=$1
	export branch=$2
	export workspace=$3
fi
#added a test comment
#added a comment
#december 19 2022
function getProductNumber {
        product=$(grep "$module" | awk -F " " '{print $3}' "$PWD"/build.cfg )
}
function setRstate {
        revision=$(grep "$module" | awk -F " " '{print $4}' "$PWD"/build.cfg)
	
	if git tag | grep "$product"-"$revision"; then
        	rstate=$(git tag | grep "${product}"-"${revision}" | tail -1 | sed s/.*-// | perl -nle 'sub nxt{$_=shift;$l=length$_;sprintf"%0${l}d",++$_}print $1.nxt($2) if/^(.*?)(\d+$)/';)
        else
		ammendment_level=14
	        rstate=$revision$ammendment_level
	fi
	mv "$PWD"/Transport-MINI-LINK-Performance/build/feature-release.xml "$PWD"/Transport-MINI-LINK-Performance/build/feature-release."${rstate}".xml
		echo "Building rstate:$rstate"
		echo "$rstate" > params.txt
		echo "$product" >> params.txt
}
getProductNumber
setRstate
