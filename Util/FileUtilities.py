import re


class FileUtilities:

    @staticmethod
    def readLines(filePath):
        f = open(filePath)
        data1 = f.read()
        f.close()
        s = []
        lines1 = data1.split('\n')
        for line in lines1:
            if line is not "":
                s.append(line)
        return s

    @staticmethod
    def readClueList(filePath):
        strings = []
        endClues = []
        result = [[],[]]
        f = open(filePath)
        data1 = f.read()
        lines1 = data1.split('\n')
        for line in lines1:
            if line is not "":
                temp = line.split("]")
                strings.append(temp[1])
                if re.match('\[E', line):
                    endClues.append(temp[1])
        result[0].append(strings)
        result[1].append(endClues)
        return result

    @staticmethod
    def readAdditionalData(filePath):
        clues = []
        patterns = []
        f = open(filePath)
        data1 = f.read()
        lines1 = data1.split('\n')
        for line in lines1:
            temp = line.split("]")
            if re.match(line, "[clue]"):
                clues.append(temp[1])
            elif re.match(line, "[pattern]"):
                patterns.append(temp[1])
        result = [[], []]
        result[0].append(clues)
        result[1].append(patterns)
        return result


    @staticmethod
    def readSvmResults(filePath):
        svmHash = []
        f = open(filePath)
        data1 = f.read()
        lines1 = data1.split('\n')
        for line in lines1:
            temp = line.split("\t")
            svmHash[temp[1]].append(int(temp[0]))
        return svmHash
