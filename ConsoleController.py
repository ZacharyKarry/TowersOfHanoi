# Copyright 2014 Dustin Wehr
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSC148, Winter 2014.
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""
ConsoleController: User interface for manually solving Anne Hoy's problems
from the console.

move: Apply one move to the given model, and print any error message
to the console.
"""

from TOAHModel import TOAHModel, Cheese, IllegalMoveError
import random


def move(model: TOAHModel, origin: int, dest: int):
    '''
    Module method to apply one move to the given model, and print any
    error message to the console.

    model - the TOAHModel that you want to modify
    origin - the stool number (indexing from 0!) of the cheese you want
             to move
    dest - the stool number that you want to move the top cheese
            on stool origin onto.
    '''
    try:
        model.move(origin, dest)
    except IllegalMoveError:
        #This is so we can give the interface some "personality"
        rand = random.randint(1, 3)
        if rand == 1:
            print("Whoops! Can't do that!")
        elif rand == 2:
            print("Clearly someone needs to read the instructions again!")
        else:
            print("I can't let you do that.")
    except KeyError:
        print("That stool doesn't exist dummy.")


def is_move(query: str) -> bool:
    """
    Determines if a query is a move.

    >>> is_move("1 2")
    True
    >>> is_move("a b")
    False
    >>> is_move("123")
    False
    """
    check = query.split()
    if len(check) == 2:
        try:
            int(check[0])
            int(check[1])
        except:
            return False
        return True
    return False


class ConsoleController:

    def __init__(self: 'ConsoleController',
                 number_of_cheeses: int, number_of_stools: int):
        """
        Initialize a new 'ConsoleController'.

        number_of_cheeses - number of cheese to tower on the first stool
        number_of_stools - number of stools
        """
        self.model = TOAHModel(number_of_stools)
        self.model.fill_first_stool(number_of_cheeses)
        self.has_seen_instructions = False

    def intro(self: 'ConsoleController') -> None:
        """
        Simply prints an introduction to the console.
        """
        print('--------------------------------------------------')
        print('|    Welcome to the Towers of Anne Hoi game!     |')
        print('|       Can you move all of the cheeses?         |')
        print("|Be careful though, you can't put a cheese on top|")
        print('|              of a smaller cheese.              |')
        print('|                   Good Luck!                   |')
        print('--------------------------------------------------')

    def display_instructions(self: 'ConsoleController'):
        """
        Prints instructions to the console.
        """
        print("Moves are entered in the following format:")
        print("'Location Stool' 'Destination Stool'")
        print("Separated by a space. ex. '1 2' moves the cheese")
        print("from the first stool to the second.")

    def process_query(self: "ConsoleController", query: str):
        """
        Takes an input, and applies the appropriate command.

        """
        #applies the move if it is indeed a move, or prints instructions
        #the only other valid command is exit which is accounted for in
        #play_loop
        if is_move(query):
            relocation = query.split()
            #I decided to make the first stool 1 instead of 0
            #since it seems more intuitive to a user who doesn't
            #program.
            location = int(relocation[0]) - 1
            destination = int(relocation[1]) - 1
            move(self.model, location, destination)
        elif query.lower() == 'i':
            self.has_seen_instructions = False

    def play_loop(self: 'ConsoleController'):
        '''
        Console-based game.
        TODO:
        -Start by giving instructions about how to enter moves (which is up to
        you). Be sure to provide some way of exiting the game, and indicate
        that in the instructions.
        -Use python's built-in function input() to read a potential move from
        the user/player. You should print an error message if the input does
        not meet the specifications given in your instruction or if it denotes
        an invalid move (e.g. moving a cheese onto a smaller cheese).
        You can print error messages from this method and/or from
        ConsoleController.move; it's up to you.
        -After each valid move, use the method TOAHModel.__str__ that we've
        provided to print a representation of the current state of the game.
        '''
        self.intro()
        query = ''
        print(self.model)

        while not query.lower() == 'e':
            #So that we only see the instructions when wanted
            if not self.has_seen_instructions:
                self.display_instructions()
                self.has_seen_instructions = True
            else:
                print(self.model)
            print("Type 'i' to see instructions again. 'e' to exit")
            query = input("Please enter a move:")
            self.process_query(query)
        print("Goodbye!")

if __name__ == '__main__':
    # TODO:
    # You should initiate game play here. Your game should be playable by
    # running this file.
    stools = 4
    cheeses = 5

    game = ConsoleController(cheeses, stools)
    game.play_loop()