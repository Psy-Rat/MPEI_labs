# -*- coding: utf-8 -*-
import random as rnd
import matplotlib.pyplot as plt
import json
import sys

sys.setrecursionlimit(100000)


# 'beautiful text drawing'
def draw_text(ax, x, y, t, size=20, **kwargs):
    ax.text(x, y, t,
            ha='center', va='center', size=size,
            bbox=dict(boxstyle='round', ec='k', fc='w'), **kwargs)


# 'gini`s impurity'
def gini_impurity(aClasslist):
    """Main entropy characteristic
    Gini impurity is a measure of how often a randomly chosen element from the set would be incorrectly labeled if
    was randomly labeled according to the distribution of labels in the subset
    """
    class_map = {}
    for classy in aClasslist:
        if classy not in class_map:
            class_map[classy] = 0
        class_map[classy] += 1
    entropy = 1
    for lbl in class_map:
        entropy -= (class_map[lbl] / float(len(aClasslist)))**2
    return entropy


# 'bagging from CSV data file'
# 'Attention! Class/Label parameter must be in the last column!'
def bagging(aCSVData, b_perc=0.3, a_perc=0.1, labels=None):
    a = round(len(aCSVData) * a_perc)
    b = round(len(aCSVData) * b_perc)
    col_names = aCSVData.columns.values.tolist()
    if labels is None:
        labels = rnd.sample(col_names[:-1], rnd.randint(1, len(col_names)-1))
    translations = []
    for label in labels:
        translations.append(col_names.index(label))

    elems = rnd.sample(range(len(aCSVData)), rnd.randint(a, b))

    result_data = []

    for elem in elems:
        single_row = []
        for parm in labels:
            single_row.append(aCSVData[parm][elem])
        single_row.append(aCSVData[col_names[len(col_names) - 1]][elem])
        result_data.append(single_row)

    return result_data, labels, translations


# 'Question class'
class Question:
    # 'Constructor'
    def __init__(self, a_column, a_value):
        self.column = a_column
        self.value = a_value
        self.name = ""

    # 'Label setter'
    def set_label(self, a_name):
        self.name = a_name

    # 'Print method override'
    def __repr__(self):
        return self.question_text()

    # 'For textual quesition representation (For printing)'
    def question_text(self):
        if self.is_number(self.value):
            return "if  " + self.name + "\n >= \n" + str(self.value)
        else:
            return "if  " + self.name + "\n == \n" + str(self.value)

    # 'for data question representation (For json)'
    def get_as_data(self):
        return {"name": self.name, "column": self.column, "value": self.value}

    # 'Type matching'
    def is_number(self, a_instance):
        return isinstance(a_instance, int) or isinstance(a_instance, float)

    # 'You got a question? This gives an answer'
    def compare(self, aExample, transliteration=None):
        if transliteration is None:
            buffValue = aExample[self.column]
        else:
            buffValue = aExample[transliteration.index(self.column)]
        if self.is_number(buffValue):
            return buffValue >= self.value
        else:
            return buffValue == self.value


# 'Data structure class'
class DataWorks:
    def __init__(self, aDataMatrix, aLabels, aTranslations):
        self.data = aDataMatrix
        self.labels = aLabels
        self.translations = aTranslations

    # return map of [class : number of it`s appearance]
    def class_counts(self, aDataset):
        result = {}
        for row in aDataset:
            if row[-1] not in result:
                result[row[-1]] = 0
            result[row[-1]] += 1
        return result

    # return list of existing unique classes
    def getClasses(self):
        classlist = []
        for row in self.data:
            if row[-1] not in classlist:
                classlist.append(row[-1])
        return classlist

    # return list of labels
    def getLabelField(self):
        classlist = []
        for row in self.data:
            classlist.append(row[-1])
        return classlist

    # get gini impurity
    def getGini(self):
        return gini_impurity(self.getLabelField())

    def splitData(self, aQuestion):
        left = []
        right = []
        for row in self.data:
            if aQuestion.compare(row, self.translations):
                left.append(row)
            else:
                right.append(row)

        return DataWorks(left, self.labels, self.translations), DataWorks(right, self.labels, self.translations)

    def questionProfits(self, aQuestion):
        left_split, right_split = self.splitData(aQuestion)
        return (self.getGini()
                - left_split.getGini()*(len(left_split.data)/len(self.data))
                - right_split.getGini()*(len(right_split.data)/len(self.data))
                )

    # finding best choice
    def getBestQuestion(self):
        question_map = {}
        for row in self.data:
            for column in range(len(row)-1):
                q = Question(self.translations[column], row[column])
                q.set_label(self.labels[column])
                question_map[q] = self.questionProfits(q)

        best_question, best_gini = question_map.popitem()
        for k in question_map.keys():
            if question_map.get(k) > best_gini:
                best_question = k
                best_gini = question_map.get(k)
        return best_question
# 'Tree knot'


class DecisionNode:
    def __init__(self, aQuestion, aLeft, aRight):
        self.question = aQuestion
        self.left = aLeft
        self.right = aRight

    @classmethod
    def createFromData(cls, aQuestion, aLeft, aRight):
        print(aQuestion)
        thisLeft = []
        thisRight = []
        if len(aLeft.getClasses()) > 1:
            buffA, buffB = aLeft.splitData(aLeft.getBestQuestion())
            thisLeft = DecisionNode.createFromData(
                aLeft.getBestQuestion(), buffA, buffB)

        if len(aRight.getClasses()) > 1:
            buffA, buffB = aRight.splitData(aRight.getBestQuestion())
            thisRight = DecisionNode.createFromData(
                aRight.getBestQuestion(), buffA, buffB)

        chooser = (len(aLeft.getClasses()) > 1)*3 + \
            (len(aRight.getClasses()) > 1)*5
        #print("chooser: ", chooser, " | ThisLeft: ", thisLeft, " | thisRight: ", thisRight)
        if chooser == 0:
            return cls(aQuestion, aLeft.getClasses()[0], aRight.getClasses()[0])
        elif chooser == 3:
            return cls(aQuestion, thisLeft, aRight.getClasses()[0])
        elif chooser == 5:
            return cls(aQuestion, aLeft.getClasses()[0], thisRight)
        else:
            return cls(aQuestion, thisLeft, thisRight)

    @classmethod
    def createFromJson(cls, aJson):
        if isinstance(aJson, int) or isinstance(aJson, float) or isinstance(aJson, str):
            return aJson

        question = Question(aJson[0]['column'], aJson[0]['value'])
        question.set_label(aJson[0]['name'])
        return cls(question, DecisionNode.createFromJson(aJson[1]), DecisionNode.createFromJson(aJson[2]))

    def findAnswer(self, aDataRow, translations):
        if self.question.compare(aDataRow, translations):
            if isinstance(self.left, DecisionNode):
                return self.left.findAnswer(aDataRow, translations)
            else:
                return self.left
        else:
            if isinstance(self.right, DecisionNode):
                return self.right.findAnswer(aDataRow, translations)
            else:
                return self.right

    def drawItself(self):
        return self.question.question_text()


# 'Tree itself'
class DecisionTree:
    def __init__(self, aHead):
        self.fig = None
        self.ax = None
        self.head = aHead

    # Different creators:
    @classmethod
    def createFromData(cls, aTrainingData):
        a1, a2 = aTrainingData.splitData(aTrainingData.getBestQuestion())
        return cls(DecisionNode.createFromData(aTrainingData.getBestQuestion(), a1, a2))

    @classmethod
    def LoadHead(cls, aJsoned_tree):
        if isinstance(aJsoned_tree, int) or isinstance(aJsoned_tree, float) or isinstance(aJsoned_tree, str):
            return aJsoned_tree

        return(cls(DecisionNode.createFromJson(aJsoned_tree)))

    @classmethod
    def createFromFile(cls, aFileName):
        with open(aFileName, 'r') as infile:
            jsoned_tree = json.load(infile)
        return cls.LoadHead(jsoned_tree)

    # Methods:

    def findAnswer(self, aDataRow, translations=None):
        if translations is None:
            translations = range(0, len(aDataRow))
        return self.head.findAnswer(aDataRow, translations)

    def drawPart(self, aNextNode, anLastLength, anLastHeight):
        if isinstance(aNextNode, int) or isinstance(aNextNode, float) or isinstance(aNextNode, str):
            draw_text(self.ax, anLastLength, anLastHeight, aNextNode, 10)
            return anLastHeight - 0.1
        else:
            self.ax.plot([anLastLength, anLastLength + 0.4],
                         [anLastHeight, anLastHeight], '-k', color="g")
            new_height = self.drawPart(
                aNextNode.left, anLastLength + 0.4, anLastHeight)
            self.ax.plot([anLastLength, anLastLength + 0.4],
                         [anLastHeight, new_height], '-k', color="firebrick")
            new_height = self.drawPart(
                aNextNode.right, anLastLength + 0.4, new_height)
            draw_text(self.ax, anLastLength, anLastHeight,
                      aNextNode.question.question_text(), 10)
            return new_height

    def savePart(self, aNextNode):
        if isinstance(aNextNode, int) or isinstance(aNextNode, float) or isinstance(aNextNode, str):
            return aNextNode
        else:
            return [aNextNode.question.get_as_data(),  self.savePart(aNextNode.left), self.savePart(aNextNode.right)]

    def saveTree(self, aFile):
        print(self.savePart(self.head))
        print(json.dumps(self.savePart(self.head)))
        with open(aFile, 'w') as outfile:
            json.dump(self.savePart(self.head), outfile,
                      indent=2, separators=(',', ': '))

    def loadTree(self, aFile):
        with open(aFile, 'r') as infile:
            jsoned_tree = json.load(infile)
        print(jsoned_tree)

    def drawTree(self):
        self.fig = plt.figure(figsize=(10, 10))
        self.ax = self.fig.add_axes(
            [0, 0, 0.8, 1], frameon=False, xticks=[], yticks=[])
        self.drawPart(self.head, 0, 1)
        #draw_text(self.ax, 0, 1, self.head.question.question_text(), 10)
        plt.show()


'''
fixed_df = pd.read_csv('data/voice.csv')

tree_pool, labels, translations = bagging(fixed_df, 0.05, 0.05)

checkingData = DataWorks(tree_pool, labels,translations)

tree = DecisionTree.createFromData(checkingData)#DecisionTree(checkingData)
tree.drawTree()
tree.saveTree('test_json.json')
tree.loadTree('test_json.json')
LoadedTree = DecisionTree.createFromFile('test_json.json')
LoadedTree.drawTree()

ansv = 0
for dataRow in tree_pool:
    answer = str(tree.findAnswer(dataRow, translations))
    label = str(dataRow[-1])
    if answer == label:
            ansv += 1
    else:
            print("wtf  " + answer + "   " + label)
print("len = " + str(len(tree_pool)) + "\nansver:" + str(ansv))

ansv = 0
for dataRow in fixed_df.values:
    answer = str(tree.findAnswer(dataRow))
    label = str(dataRow[-1])
    if answer == label:
        ansv += 1
    else:
        print("wtf  " + answer + "   " + label)
print("len = " + str(len(fixed_df.values)) + "\nansver:" + str(ansv))
'''
