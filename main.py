# -*- coding:gbk -*-

import csv
from processor import DataProcessor


VipLvPath = './input/vip.csv'
InfoPath = './input/�����¼.csv'


def calcFirstReplyInOneDayData(outputPath, includeSystem=True):
	dp = DataProcessor(VipLvPath, InfoPath)
	dp.preprocess(includeSystem=includeSystem)

	with open(outputPath, 'wb+') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(["�ȼ�", "��ҷ�����Ϣ����", "3��������Ӧ����", "3��������Ӧ��", "ƽ����Ӧʱ��"])
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
		writer.writerow(["�ȼ�", "��ҷ�����Ϣ����", "3��������Ӧ����", "3��������Ӧ��", "ƽ����Ӧʱ��"])
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
		writer.writerow(["�ͷ�ID", "���ID", "���VIP�ȼ�", "���������Ϣʱ��", "�����Ϣ����", "�ظ������Ϣʱ��", "�ظ��������", "�ظ����"])
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
		writer.writerow(["�ͷ�ID", "���ID", "���VIP�ȼ�", "���������Ϣʱ��", "�����Ϣ����", "�ظ������Ϣʱ��", "�ظ��������", "�ظ����"])
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
		writer.writerow(["ȱ�ȼ���Ϣ���ID"])
		for pid in pidset:
			writer.writerow([pid, ])


calcPidWithoutLv("./output/ȱ�ȼ���Ϣ���ID.csv")

calcFirstReplyData('./output/��������Ӧ����-����ϵͳ.csv', includeSystem=True)
calcFirstReplyData('./output/��������Ӧ����.csv', includeSystem=False)

calcFirstReplyInOneDayData("./output/ÿ���״�-��������Ӧ����-����ϵͳ.csv", includeSystem=True)
calcFirstReplyInOneDayData("./output/ÿ���״�-��������Ӧ����.csv", includeSystem=False)

calcFirstReplyDetail("./output/����ʱ������Ӧ��ϸ-����ϵͳ.csv", includeSystem=True)
calcFirstReplyDetail("./output/����ʱ������Ӧ��ϸ.csv", includeSystem=False)

calcAllFirstReplyDetail("./output/��Ӧ��ϸ.csv")
