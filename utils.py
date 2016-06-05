# -*- coding:gbk -*-

import csv
import datetime
import const


class Msg(object):
	def __init__(self, msgId, pid, sid, when, msgType, content):
		self.id = msgId
		self.pid = pid
		self.sid = sid
		self.time = when
		self.type = msgType
		self.content = content


def getPid2Lv(path, delimiter=','):
	pid2lv = dict()
	with open(path, 'rb') as f:
		reader = csv.DictReader(f, delimiter=delimiter)
		for row in reader:
			pid = int(row[const.TH_VIP_ID])
			lv = int(row[const.TH_VIP_LV])
			pid2lv[pid] = lv
	return pid2lv


def getMsgList(path, delimiter='\t'):
	msglist = list()
	idx = 0

	with open(path, 'rb') as f:
		reader = csv.DictReader(f, delimiter=delimiter)
		for row in reader:
			time = datetime.datetime.strptime(row[const.TH_INFO_TIME], "%Y-%m-%d %H:%M:%S")
			sid = row[const.TH_INFO_SID]
			msgtype = row[const.TH_INFO_TYPE]

			if msgtype != const.MSG_TYPE_RECV and msgtype != const.MSG_TYPE_SEND:
				continue

			pid = int(row[const.TH_INFO_PID])
			content = row[const.TH_INFO_CONTENT]
			msglist.append(Msg(idx, pid, sid, time, msgtype, content))
			idx += 1

	return msglist


def getFirstReplyAfter(msglist, time):
	for msg in msglist:
		if msg.type == const.MSG_TYPE_SEND and msg.time >= time:
			return msg
	return None
