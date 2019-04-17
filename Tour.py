# Copyright 2013, 2014 Gary Baumgartner, Danny Heap, Dustin Wehr
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSC148, Fall 2013.
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
from ConsoleController import ConsoleController
from GUIController import GUIController
from TOAHModel import TOAHModel, MoveSequence

import time


def minimum(num_cheeses: int, depth: int=0) -> int:
    """Takes a number of cheeses, and returns the i that generated
    the minimum amount of moves according to the Frame-Stewart algorithm.

    >>> minimum(6)
    3
    >>> minimum(10)
    4
    >>> minimum(15)
    5
    >>> minimum(-2)
    0
    """
    depth += 1
    if num_cheeses == 1:
        return 1
    lowest = 0
    right_i = 0
    for i in range(1, num_cheeses):
        moves = (2 * minimum(num_cheeses - i, depth)) + (2 ** i) - 1
        if moves <= lowest or lowest == 0:
            lowest = moves
            right_i = i
    #This part returns i ONLY if we are on the shallowest recursive
    #depth, so we can use it recursively to get the lowest i and
    #at the same time use it easily for our intended purpose.
    if depth == 1:
        return right_i
    else:
        return lowest


def three_stool_solution(movelist: 'MoveSequence', n: int,
                         loc: int, mid: int, dest: int):
    """Adds to our movelist the moves for n cheeses given a number for
    location stool, middle stool, and destination stool.

    >>> move = MoveSequence([])
    >>> three_stool_solution(move, 3, 0, 1, 2)
    >>> move
    MoveSequence([(0, 2), (0, 1), (2, 1), (0, 2), (1, 0), (1, 2), (0, 2)])
    >>> move2 = MoveSequence([])
    >>> three_stool_solution(move2, 2, 4, 6, 15)
    >>> move2
    MoveSequence([(4, 6), (4, 15), (6, 15)])
    """
    if n == 1:
        movelist.add_move(loc, dest)
    else:
        #Moves n-1 cheeses to mid, moves the last cheese to
        #destination, and then moves the n-1 cheeses on top
        #of that.
        three_stool_solution(movelist, n - 1, loc, dest, mid)
        movelist.add_move(loc, dest)
        three_stool_solution(movelist, n - 1, mid, loc, dest)


def four_stool_solution(movelist: 'MoveSequence', n: int, location: int,
                        mid1: int, mid2: int, destination: int):
    """Appends to our movelist the moves required to move n cheeses given
    a location stool, two mid stools, and a destination stool.

    >>> move = MoveSequence([])
    >>> four_stool_solution(move, 3, 0, 1, 2, 3)
    >>> move
    MoveSequence([(0, 2), (0, 1), (0, 3), (1, 3), (2, 3)])
    >>> move2 = MoveSequence([])
    >>> four_stool_solution(move2, 2, 5, 6, 7, 8)
    >>> move2
    MoveSequence([(5, 7), (5, 8), (7, 8)])
    """
    if n == 1:
        movelist.add_move(location, destination)
    else:
        #Minimum tells us exactly which i to choose without having
        #brute force the moves.
        i = minimum(n)
        #n-i cheeses to mid 2
        four_stool_solution(movelist, n - i,
                            location, mid1, destination, mid2)
        #i cheeses using 3 stool to destination
        three_stool_solution(movelist, i,
                             location, mid1, destination)
        #n-i cheeses from before from mid2 to destination
        four_stool_solution(movelist, n - i, mid2,
                            mid1, location, destination)


def tour_of_four_stools(model: TOAHModel, delay_btw_moves: float=0.5,
                        console_animate: bool=False):
    """Move a tower of cheeses from the first stool in model to the fourth.

       model - a TOAHModel with a tower of cheese on the first stool
                and three other empty stools
       console_animate - whether to use ConsoleController to animate the tour
       delay_btw_moves - time delay between moves in seconds IF
                         console_animate == True
                         no effect if console_animate == False
    """

    #This first part is to make the right MoveSequence
    cheese_num = model.number_of_cheeses()
    moves = MoveSequence([])
    four_stool_solution(moves, cheese_num, 0, 1, 2, 3)

    #Then we apply it to our existing model, animating with delay if
    #requested.
    if console_animate:
        for move in moves._moves:
            print(model)
            model.move(move[0], move[1])
            time.sleep(delay_btw_moves)
        print(model)
    else:
        for move in moves._moves:
            model.move(move[0], move[1])

if __name__ == '__main__':
    NUM_CHEESES = 25
    DELAY_BETWEEN_MOVES = .1
    CONSOLE_ANIMATE = True

    # DO NOT MODIFY THE CODE BELOW.
    four_stools = TOAHModel(4)
    four_stools.fill_first_stool(number_of_cheeses=NUM_CHEESES)

    tour_of_four_stools(four_stools,
                        console_animate=CONSOLE_ANIMATE,
                        delay_btw_moves=DELAY_BETWEEN_MOVES)

    print(four_stools.number_of_moves())
