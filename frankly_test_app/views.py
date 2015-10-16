from django.shortcuts import render_to_response
from django.template import RequestContext
from config import *
from goose import Goose
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def fetch_data_db(request):
    obj = get_context()
    connection,cursor = obj.get_connection()
    select_query = "SELECT * FROM hackers_news  ORDER BY posted_on ASC limit 20"
    cursor.execute(select_query,)
    all_news = cursor.fetchall()
    total_data =[]
    if all_news:
        dict_result = obj.get_query_dictonary(all_news,cursor)
        print dict_result
        for news in dict_result:
            news_url = news['news_url']
            content = news['news_content']
            upvotes = news['upvotes']
            posted_on = news['posted_on']
            comments = news['comments']
            total_data.append({'news_url':news_url, 'content':content , 'upvotes':upvotes,\
                                'posted_on':posted_on,'comments':comments,})
        context_dict = {'total_data':total_data}
    else:
        context_dict = hackers_news() 
    cursor.close()
    connection.close()
    import ipdb;ipdb.set_trace()
    return render_to_response('hackers_news.html', context_dict,context_instance=RequestContext(request))
    
    
def hackers_news():
    total_data = []
    obj = get_context()
    base_url,target_url = obj.urls()
    parsed_source = obj.get_parsed_source(base_url,target_url )
    news_urls = parsed_source.xpath("//table[@id='hnmain']//table//tr[@class='athing']")
    for each_data in news_urls:
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
        connection,cursor = obj.get_connection()
        duplicate_query = "SELECT news_url FROM hackers_news WHERE news_url=%s"
        duplicate_values = (news_url,)
        cursor.execute(duplicate_query,duplicate_values)
        duplicate_data = cursor.fetchall()
        if duplicate_data:
            insert_data = "update hackers_news set upvotes ="+upvotes+",comments="+comments+" where news_url=%s"
            values = (news_url,)
            cursor.execute(insert_data,values)
            connection.commit()
        else:
            try:
                insert_data = "insert into hackers_news(news_url,news_content,upvotes,posted_on,comments) values(%s,%s,%s,%s,%s)"
                values = (news_url,content,upvotes,posted_on,comments)
                cursor.execute(insert_data,values)
                connection.commit()
            except:
                continue
        cursor.close()
        connection.close()
        total_data.append({'news_url':news_url, 'content':content , 'upvotes':upvotes,\
                                 'posted_on':posted_on,'comments':comments,})
    context_dict = {'total_data':total_data}
    return context_dict
