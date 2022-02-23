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
t2=(t+datetime.timedelta(hours=10)).strftime("%Y-%m-%d %H:%M:%S")
ts2=time.mktime(time.strptime(t2, '%Y-%m-%d %H:%M:%S'))
param_data = {
      "name": "严蓉测试直播房间",
      "coverImg": "hICFk2yAT77qFxiAg51Q68WYOxfoufXf46bbe4ZD546egbezwCENHC2dPIUiHPWK",
      "startTime": ts1,
      "endTime": ts2,
      "anchorName": "严蓉test",
      "anchorWechat": "YR745986854",
      "shareImg": "hICFk2yAT77qFxiAg51Q68WYOxfoufXf46bbe4ZD546egbezwCENHC2dPIUiHPWK",
      "type": 1,
      "screenType": 0,
      "closeLike": 0,
      "closeGoods": 0,
      "closeComment": 0,
      "feedsImg": "hICFk2yAT77qFxiAg51Q68WYOxfoufXf46bbe4ZD546egbezwCENHC2dPIUiHPWK"
}
url = "https://api.weixin.qq.com/wxaapi/broadcast/room/create?access_token=54_2Q22uIcJo5oMMxcGo8OW165zfxdOb6zzSt9TO3aqmPRtbOmS-Rs4MMbEe5GQgYimRgzRiROPARfVV_ztPs9DQhicW6CFEpntNbRfHeFGj4JzNNgHzlUBRAgtolvzhsIb1uC9mlguiI7PY9npSWChAJAXBH"

# param_data = json.dumps(param_data)

headers = {'Content-Type': 'application/json;charset=UTF-8'}

r1 = requests.request("post", url, json=param_data, headers=headers)