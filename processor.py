# -*- coding:gbk -*-

import utils
import const


class DataProcessor(object):
	def __init__(self, vipTablePath, infoTablePath):
		super(DataProcessor, self).__init__()
		self.vipTablePath = vipTablePath
		self.infoTablePath = infoTablePath

	def filterNotOnDutyMsg(self):
		msglist = []

		for msg in self.msglist:
			weekday = msg.time.weekday()
			time = msg.time.time()
			if const.Weekday2DutyTime[weekday][0] < time < const.Weekday2DutyTime[weekday][-1]:
				msglist.append(msg)
		return msglist

	def filterOffWorkMsg(self):
		numberMap = dict()
		for msg in self.msglist:
			if msg.type == const.MSG_TYPE_SEND and msg.sid != const.SID_SYSTEM:
				key = (msg.sid, msg.time.date())
				numberMap.setdefault(key, 0)
				numberMap[key] += 1

		offWorkKeys = set(key for key, num in numberMap.iteritems() if num < 10)
		self.offWorkKeys = offWorkKeys

		return [msg for msg in self.msglist if (msg.sid, msg.time.date()) not in offWorkKeys]

	def filterSystemMsg(self):
		return [msg for msg in self.msglist if msg.sid != const.SID_SYSTEM]

	def preprocess(self, includeSystem=True, filterOffWork=True, filterNotOnDuty=True):
		self.pid2lv = utils.getPid2Lv(self.vipTablePath)
		self.msglist = utils.getMsgList(self.infoTablePath)

		self.lvset = set(lv for lv in self.pid2lv.itervalues())
		self.dateset = set(msg.time.date() for msg in self.msglist)
		self.pidset = set(msg.pid for msg in self.msglist)
		self.sidset = set(msg.sid for msg in self.msglist)

		if filterNotOnDuty:
			self.msglist = self.filterNotOnDutyMsg()

		if filterOffWork:
			self.msglist = self.filterOffWorkMsg()

		if not includeSystem:
			self.msglist = self.filterSystemMsg()

		self.pid2msglist = self.getPid2MsgList()

	def getPid2MsgList(self):
		pid2msglist = dict()
		for msg in self.msglist:
			msglist = pid2msglist.setdefault(msg.pid, list())
			msglist.append(msg)
		return pid2msglist

	def calcLvData(self, lv2process):
		sumRecv = 0
		sumReplyIn3Mins = 0
		sumFirstReplyTime = 0

		for pid, msglist in self.pid2msglist.iteritems():
			if pid not in self.pid2lv:
				continue

			if self.pid2lv[pid] != lv2process:
				continue

			msglist = sorted(msglist, key=lambda msg: msg.time)

			for msgRecv in msglist:
				if msgRecv.type != const.MSG_TYPE_RECV:
					continue
				sumRecv += 1
				firstReply = utils.getFirstReplyAfter(msglist, msgRecv.time)
				if firstReply:
					delta = firstReply.time - msgRecv.time
					sumFirstReplyTime += delta.total_seconds()
					if delta.total_seconds() <= 3 * 60:
						sumReplyIn3Mins += 1

		if sumRecv:
			avgFirstReplyTime = sumFirstReplyTime / float(sumRecv)
			replyIn3MinsRate = sumReplyIn3Mins / float(sumRecv)
			return lv2process, sumRecv, sumReplyIn3Mins, replyIn3MinsRate, avgFirstReplyTime
		return None

	def calcLvDataInOneday(self, lv2process):
		sumRecv = 0
		sumReplyIn3Mins = 0
		sumFirstReplyTime = 0

		for pid, msglist in self.pid2msglist.iteritems():
			if pid not in self.pid2lv:
				continue

			if self.pid2lv[pid] != lv2process:
				continue

			msglist = sorted(msglist, key=lambda msg: msg.time)

			datecalced = set()
			for msgRecv in msglist:
				if msgRecv.time.date() in datecalced:
					continue

				datecalced.add(msgRecv.time.date())
				if msgRecv.type != const.MSG_TYPE_RECV:
					continue

				sumRecv += 1
				firstReply = utils.getFirstReplyAfter(msglist, msgRecv.time)
				if firstReply:
					delta = firstReply.time - msgRecv.time
					sumFirstReplyTime += delta.total_seconds()
					if delta.total_seconds() <= 3 * 60:
						sumReplyIn3Mins += 1

		if sumRecv:
			avgFirstReplyTime = sumFirstReplyTime / float(sumRecv)
			replyIn3MinsRate = sumReplyIn3Mins / float(sumRecv)
			return lv2process, sumRecv, sumReplyIn3Mins, replyIn3MinsRate, avgFirstReplyTime
		return None

	def calcFirstReplyDetail(self):
		details = list()

		for pid, msglist in self.pid2msglist.iteritems():
			if pid not in self.pid2lv:
				continue

			msglist = sorted(msglist, key=lambda msg: msg.time)

			for msgRecv in msglist:
				if msgRecv.type != const.MSG_TYPE_RECV:
					continue

				firstReply = utils.getFirstReplyAfter(msglist, msgRecv.time)
				if firstReply:
					delta = firstReply.time - msgRecv.time
					details.append([
						msgRecv.sid, pid, self.pid2lv[pid], msgRecv.time, msgRecv.content, firstReply.time, firstReply.content, delta.total_seconds() / 60.0
					])
				else:
					details.append([msgRecv.sid, pid, self.pid2lv[pid], msgRecv.time, msgRecv.content, '未回复', '未回复', '未回复'])

		return details
