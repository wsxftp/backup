import requests

CropID='ww86706ff35923cd1c'
Secret='j4CotkpKfYTpenxh_dLj2j6_W8Sv8VmjJ01VDT7RpfQ'
gurl = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'.format(CropID, Secret)

mes = requests.request()

print