'''
Project: Choose Your Own Adventure Game
Team Members: Michael Chen, Kevin Guan, Preston Meek
Due Date: 5/9/2022
Task Description: Design a school-appropriate program that will let users move through rooms based on user input 
and get descriptions of each room.
'''

import pygame

class Key:
    checkedKeys  = []
    releasedKeys = []
    toggledKeys  = {}

    @staticmethod
    def addKey(key):
        Key.checkedKeys.append(key)
        Key.releasedKeys.append(key)

    @staticmethod
    def tick():
        for key in Key.checkedKeys:
            if pygame.key.get_pressed()[key] and key in Key.releasedKeys:
                Key.releasedKeys.remove(key)
                
                # flip the boolean if it has already been assigned
                # otherwise, just set it to true (aka first time being pressed)
                if key in Key.toggledKeys:
                    Key.toggledKeys[key] = not Key.toggledKeys[key]
                else:
                    Key.toggledKeys[key] = True

            if not pygame.key.get_pressed()[key] and key not in Key.releasedKeys:
                Key.releasedKeys.append(key)

    # checks if a key has been toggled or not
    @staticmethod
    def isToggled(key):
        if key in Key.toggledKeys:
            return Key.toggledKeys[key]
        else:
            return False