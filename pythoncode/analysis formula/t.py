import urllib.request
import json

ip = '80.82.78.38'
apiurl = 'http://ip.taobao.com/service/getIpInfo.php?ip={}'.format(ip)
data = urllib.request.urlopen(apiurl).read()
data = json.loads(str(data, encoding="utf-8"))['data']
print(data)
print('{} {} {}'.format(data['city'], data['region'], data['isp']))
