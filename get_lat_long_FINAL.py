import urllib2, csv

def get_page(url):
    """opens and reads urls"""
    return urllib2.urlopen(url).read()

def get_next_target(page):
    """searches container company website for each port's url"""
    start_link=page.find('<a href="/ports')
    if start_link == -1:
        return None, 0
    start_quote=page.find('"',start_link + 1)
    end_quote=page.find('"',start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def print_all_links(page):
    """Pulls port urls and puts urls into a list"""
    global port_links
    port_links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            port_links_urls = "http://www.worldportsource.com" + url
            port_links.append(port_links_urls)
            page = page[endpos:]
        else:
            break
    return port_links

def lat_and_long(page):
    """searches for and returns name of port, latitude of port, and longitude of port"""
    for i in page[1:]:
        links = get_page(i)
        """find lat"""
        find_lat = links.find("Latitude:") + 86
        if find_lat == -1:
            return None, 0
        start_lat = links.find(">",find_lat + 1)
        end_lat = links.find('</td>',start_lat + 1)
        output_lat = links[start_lat + 1:end_lat].replace('&#176;','')
        """find long"""
        find_long = links.find("Longitude:") + 86
        if find_long == -1:
            return None, 0
        start_long = links.find(">",find_long + 1)
        end_long = links.find('</td>',start_long + 1)
        output_long = links[start_long + 1:end_long].replace('&#176;','')
        """find name"""
        find_name=links.find("<title>WPS")
        if find_name == -1:
            return None, 0
        start_name=links.find('-',find_name + 1)
        end_name=links.find('contact',start_name + 1)
        output_name = links[start_name + 1:end_name]
        filewrite.writerow([output_name, output_lat, output_long])


b = open('china_shipping.csv', 'w')
filewrite = csv.writer(b)
            
links = print_all_links(get_page(raw_input("Enter a url: ")))
lat_and_long(links)

