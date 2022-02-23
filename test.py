# !/usr/bin/env python
# coding:utf-8
import json
import requests
from datetime import datetime
import time
import datetime

t=datetime.datetime.now()
t1=(t+datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
ts1=time.mktime(time.strptime(t1, '%Y-%m-%d %H:%M:%S'))
t2=(t+datetime.timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")
ts2=time.mktime(time.strptime(t2, '%Y-%m-%d %H:%M:%S'))
param_data = {
      "name": "测试直播房间1",
      "coverImg": "hICFk2yAT77qFxiAg51Q68WYOxfoufXf46bbe4ZD546egbezwCENHC2dPIUiHPWK",
      "startTime": ts1,
      "endTime": ts2,
      "anchorName": "严哲",
      "anchorWechat": "ybc1994829",
      "shareImg": "hICFk2yAT77qFxiAg51Q68WYOxfoufXf46bbe4ZD546egbezwCENHC2dPIUiHPWK",
      "type": 1,
      "screenType": 0,
      "closeLike": 0,
      "closeGoods": 0,
      "closeComment": 0,
      "feedsImg": "hICFk2yAT77qFxiAg51Q68WYOxfoufXf46bbe4ZD546egbezwCENHC2dPIUiHPWK"
}
url = "https://api.weixin.qq.com/wxaapi/broadcast/room/create?access_token=54_UoJu0zQ3Ug1J6gqFi2jD7XR1-YdWn5ftAxEZfq6zIaumsX58IErgrNNRBGTthilth1zRaCP4wvbu4m2tMoFdXUgEQPU_nF0lduSwDbbDWUMVGCtzOxGOQZ-P40hCKhroZsu0w_8ZHlpPuJ9xSCThAEADNE"

# param_data = json.dumps(param_data)

headers = {'Content-Type': 'application/json;charset=UTF-8'}

r1 = requests.request("post", url, json=param_data, headers=headers)