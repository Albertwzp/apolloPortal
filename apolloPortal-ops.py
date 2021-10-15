#coding=utf-8
#import pyapollos
#import subprocess
import requests
import json
import time

from selenium import webdriver

def get_cookie(url, username, password):
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.delete_all_cookies()
    browser.get(url)
    browser.find_element_by_xpath('//input[@name="username"]').send_keys(username)
    browser.find_element_by_xpath('//input[@name="password"]').send_keys(password, Keys.ENTER)
    cookie = browser.get_cookies()
    return cookie

def request_get(url, headers):
        print("[GET]---url: %s,\t headers: %s" %(url, headers))
        res = requests.get(url, headers=headers)
        #if res.ok:
        if res.status_code == 200:
            #data = res.json()
            data = json.dumps(res.json(), indent=2, ensure_ascii=False)
            #re.match(r'(appId)'
            data_s = json.loads(data)
            res_j = res.json()
            #print("res: %s, data: %s, data_s: %s res_j: %s" % (type(res), type(data), type(data_s), type(res_j)))
            print(data_s)
            return data_s
        else:
            print("data: nil")

def request_post(url, headers, body):
        print("[POST]---url: %s,\t headers: %s,\t body: %s" %(url, headers, body))
        en_body = body.encode('utf-8')
        res = requests.post(url, headers=headers, data=en_body)
        if res.status_code == 200:
            print("POST Success")
        else:
            print("POST FAIL")
        #data = json.dumps(data)
        #print(res.json())
        
    
class ApolloOps(object):
    def __init__(self, config_server='localhost:30005', portal_server='localhost:30001', user='apollo', password='admin', cookie=''):
        self.config_server = config_server
        self.portal_server = portal_server
        self.user = user
        self.password = password
        self.cookie = cookie
	#get_cookie(portal_server)

    def login(self):
        url = '{}/signin'.format(self.portal_server)
        #headers = {'content-type': 'application/json'}
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'zh,zh-TW;q=0.9,en-US;q=0.8,en;q=0.7',
                   'Cache-Control': 'max-age=0',
                   'Connection': 'keep-alive',
                   'content-type': 'application/x-www-form-urlencoded',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        payload = {'username': 'apollo', 'password': 'admin', 'login-submit': '登录'}
        print(url)
        loginx = requests.post(url, data=json.dumps(payload), headers=headers)
        #loginx = requests.Session()
	#loginx.headers.update(headers)
	#loginx.post(url, data=payload)
        if loginx.status_code == 302:
            print('login success')
        else:
            print('login error')

    def get_xxx(self, xxx, *, appId='parent', envName='FAT', clusterName='default', namespaceName='option'):
        #headers = {'content-type': 'application/json', "Authorization":"Bearer {}".format(token)}
        headers = {"Cookie": self.cookie, 'Content-Type': "application/json;charset=UTF-8"}
        if xxx == 'apps':
            url = '{}/apps'.format(self.portal_server)
            ret = request_get(url, headers)
            #print(type(ret))
            #apps = []
            #for i in ret:
            #    apps.append(i["appId"])
            #return apps
            #print(apps)
            return ret
        elif xxx == 'nameSpaces':
            #url = '{}/openapi/v1/envs/{}/apps/{}/clusters/{}/namespaces'.format(self.portal_server, envName, appId, clusterName)
            url = '{}/apps/{}/envs/{}/clusters/{}/namespaces'.format(self.portal_server, appId, envName, clusterName)
            ret = request_get(url, headers)
            namespaces = []
            for i in (ret or []):
                namespaces.append(i["baseInfo"]["namespaceName"])
            return namespaces
        elif xxx == 'properties':
            url = '{}/apps/{}/envs/{}/clusters/{}/namespaces/{}'.format(self.portal_server, appId, envName, clusterName, namespaceName)
            ret = request_get(url, headers)
            

        elif xxx == 'envclusters':
            url = '{}/openapi/v1/apps/{}/envclusters'.format(self.portal_server)
            params={'token': '{}'.format(self.token)}
        elif xxx == 'clusterName':
            url = '{}/openapi/v1/envs/{}/apps/{}/clusters/{}'.format(self.portal_server, env, appId, clusterName)
            print(namespaces)
        elif xxx == 'nameSpaceName':
            #url = '{}/openapi/v1/envs/{}/apps/{}/clusters/{}/namespaces/{}'.format(self.portal_server, envName, appId, clusterName, namespaceName)
            url = '{}/apps/{}/envs/{}/clusters/{}/namespaces/{}'.format(self.portal_server, appId, envName, clusterName, namespaceName)
        else:
            print("get error")

    def post_xxx(self, xxx, *, appId='parent', envName='FAT', clusterName='default', namespaceName='application', app={}):
        headers = {"Cookie": self.cookie, 'Content-Type': "application/json;charset=UTF-8"}
        if xxx == 'app':
            url = '{}/apps'.format(self.portal_server)
            body = "{{'appId': '{}', 'name': '{}', 'orgId': '{}', 'orgName': '{}', 'ownerName': '{}', 'admins': []}}".format(app["appId"], app["name"], app["orgId"], app["orgName"], app["ownerName"])
            #en_body = body.encode('utf-8')
            print(body)
            ret = request_post(url, headers, body)
        elif xxx == 'clusterName':
            #url = '{}/openapi/v1/envs/{}/apps/{}/clusters'.format(self.portal_server, env, appId)
            url = '{}/apps/{}/envs/{}/clusters'.format(self.portal_server, appId, envName)
            #body = "{'name': {}, 'appId': {}, 'dataChangeCreatedBy': {}}".format(clusterName, appId, self.user)
            body = "{{'appId': '{}', 'name': '{}'}}".format(appId, clusterName)
            print(type(body))
            ret = request_post(url, headers, body)
        elif xxx == 'nameSpace':
            #url = '{}/openapi/v1/apps/{}/appnamespaces'.format(self.portal_server, appId)
            url = '{}/apps/{}/namespaces'.format(self.portal_server, appId)
            #body = "{'name': {}, 'appId': {}, 'format': {}, 'isPublic': {}, 'comment':{}, 'dataChangeCreatedBy': {}}".format(clusterName, appId, format, isPubic, comment, self.user)
            body = "[{{'env': '{}', 'namespace': {{'appId': '{}', 'clusterName': '{}', 'namespaceName': '{}'}}}}]".format(envName, appId, clusterName, namespaceName)
            print(type(body))
            ret = request_post(url, headers, body)
        elif xxx == 'release':
            url = '{}/apps/{}/envs/{}/clusters/{}/namespaces/{}/release'.format(self.portal_server, appId, envName, clusterName, namespaceName)
        else:
            print("post error")

    def put_xxx(self, xxx, *, appId, envName, clusterName, namespaceName):
        if xxx == 'item':
            url = '{}/apps/{}/envs/{}/clusters/{}/namespaces/{}/items'.format(self.portal_server, appId, envName, clusterName, namespaceName)


    def get_values(self, *, appId, cluster='default', ns='application', client='locahost'):
        url = '{}/configfiles/json/{}/{}/{}?ip={}'.format(self.config_server, appId, cluster, ns, client)
        print(url)
        values = requests.get(url)
        if values.ok:
            data = values.json()
            print(data)
        else:
            print("values: no data")
        #print(res.json())

    def sync_app(self, *, remote=None):
        apps = remote.get_xxx('apps')
        for app in apps:
            print(app)
            self.post_xxx('app', app=app)

    def sync_cls(self, *, remote=None, srcEnv='', dstEnv='', srcCls='', dstCls=[] ):
        apps = remote.get_xxx('apps')
        for app in apps:
            for cls in dstCls:
                print('Create cls: %s' % cls)
                self.post_xxx('clusterName', appId=app["appId"], envName=dstEnv, clusterName=cls)
        
    def sync_ns(self, *, remote=None, srcEnv='', dstEnv='', srcCls='', dstCls=[] ):
        apps = remote.get_xxx('apps')
        for app in apps:
            nss = remote.get_xxx('nameSpaces', appId=app["appId"], envName=srcEnv, clusterName=srcCls)
            for cls in dstCls:
                #print('Create cls: %s' % cls)
                #self.post_xxx('clusterName', appId=app, envName=dstEnv, clusterName=cls)
                for ns in nss:
                    print('Create ns: %s' % ns)
                    self.post_xxx('nameSpace', appId=app["appId"], envName=dstEnv, clusterName=cls, namespaceName=ns)
                    #time.sleep(10)

