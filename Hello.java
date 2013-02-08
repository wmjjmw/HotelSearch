package mypackage;

import java.io.IOException;
import java.io.PrintWriter;
import java.io.InputStream;
import java.net.URLConnection;
import java.net.URL;
import java.lang.String;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.util.Enumeration;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.net.*;
import java.io.*;
import javax.xml.parsers.*;
import org.w3c.dom.*;
import org.apache.xerces.dom.DOMImplementationImpl;
import java.io.File;
import org.xml.sax.SAXException;
import java.io.IOException;

public final class Hello extends HttpServlet {


    /**
     * Respond to a GET request for the content produced by
     * this servlet.
     *
     * @param request The servlet request we are processing
     * @param response The servlet response we are producing
     *
     * @exception IOException if an input/output error occurs
     * @exception ServletException if a servlet error occurs
     */
    public void doGet(HttpServletRequest request,
                      HttpServletResponse response)
      throws IOException, ServletException {

	response.setContentType("text/plain");
	response.setHeader("Cache-Control","no-cache");
	PrintWriter writer = response.getWriter();
	
	URL CGIURL = new URL("http://cs-server.usc.edu:29567/cgi-bin/hotel_search2.cgi?"+request.getQueryString());
	InputStream CGIStream = CGIURL.openStream();
	DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
	DocumentBuilder db = null;
	try{
		db = dbf.newDocumentBuilder();	
	}catch(ParserConfigurationException pce){
		pce.printStackTrace();
	}
	Document Dom = null;
	try{
		Dom = db.parse(CGIStream);
	}catch(SAXException pce){
		pce.printStackTrace();
	}catch(IOException pce){
		pce.printStackTrace();
	}
	Element docEle = Dom.getDocumentElement();
	writer.println("{\"hotels\":{");
    //System.out.println(docEle.getAttribute("total"));
    NodeList nl = docEle.getElementsByTagName("hotel");
    writer.println("\t\"hotel\":[");
	
	if (nl != null && nl.getLength() > 0){
		for (int i = 0; i < nl.getLength(); i++){
			Element hotel = (Element)nl.item(i);
			String outString = createStringBufferJSON(hotel);
			writer.print(outString);
			if (i != nl.getLength()-1){
				writer.print(",\n");
			}
		}
	}
	writer.print("\n\t]}\n}");
    }
	
	public String createStringBufferJSON(Element hotelElem){
	  StringBuffer returnJSON = new StringBuffer("\t{");
	  returnJSON.append("\"name\":\""+ hotelElem.getAttribute("name").replaceAll(",", "*")+"\",");
	  returnJSON.append("\"location\":\""+hotelElem.getAttribute("location").replaceAll(",", "*")+"\",");
	  returnJSON.append("\"no_of_stars\":\""+hotelElem.getAttribute("no_of_stars")+"\",");
	  returnJSON.append("\"no_of_reviews\":\""+hotelElem.getAttribute("no_of_reviews")+"\",");
	  returnJSON.append("\"image_url\":\""+hotelElem.getAttribute("image_url").replaceAll(":", "!")+"\",");
	  returnJSON.append("\"review_url\":\""+hotelElem.getAttribute("review_url").replaceAll(":", "!")+"\"");
	  returnJSON.append("}");
	  return returnJSON.toString();
  }
}
