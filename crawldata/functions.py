
import hashlib,re,requests,platform

def check_os():
    return platform.system()
    
__version__ = '0.1.2'
class TrackerBase(object):
    def on_start(self, response):
        pass
    def on_chunk(self, chunk):
        pass
    def on_finish(self):
        pass
class ProgressTracker(TrackerBase):
    def __init__(self, progressbar):
        self.progressbar = progressbar
        self.recvd = 0
    def on_start(self, response):
        max_value = None
        if 'content-length' in response.headers:
            max_value = int(response.headers['content-length'])
        self.progressbar.start(max_value=max_value)
        self.recvd = 0
    def on_chunk(self, chunk):
        self.recvd += len(chunk)
        try:
            self.progressbar.update(self.recvd)
        except ValueError:
            # Probably the HTTP headers lied.
            pass
    def on_finish(self):
        self.progressbar.finish()
class HashTracker(TrackerBase):
    def __init__(self, hashobj):
        self.hashobj = hashobj
    def on_chunk(self, chunk):
        self.hashobj.update(chunk)
def download(url, target, proxy=None , headers=None, trackers=()):
    if headers is None:
        headers = {}
    headers.setdefault('user-agent', 'requests_download/'+__version__)
    if proxy is None:
        r = requests.get(url, headers=headers, stream=True)
    else:
        host=str(proxy).split('@')[1]
        account=(str(proxy).split('@')[0]).split(':')
        proxies = {'http': 'http://'+host,'https': 'http://'+host,}
        r = requests.get(url, proxies=proxies, auth=(account[0], account[1]) , headers=headers, stream=True, verify=False, timeout=20)
    r.raise_for_status()
    for t in trackers:
        t.on_start(r)
    with open(target, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                for t in trackers:
                    t.on_chunk(chunk)
    for t in trackers:
        t.on_finish()
def translate(text,fromlag,tolang):
    data = {'text': text,'gfrom': fromlag,'gto': tolang}
    response = requests.post('https://www.webtran.eu/gtranslate/', data=data)
    return(response.text)
def Get_Number(xau):
    KQ=re.sub(r"([^0-9.])","", str(xau).strip())
    return KQ
def Get_String(xau):
    KQ=re.sub(r"([^A-Za-z_])","", str(xau).strip())
    return KQ
def cleanhtml(raw_html):
    if raw_html:
        raw_html=str(raw_html).replace('</',' ^</')
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        cleantext=(' '.join(cleantext.split())).strip()
        cleantext=str(cleantext).replace(' ^','^').replace('^ ','^')
        while '^^' in cleantext:
            cleantext=str(cleantext).replace('^^','^')
        cleantext=str(cleantext).replace('^','\n')
        return cleantext.strip()
    else:
        return ''
def kill_space(xau):
    xau=str(xau).replace('\t','').replace('\r','').replace('\n',', ')
    xau=(' '.join(xau.split())).strip()
    return xau
def key_MD5(xau):
    xau=(xau.upper()).strip()
    KQ=hashlib.md5(xau.encode('utf-8')).hexdigest()
    return KQ
def get_item_from_json(result,item,space):
    if isinstance(item,dict):
        for k,v in item.items():
            if isinstance(v,dict) or isinstance(v,list):
                if space=='':
                    get_item_from_json(result,v,k)
                else:
                    get_item_from_json(result,v,space+'.'+k)
            else:
                if space=='':
                    result[k]=v
                else:
                    result[space+'.'+k]=v
    else:
        for i in range(len(item)):
            k=str(i)
            v=item[i]
            if isinstance(v,dict) or isinstance(v,list):
                if space=='':
                    get_item_from_json(result,v,k)
                else:
                    get_item_from_json(result,v,space+'.'+k)
            else:
                if space=='':
                    result[k]=v
                else:
                    result[space+'.'+k]=v
    return result