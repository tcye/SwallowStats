# -*- coding:gbk -*-

import datetime


Weekday2DutyTime = {
	0: (datetime.time(10, 0), datetime.time(19, 30)),  # 周一
	1: (datetime.time(10, 0), datetime.time(19, 30)),  # 周二
	2: (datetime.time(11, 30), datetime.time(20, 0)),  # 周三
	3: (datetime.time(10, 0), datetime.time(19, 30)),  # 周四
	4: (datetime.time(10, 0), datetime.time(19, 30)),  # 周五
	5: (datetime.time(11, 30), datetime.time(20, 0)),  # 周六
	6: (datetime.time(11, 30), datetime.time(20, 0)),  # 周日
}


# VIP.csv 表头名
TH_VIP_ID = 'ID'
TH_VIP_LV = 'VIP等级'

# info.csv 表头名
TH_INFO_TIME = '时间'
TH_INFO_SID = '客服工号'
TH_INFO_TYPE = '聊天类型'
TH_INFO_PID = '玩家ID'
TH_INFO_CONTENT = '聊天内容'

# 常量
MSG_TYPE_RECV = "接收消息"
MSG_TYPE_SEND = "发送消息"

SID_SYSTEM = 'system'
