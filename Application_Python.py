#@author: Isaac Altice
#@Date: 09/15/2020

import math
#Functions
# 1
def reverseOrder(list1):
    reversedList = []
    length = len(list1)
    while(length > 0):
        reversedList.append(list1[length -1])
        length -= 1
    return reversedList
#test
testList = [1,2,3]
print(reverseOrder(testList))
# 2
def maxIndex(list1):
    index = 0
    maxAt = 0
    for item in list1:   
        if item > list1[maxAt]:
           maxAt = index
        index += 1    
    return maxAt
#test
testList = [1,2,3,1,2]
print(maxIndex(testList))
# 3
def oddList(list1):
    oddList1 = [num for num in list1 if num % 2 == 1]
    return oddList1
#test
testList = [1,2,3,1,2]
print(oddList(testList))
# 4
def euclideanDistance(list1, list2):
    sumNums = 0
    dimensions = len(list1) -1
    while dimensions > -1:
        sumNums += (list1[dimensions] - list2[dimensions])**2
        dimensions -= 1
    return math.sqrt(sumNums)
#test
testList1 = [1,2]
testList2 = [1,-1]
print(euclideanDistance(testList1,testList2))
# 5
def fileToList(file1):
    fileContents = []
    file = open(file1, "r")
    for line in file:
        fileContents.append(line)
    file.close()
    return fileContents
#test
#print(fileToList("test.txt.txt"))

# 6
def listToFile(file1,list1):
    file = open(file1, "a")
    for element in list1:
        file.write("\n")
        file.write(element)
    file.close()
#test
#list1 = ["Test Line 4","Test Line 5"]
#listToFile("test.txt.txt", list1)
#Classes
#1
class BankAccount:
    #2
    id = 0
    balance = 0
    def __init__(self,ID,InitialDeposit):
        self.id = ID
        self.balance = InitialDeposit
    #3 & 4
    def deposit(self,depositAmount):
        self.balance += depositAmount
        return self.balance
    
    def withdraw(self,withdrawlAmount):
        if self.balance >= withdrawlAmount:
            self.balance -= withdrawlAmount
        else:
            print("Withdrawl amount was greater than account balance, no withdrawl made.")
        return self.balance
#5
bankAccount1 = BankAccount(1,1000)
bankAccount2 = BankAccount(2,2000)
#6
print('Account ID: ', bankAccount1.id)
print('Account Balance: $',bankAccount1.balance)
print('Deposit $500, Account Balance: $', bankAccount1.deposit(500))
print('Withdrawl $250, Account Balance: $', bankAccount1.withdraw(250))
print('Account ID: ', bankAccount2.id)
print('Account Balance: $',bankAccount2.balance)
print('Deposit $100, Account Balance: $', bankAccount2.deposit(100))
print('Withdrawl $2200, Account Balance: $', bankAccount2.withdraw(2200))
print('Account Balance: $',bankAccount2.balance)
print('Withdrawl $300, Account Balance: $', bankAccount2.withdraw(300))