#!/usr/usc/bin/perl -wT

use CGI qw(:standard);


print "Content-Type: text/xml\r\n";   # header tells client you send XML
print "\r\n";
print qq(<?xml version="1.0" encoding="UTF-8"?>\n);

if ($ENV{'REQUEST_METHOD'} eq "GET"){
	$buffer = $ENV{'QUERY_STRING'};
}
else{
	read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
}

if (param()){
	$cityName = param('cityName');
	$hotelChain = param('hotelChain');
}
my @cities = split(/ /, param('cityName'));
#print qq(<h2 align="center">$hotelChain hotel in);

# retrieve web page from trip advisor
my $url = 'http://www.tripadvisor.com/Search?q=' . $hotelChain;
foreach $city (@cities){
	$url = $url . '+' . $city;
#	print qq( $city);
}
#print qq(:</h2>\n);
# Check whether LWP module is installed  
if(eval{require LWP::Simple;}){  
}else{  
print "You need to install the Perl LWP module!<br>";  
exit;  
}
$content = LWP::Simple::get($url);
die "Couldn't get $url" unless defined $content;

# obtain information between 2 <div class="section">
if ($content =~ /<div class="section">(.*?)<div class="section">/s){
	$searchResult = $1;
	
	# separate all the hotels
	@hotels = split /<div class="searchResult srLODGING">/, $searchResult;
	shift @hotels;
	
	# print table header
	#print qq(<table border align="center"> \n);
	#print qq(<tr> \n);
	#print qq(<td width="150" align="center">Image</td><td width="160" align="center">Name</td><td width="130" align="center">Location</td><td width="148" align="center">Rating out of 5</td><td width="150" align="center">Reviews</td> \n);
	#print qq(</tr> \n);
	
	#print qq(<hotels total="scalar @hotels">);
	print qq(<hotels total=\");
	print scalar @hotels;
	print qq (">\n);
	# for each hotel, get its information
	foreach $hotel(@hotels){
		# get hotel Name
		if ($hotel =~ /\);">(.*?)<\/div>/s){
			#$hotelName1 = $1;
			#if ($hotelName1 =~ /onclick="setOneTimeCookie('NORDINAL','B1');">(.*?)<\/a>/s){
				$hotelName = $1;
				$hotelName =~s/<b>//g;
				$hotelName =~s/<\/b>//g;
				$hotelName =~s/<\/a>//g;
				$hotelName =~s/&/&amp;/g;
				#$hotelName =~ tr/A-Za-z0-9 //cd
			#}
		}
		
		# get image
		if ($hotel =~ /<img src=(.*?) class=/){
			$hotelImage = $1;
		}
		
		# get location
		if ($hotel =~ /&ndash;(.*?)<\/div>/s){
			$hotelLocation = $1;
		}
		
		# get rating
		if ($hotel =~ /alt="(.*?)of 5 stars"\/><\/span>/){
			$hotelRating = $1;
		}
		
		# get reviews
		if ($hotel =~ /span class="rate rate_no no..">.*<\/span>(.*?)reviews/s){
			$hotelReviews = $1;
			$hotelReviews =~s/,//g;
		}
		
		# get review link
		if ($hotel =~ /<div class="rating">\n<a href="(.*?)" onclick=/s){
			$hotelReviewLink = $1;
		}
		
		#print qq(<tr> \n);
		#print qq(<td align="center"><img src=$hotelImage style="height: 200px; width: 150px;"></td> \n);
		#print qq(<td align="center">$hotelName</td> \n);
		#print qq(<td align="center">$hotelLocation</td>);
		#print qq(<td align="center">$hotelRating</td>);
		#print qq(<td align="center"><a href=http://www.tripadvisor.com$hotelReviewLink>$hotelReviews</a></td> \n);
		#print qq(</tr> \n);
		print qq(\n);
		print qq(\t<hotel name="$hotelName" location="$hotelLocation" no_of_stars="$hotelRating" no_of_reviews="$hotelReviews"
image_url=$hotelImage review_url="$hotelReviewLink"/>);		
	}
	#print qq(</table> \n);
	print qq(\n);
	print qq(</hotels>);
}
else {
	print qq(<h1 align="center">No hotels found!</h1>);
}

1;