from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from config import *
from goose import Goose
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login



# Create your views here.


@login_required
def hackers_news(request):
    total_data = []
    if request.method == 'GET':
        obj = get_context()
        base_url,target_url = obj.urls()
#         total_news = request.POST.get('text_co').encode('utf-8')
        parsed_source = obj.get_parsed_source(base_url,target_url )
        
        news_urls = parsed_source.xpath("//table[@id='hnmain']//table//tr[@class='athing']")
        for each_data in news_urls[:2]:
            import ipdb;ipdb.set_trace()
            news_url = each_data.xpath(".//td[@class='title']//span[@class='deadmark']//following-sibling::a[1]//@href")
            news_url = "".join(news_url)
            upvotes = each_data.xpath(".//following-sibling::tr[1]//td[@class='subtext']//span//text()")
            upvotes = "".join(upvotes)
            posted_on = each_data.xpath(".//following-sibling::tr[1]//td[@class='subtext']//span//following-sibling::a[2]//text()")
            posted_on = "".join(posted_on)
            comments= each_data.xpath(".//following-sibling::tr[1]//td[@class='subtext']//span//following-sibling::a[3]//text()")
            comments = "".join(comments)
            g = Goose()
            article = g.extract(url=news_url)
            content = article.cleaned_text
            content = " ".join(content.split()).replace('\n','').replace('\t','').replace('\r','')
            try:
                content =content.encode("utf-8").decode("ascii", "ignore").encode("ascii")
            except :
                try:
                    content =content.decode("ascii", "ignore").encode("ascii")
                except:
                    try:
                        content =content.encode("utf-8")
                    except:
                        content = "No news found"
                
            total_data.append({'news_url':news_url, 'content':content , 'upvotes':upvotes,\
                                     'posted_on':posted_on,'comments':comments,})
            
            
        context_dict = {'total_data':total_data}
    else:
        context_dict = {}
        
    
    return render_to_response('hackers_news.html', context_dict,context_instance=RequestContext(request))