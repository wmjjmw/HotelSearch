Link: http://cs-server.usc.edu:29568/hw8/hotel_search2.html

This project provided an interface to perform search from tripadvisor.com and post details to Facebook
It used a combination of HTML, CSS, DOM, XMLHttpRequest, Java Servlets, AJAX, JSON& XMLtechnologies.

hotel_search2.cgi is used in Apache server to parse the information getting from tripadvisor.com into XML
hello.java is used in Java servlet to extract the appropriate information from this XML.
Lastly, the Java Servlet produces a JSON string that is returned asynchronously to the original XMLHttpRequest.