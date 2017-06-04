import requests
import json
import bs4, re


def get_urls(q):
    key = "e85385f28bc14dac94f411e9f418f3ae"
    count="50"
    url="https://api.cognitive.microsoft.com/bing/v5.0/search"
    headers={
        'Ocp-Apim-Subscription-Key': key
    }
    params={
        'q' : q,
        'count' : count
    }
    r = requests.get(url,params=params, headers=headers)
    j = json.loads(r.text)
    x=j['webPages']['value']
    urls = [v['displayUrl'] for v in x] # maybe v['url']
    return urls


def get_text(url):
    html =requests.get(url).text
    soup = bs4.BeautifulSoup(html,'lxml')
    raw = soup.get_text();
    text = re.sub("[\t\n ]+"," ",raw)
    return text

def get_names(text):
    """
    return a list of all names in a page (each as a string)
    Name is described by the regular expression below.
    """
    exp = "[A-Z][a-z]+ [A-Z][a-z]+"
    results = re.findall(exp,text)
    return [x for x in results]

def get_dates(text):
    """
    return a list of all the dates in a page (each as a string)
    Dates are described by the regular expression below
    """
    exp = "[A-Za-z\.]+ [0-9]{1,2},? [0-9]{4}"
    results = re.findall(exp,text)
    return [x for x in results]
 

def add_to_tallies(keys,tallies={}):
    """
    Input: a list of keys and a disctionary of current tallies
    
    Returns: Updated tallies - how many time each key occured
    """
    for k in keys:
        tallies.setdefault(k,0)
        tallies[k]=tallies[k]+1
    return tallies

# z=get_text("https://en.wikipedia.org/wiki/Iron_Man_2")
# t=get_names(z)
# d = add_to_tallies(t,{})
# v = [x for x in d.values()]
# v.sort()

# print(v)

#urls = get_urls("who played ironman")
#urls = get_urls("who played spiderman")
#urls = get_urls("who played Thor")
#urls = get_urls("who shot John Lennon")
# urls = get_urls("who shot Ronald Reagan")
# t = {}
# for u in urls:
#     if u[0] !='h':
#         u="http://"+u
#     print(u)
#     try:
#         text = get_text(u)
#         names = get_names(text)
#         t = add_to_tallies(names,t)
#     except:
#         pass
# v = [x for x in t.values()]
# v.sort()
# v.reverse()
# for k in t.keys():
#     if t[k] >= v[10]:
#         print(k,t[k])


def getAnswers(q):
    """
    returns list of (x,y) where x is answer y is count
    """
    if q[0:3] == "who":
        refunc = get_names
    else:
        refunc = get_dates

    urls = get_urls(q)    
    t={}
    for u in urls:
        if u[0] != 'h':
            u="http://"+u
        print(u)
        try:
            text = get_text(u)
            res = refunc(text)
            t=add_to_tallies(res,t)
        except:
            pass

    retvals=[]
    
    for k in t:
        retvals.append((k,t[k]))
    retvals = sorted(retvals,key=lambda x: x[1])
    retvals.reverse()
    return retvals

