#encoding=utf-8
# from openpyxl import load_workbook
import xlrd
import re
import json

class excelNERToEntity(object):

    def __init__(self):
        self.vacb = ['L', 'C', 'INS', 'PRO', 'P', 'IND']

    def readFile(self, path):
        return xlrd.open_workbook(path)

    def processLine(self, sheetName, wb):

        sheet = wb.sheet_by_name(sheetName)
        nrows = sheet.nrows
        ncols = sheet.ncols
        sentenseList = []
        for i in range(0,nrows):
            textMap = {}
            entityListAndType = []
            textMap['entities'] = []
            for j in range(0,ncols):


                if (j == 0):
                    textMap['text'] = sheet.cell(i,j).value

                else:

                    if (len(sheet.cell(i,j).value)!=0):
                        entityListAndType.extend(re.split('[：:]',sheet.cell(i,j).value))

            for q,t in enumerate(entityListAndType):
                if t in self.vacb:
                    textMap['entities'] = self.getEntityMap(textMap['entities'],textMap['text'],entityListAndType[q-1],t)

            sentenseList.append(textMap)
        #     print('---------------------')
        #     print(i)
        #     print(textMap)
        # print(sentenseList)
        return  sentenseList

    def getEntityMap(self, entityList, sentence, entity, type):
        if (sentence.find(entity) != -1):
            list = [t.start() for t in re.finditer(entity, sentence)]
            for index in list:
                entityMap = {}
                entityMap['word'] = entity
                entityMap['start'] = index
                entityMap['end'] = index + len(entity)
                entityMap['type'] = type
                entityList.append(entityMap)
        return entityList

    def write(self, sentenList,path):
        with open(path,'w',encoding='utf-8') as t:
            for i in sentenList:

                t.write(json.dumps(i,ensure_ascii=False) + '\n')

    def test(self):
        sentList = A.processLine('sheet1', wb)
        n = 0
        for i in sentList:
            text = i['text']
            # print(text)
            if '投资' in text:
                n += 1
                print(n)
                print(text)
                print('-------------------')



A = excelNERToEntity()
A.__init__()
wb = A.readFile('/users/anlei/Documents/标注任务/nlp-datasets/实体标注/1.1-2.20.xls')
A.test()
# A.write(A.processLine('sheet1', wb), './data/1.1-2.20.txt')