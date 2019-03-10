#encoding=utf-8
import json
class entityJsonToTrain(object):

    def __init__(self):
        self.vocab = [',','。','，']


    def read(self, path):
        jsonList = []
        with open(path,encoding='utf-8') as T:
            for i  in T.readlines():
                i = i.strip('\n')
                jsonList.append(json.loads(i))
        return jsonList

    def processJson(self, jsonList):
        result = []
        n = 0
        for i in jsonList:
            n += 1
            type = ['O' for j in range(0,len(i['text']))]
            for j in i['entities']:
                type[j['start']] = 'B-' + j['type']
                for t in range(j['start']+1,j['end']):
                    type[t] = 'I-' + j['type']

            for p,q in enumerate(i['text']):
                temp = ''
                if q not in self.vocab:
                    temp = q + " " + type[p]

                result.append(temp)
            result.append('')

        return result

    def write(self, path, result):
        with open(path,'w',encoding='utf-8') as T:
            for i in result:
                T.write(i+"\n")


    def test(self, jsonList):
        result = []
        for i in jsonList:
            print(i['entities'])
            for j in i['entities']:
                print(1)


A = entityJsonToTrain()
jsonList = A.read('./data/1.1-2.20.txt')
result = A.processJson(jsonList)
A.write('./data/1.1-2.20_train.txt',result)
