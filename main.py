# -*- coding:gbk -*-

import csv
from processor import DataProcessor


VipLvPath = './input/vip.csv'
InfoPath = './input/聊天记录.csv'


def calcFirstReplyInOneDayData(outputPath, includeSystem=True):
	dp = DataProcessor(VipLvPath, InfoPath)
	dp.preprocess(includeSystem=includeSystem)

	with open(outputPath, 'wb+') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(["等级", "玩家发送信息总量", "3分钟内响应总量", "3分钟内响应率", "平均响应时长"])
		for lv in sorted(dp.lvset):
			output = dp.calcLvDataInOneday(lv)
			if not output:
				continue
			writer.writerow(output)


def calcFirstReplyData(outputPath, includeSystem=True):
	dp = DataProcessor(VipLvPath, InfoPath)
	dp.preprocess(includeSystem=includeSystem)

	with open(outputPath, 'wb+') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(["等级", "玩家发送信息总量", "3分钟内响应总量", "3分钟内响应率", "平均响应时长"])
		for lv in sorted(dp.lvset):
			output = dp.calcLvData(lv)
			if not output:
				continue
			writer.writerow(output)


def calcFirstReplyDetail(outputPath, includeSystem=True):
	dp = DataProcessor(VipLvPath, InfoPath)
	dp.preprocess(includeSystem=includeSystem)

	with open(outputPath, 'wb+') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(["客服ID", "玩家ID", "玩家VIP等级", "接收玩家消息时间", "玩家消息内容", "回复玩家消息时间", "回复玩家内容", "回复间隔"])
		details = dp.calcFirstReplyDetail()
		for output in details:
			if not output:
				continue
			writer.writerow(output)


def calcAllFirstReplyDetail(outputPath):
	dp = DataProcessor(VipLvPath, InfoPath)
	dp.preprocess(includeSystem=False, filterNotOnDuty=False, filterOffWork=False)

	with open(outputPath, 'wb+') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(["客服ID", "玩家ID", "玩家VIP等级", "接收玩家消息时间", "玩家消息内容", "回复玩家消息时间", "回复玩家内容", "回复间隔"])
		details = dp.calcFirstReplyDetail()
		for output in details:
			if not output:
				continue
			writer.writerow(output)


def calcPidWithoutLv(outputPath):
	dp = DataProcessor(VipLvPath, InfoPath)
	dp.preprocess(includeSystem=False)

	pidset = set()
	for msg in dp.msglist:
		if msg.pid not in dp.pid2lv:
			pidset.add(msg.pid)

	with open(outputPath, 'wb+') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(["缺等级信息玩家ID"])
		for pid in pidset:
			writer.writerow([pid, ])


calcPidWithoutLv("./output/缺等级信息玩家ID.csv")

calcFirstReplyData('./output/三分钟响应数据-包含系统.csv', includeSystem=True)
calcFirstReplyData('./output/三分钟响应数据.csv', includeSystem=False)

calcFirstReplyInOneDayData("./output/每日首次-三分钟响应数据-包含系统.csv", includeSystem=True)
calcFirstReplyInOneDayData("./output/每日首次-三分钟响应数据.csv", includeSystem=False)

calcFirstReplyDetail("./output/当班时间内响应明细-包含系统.csv", includeSystem=True)
calcFirstReplyDetail("./output/当班时间内响应明细.csv", includeSystem=False)

calcAllFirstReplyDetail("./output/响应明细.csv")
