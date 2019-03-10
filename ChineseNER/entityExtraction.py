# coding=gbk
import re
import xlwt
import xlrd
import xlutils
from xlutils.copy import copy

class entityExtract(object):

    def addressObtain(self,address):
        self.address = address

    def comSentenceOb(self,sentence):
        enAddLabel = re.findall(r'(@.+?\*)', sentence)
        ss = re.split(r'\[(@.+?\*)\]', sentence)
        for en in enAddLabel:
            for i in range(len(ss)):
                if ss[i] == en:
                    try:
                        ss[i] = re.findall(r'@(.+)#', en)[0]
                    except IndexError:
                        continue
            # sentenceCut = re.split(r'\[@%s\*\]'%en,sentence)
        return ''.join(ss)

    def xls_write(self):
        wt = xlrd.open_workbook(r'/home/transwarp/抽取实体/11.xls')
        wt_row = wt.sheets()[0].nrows
        excel = copy(wt)
        table = excel.get_sheet(0)

        wb = xlrd.open_workbook(r'/home/transwarp/抽取实体/jrj.part%s.xls'%self.address)
        xls_sheet = wb.sheets()[0]
        count = 0
        while True:
            try:
                row_value = xls_sheet.row_values(count)
            except IndexError:
                break
            for i in range(len(row_value)):
                if row_value[i]:
                    table.write(wt_row,i,row_value[i])
                else:
                    break
            wt_row = wt_row + 1
            count = count + 1

        excel.save(r'/home/transwarp/抽取实体/11.xls')



    def run(self):

        wb = xlwt.Workbook()
        mySheet = wb.add_sheet('sheet1')
        lineth = 0

        with open(r'/home/transwarp/抽取实体/jrj.part%s.txt.ann'%self.address, 'r', encoding='utf-8') as f:
            rawdata = f.readlines()[0].split('。')
            for sentence in rawdata:
                entity = re.findall(r'@(.+?)#', sentence)
                label = re.findall(r'#(.+?)\*', sentence)
                comSentence = self.comSentenceOb(sentence)
                if not entity:
                    continue
                else:
                    mySheet.write(lineth, 0, comSentence)
                    for i in range(len(entity)):
                        if len(re.split('[（\(].+[）\)]',entity[i]))>1:
                            entity[i] = ''.join(re.split('[（\(].+[）\)]',entity[i]))
                        try:
                            ee = entity[i] + ':' + label[i]

                            mySheet.write(lineth, i + 1, ''.join(re.split('[(（]',ee)))
                        except IndexError:
                            continue
                    lineth = lineth + 1
        wb.save(r'/home/transwarp/抽取实体/jrj.part%s.xls'%self.address)

if __name__ == '__main__':
    t = entityExtract()
    for i in range(1090):
        try:
            t.addressObtain(str(i))
            t.run()
            t.xls_write()
        except FileNotFoundError:
            continue
