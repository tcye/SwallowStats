# -*- coding:gbk -*-

import datetime


Weekday2DutyTime = {
	0: (datetime.time(10, 0), datetime.time(19, 30)),  # ��һ
	1: (datetime.time(10, 0), datetime.time(19, 30)),  # �ܶ�
	2: (datetime.time(11, 30), datetime.time(20, 0)),  # ����
	3: (datetime.time(10, 0), datetime.time(19, 30)),  # ����
	4: (datetime.time(10, 0), datetime.time(19, 30)),  # ����
	5: (datetime.time(11, 30), datetime.time(20, 0)),  # ����
	6: (datetime.time(11, 30), datetime.time(20, 0)),  # ����
}


# VIP.csv ��ͷ��
TH_VIP_ID = 'ID'
TH_VIP_LV = 'VIP�ȼ�'

# info.csv ��ͷ��
TH_INFO_TIME = 'ʱ��'
TH_INFO_SID = '�ͷ�����'
TH_INFO_TYPE = '��������'
TH_INFO_PID = '���ID'
TH_INFO_CONTENT = '��������'

# ����
MSG_TYPE_RECV = "������Ϣ"
MSG_TYPE_SEND = "������Ϣ"

SID_SYSTEM = 'system'
