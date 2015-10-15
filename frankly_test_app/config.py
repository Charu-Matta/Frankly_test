import urllib2
from lxml import html

class get_context(object):
    
    
    def get_parsed_source(self,base_url, target_url, raw1=False):
        req = urllib2.Request(target_url,
                            headers={'User-Agent': 'Mozilla/5.0' })
        html_opener = urllib2.urlopen(req)
        html_code = html_opener.read()
        if raw1:
            return html_code
        parsed_source = html.fromstring(html_code, base_url)
        parsed_source.make_links_absolute()
        
        return parsed_source
    
    def urls(self):
        base_url = "https://news.ycombinator.com"
        target_url = "https://news.ycombinator.com/news"
        
        return base_url,target_url