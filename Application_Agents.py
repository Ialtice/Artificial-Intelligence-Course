# -*- coding: utf-8 -*-
"""
Created on (09/25/2020)

@author: Isaac Altice
"""

class Agent:
    name = ""
    environment = ""
    actuators = []
    sensors = []
    performanceMetrics = []
    
    def __init__(self,inName,inEnvironment,inActuators,inSensors,inPerformanceMetrics):
        self.name = inName
        self.environment = inEnvironment
        self.actuators = inActuators
        self.sensors = inSensors
        self.performanceMetrics = inPerformanceMetrics
        
    def print(self):
        print("----------------------------------------------------------------")
        print("Name: " + self.name +"\n")
        print("Environment: " + self.environment +"\n")
        print("Actuators:", end=" ")
        print(*self.actuators, sep= ", ")
        print()
        print("Sensors:", end=" ")
        print(*self.sensors, sep= ", ")
        print()
        print("Performance Metrics:", end=" ")
        print(*self.performanceMetrics,sep= ", ")
        print("----------------------------------------------------------------")
        print()
        
agent1 = Agent("Food Peeler", "kitchen", ["food holder","food peeler", "motor for food holder","motor for food peeler positioner"],
               ["safety sensor","food position sensor","on/off sensor"],["is food peeled","how much wasted","speed"])

agent2 = Agent("Snake","outdoor habitat",["mouth","body"],["eyes","tongue","heat sensors","nose", "ears"],["size","healthy","safe"] )

agent3 = Agent("Water tester", "bodies of water", ["Display", "On/Off Switch","Test probe" ], ["temperature", "ph", "contaminate",],["Purity", "Speed", "Accuracy"])

agent4 = Agent("Red light camera","Intersections",["Picture Sender","Photo trigger",], ["Camera","red light detector", "license place focuser", "driver focuser"],["Photo clarity", "Photo timing", "photo accuracy"])

agent5 = Agent("Auto Brightness Adjuster","Devices with Screens and brightness adjustability",["Brightness adjuster", "Brightness setting", "Optimal brightness calculator"],
               ["Outdoor environemnt light sensor", "Device brightness sensor"],
               ["Speed of adjustment", "Dependability", "Screen picture quality in terms of visibility"] )

agent1.print()
agent2.print()
agent3.print()
agent4.print()
agent5.print()