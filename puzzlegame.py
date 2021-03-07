import copy
import time

field = [[],
         [],
         []]

goal = [[],
        [],
        []]

objectList = []
objectList2 = []
memory = []

flag = False
layerCount = 2

class Step:
    def __init__(self, matrix, parent):
        self.matrix = matrix
        self.parent = parent
        self.children = []
        for i in range(3): #najde pozici volneho policka
            for n in range(3):
                if self.matrix[i][n] == "X":
                    self.pointerPos = [i, n]
        self.directions = ["up", "down", "left", "right"] #najde vsechny dalsi mozne kroky
        if self.pointerPos[0] == 0:
            self.directions.remove("up")
        elif self.pointerPos[0] == 2:
            self.directions.remove("down")
        if self.pointerPos[1] == 0:
            self.directions.remove("left")
        elif self.pointerPos[1] == 2:
            self.directions.remove("right")

    def calculate(self): #projde vsechny mozne smery, posune X a vytvori dalsi kroky
        for direction in self.directions:
            matrixCopy = copy.deepcopy(self.matrix)
            if direction == "up":
                numberToSwap = matrixCopy[self.pointerPos[0]-1][self.pointerPos[1]]
                matrixCopy[self.pointerPos[0]-1][self.pointerPos[1]] = "X"
                matrixCopy[self.pointerPos[0]][self.pointerPos[1]] = numberToSwap
            elif direction == "down":
                numberToSwap = matrixCopy[self.pointerPos[0]+1][self.pointerPos[1]]
                matrixCopy[self.pointerPos[0]+1][self.pointerPos[1]] = "X"
                matrixCopy[self.pointerPos[0]][self.pointerPos[1]] = numberToSwap
            elif direction == "left":
                numberToSwap = matrixCopy[self.pointerPos[0]][self.pointerPos[1]-1]
                matrixCopy[self.pointerPos[0]][self.pointerPos[1]-1] = "X"
                matrixCopy[self.pointerPos[0]][self.pointerPos[1]] = numberToSwap
            elif direction == "right":
                numberToSwap = matrixCopy[self.pointerPos[0]][self.pointerPos[1]+1]
                matrixCopy[self.pointerPos[0]][self.pointerPos[1]+1] = "X"
                matrixCopy[self.pointerPos[0]][self.pointerPos[1]] = numberToSwap
            if self.parent == None:
                self.children.append(Step(copy.deepcopy(matrixCopy), self))
            elif matrixCopy != self.parent.matrix:
                self.children.append(Step(copy.deepcopy(matrixCopy), self))


def insertIntoMatrix(data, matrix): #funkce na premenu stringu na matitci
    x = 0
    for i in range(3):
        for n in range(3):
            matrix[i].append(data[x])
            x += 1
    return matrix


fieldInput = input("Zadejte pocatecni matici: ") #user input a zpracovani
goalInput = input("Zadejte cilovou matici: ")

start = time.perf_counter()

fieldList = fieldInput.split(",")
goalList = goalInput.split(",")

insertIntoMatrix(fieldList, field)
insertIntoMatrix(goalList, goal)

firstStep = Step(field, None) #zkontroluje jestli hned 2. vrstva je goal
firstStep.calculate()
for child in firstStep.children:
    if child.matrix == goal: #jestli se najde vysledek, vypise se result.txt soubor
        flag = True
        f = open("result.txt", "w")
        f.write("Start matrix:\n")
        for i in field:
            f.write(f"|{i[0]}, {i[1]}, {i[2]}|\n")
        f.write("\nGoal matrix:\n")
        for i in goal:
            f.write(f"|{i[0]}, {i[1]}, {i[2]}|\n")
        f.write("\nResults:\n")
        f.write("Layer 1\n")
        for i in child.parent.matrix:
            f.write(f"|{i[0]}, {i[1]}, {i[2]}|\n")
        f.write("\nLayer 2\n")
        for i in child.matrix:
            f.write(f"|{i[0]}, {i[1]}, {i[2]}|\n")
        print("Calculation finished.")
    else:
        objectList.append(child)

while flag == False: #dokola prochazi, kontroluje goal a pocita dalsi vrstvy
    print("Layer ", layerCount)
    print(len(objectList))
    for step in objectList:
        step.calculate()
        for child in step.children:
            if child.matrix in memory: #jestli je matice v pameti, preskoci
                pass
            else: #jestli je matice nova, prida do
                memory.append(child.matrix)
                objectList2.append(child)
    objectList = copy.deepcopy(objectList2)
    for step in objectList:
        if step.matrix == goal: #jestli se najde vysledek, vypise se result.txt soubor
            end = time.perf_counter()
            print("Time: ", end - start)
            time.sleep(5)
            flag = True
            f = open("result.txt", "w")
            f.write("Start matrix:\n")
            for i in field:
                f.write(f"|{i[0]}, {i[1]}, {i[2]}|\n")
            f.write("\nGoal matrix:\n")
            for i in goal:
                f.write(f"|{i[0]}, {i[1]}, {i[2]}|\n")
            results = [step.matrix]
            stepCopy = step
            for i in range(layerCount):
                parent = stepCopy.parent
                results.append(parent.matrix)
                stepCopy = parent
            results.reverse()
            f.write("\nResults:\n")
            layerPrintout = 1
            for n in results:
                f.write(f"Layer {layerPrintout}:\n")
                for i in n:
                    f.write(f"|{i[0]}, {i[1]}, {i[2]}|\n")
                f.write("\n")
                layerPrintout += 1
            f.write(f"\n Time: {end - start}")
            f.close()
            print("Calculation finished.")
    layerCount += 1