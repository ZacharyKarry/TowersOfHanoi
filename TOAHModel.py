# Copyright 2013, 2014 Gary Baumgartner, Danny Heap, Dustin Wehr
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
TOAHModel:  Model a game of Towers of Anne Hoy
Cheese:   Model a cheese with a given (relative) size
IllegalMoveError: Type of exceptions thrown when an illegal move is attempted
MoveSequence: Record of a sequence of (not necessarily legal) moves. You will
need to return MoveSequence object after solving an instance of the 4-stool
Towers of Anne Hoy game, and we will use that to check the correctness of your
algorithm.
"""


class TOAHModel:
    """Model a game of Towers Of Anne Hoy.

    Model stools holding stacks of cheese, enforcing the constraint
    that a larger cheese may not be placed on a smaller one.

    fill_first_stool - put an existing model in the standard starting config
    move - move cheese from one stool to another
    add - add a cheese to a stool
    cheese_location - index of the stool that the given cheese is on
    number_of_cheeses - number of cheeses in this game
    number_of_moves - number of moves so far
    number_of_stools - number of stools in this game
    get_move_seq - MoveSequence object that records the moves used so far

    """

    def __init__(self: 'TOAHModel', number_of_stools: int):
        """
        Initialize a model of the Towers of Anne Hoi game.

        PRECONDITION: number_of_stools > 0
        """
        self._stoolnum = number_of_stools
        self._move_seq = MoveSequence([])
        #I chose to use a dictionary of lists, as this allows us to
        #easily move the cheese to a known stool while retaining
        #the order of the cheeses. It is also prettier to deal with
        #then a list of lists.
        self._model = {}
        for num in range(number_of_stools):
            self._model[num] = []

    def fill_first_stool(self: 'TOAHModel', number_of_cheeses: int):
        """
        Put number_of_cheeses cheeses on the first (i.e. 0-th) stool, in order
        of size, with a cheese of size == number_of_cheeses on bottom and
        a cheese of size == 1 on top.

        Precondition: number_of_cheeses > 0

        >>> m1 = TOAHModel(1)
        >>> m1.fill_first_stool(3)
        >>> m1._model
        {0: [Cheese(3), Cheese(2), Cheese(1)]}
        """
        self._filled_stool = True
        #Iterates backwards to build from bottom to top.
        for cheese_size in range(number_of_cheeses, 0, -1):
            new_cheese = Cheese(cheese_size)
            self._model[0].append(new_cheese)

    def add(self: "TOAHModel", location: int, cheese: "Cheese/CheeseView"):
        """ Puts a Cheese object at a specific location.

        >>> m = TOAHModel(1)
        >>> c = Cheese(3)
        >>> m.add(0, c)
        >>> m._model
        {0: [Cheese(3)]}

        """
        #This first part throws an exception if you try to set up cheeses
        #in a way that violates the game, i.e. you try to add a larger cheese
        #on a smaller cheese, or two cheeses of the same size.
        if len(self._model[location]) > 0:
            if self._model[location][-1].size <= cheese.size:
                raise SillyUserError
        self._model[location].append(cheese)

    def move(self: 'TOAHModel', location: int, destination: int):
        """ Moves the top cheese from location to destination as
        long as the top of destination isn't a cheese of smaller
        size than the cheese from location.

        >>> m = TOAHModel(2)
        >>> m.fill_first_stool(3)
        >>> m.move(0, 1)
        >>> m._model
        {0: [Cheese(3), Cheese(2)], 1: [Cheese(1)]}
        >>> m.move(1, 0)
        >>> m._model
        {0: [Cheese(3), Cheese(2), Cheese(1)], 1: []}
        """
        #Makes sure that there is a cheese on the stool to move
        if len(self._model[location]) > 0:
            loc_size = self._model[location][-1].size
        else:
            raise IllegalMoveError

        #Keeps track of the size of cheese on top of the destination stool.
        #If there is nothing there, defaults to loc_size + 1 so a move is
        #always possible
        if len(self._model[destination]) > 0:
            dest_size = self._model[destination][-1].size
        else:
            dest_size = loc_size + 1

        if loc_size < dest_size:
            cheese = self._model[location].pop()
            self._model[destination].append(cheese)
            #updates our move sequence
            self._move_seq.add_move(location, destination)
        else:
            raise IllegalMoveError

    def cheese_location(self: "TOAHModel", cheese: "Cheese/CheeseView") -> int:
        """Returns index of stool where cheese object is located.

        >>> m = TOAHModel(1)
        >>> m.fill_first_stool(1)
        >>> m.cheese_location(m._model[0][0])
        0
        """
        for stool in self._model:
            if cheese in self._model[stool]:
                return stool
        #In case someone decides to call it when there is no matching cheese
        raise SillyUserError

    def top_cheese(self: "TOAHModel", stool_index: int) -> 'Cheese/CheeseView':
        """Returns the top cheese at the stool at stool_index.

        >>> m = TOAHModel(1)
        >>> m.fill_first_stool(1)
        >>> m.top_cheese(0)
        Cheese(1)
        """
        if len(self._model[stool_index]) > 0:
            return self._model[stool_index][-1]
        else:
            return None

    def number_of_cheeses(self: 'TOAHModel') -> int:
        """Returns the number of cheeses in the current game.

        m = TOAHModel(2)
        m.fill_first_stool(7)
        m.number_of_cheeses()
        7
        """
        #pretty simple, just counts every stool and adds it up
        return sum([len(self._model[stool]) for stool in self._model])

    def number_of_moves(self: 'TOAHModel') -> int:
        """Returns the number of moves made in the current game.

        >>> m = TOAHModel(2)
        >>> m.fill_first_stool(1)
        >>> m.move(0, 1)
        >>> m.move(1, 0)
        >>> m.move(0, 1)
        >>> m.move(1, 0)
        >>> m.number_of_moves()
        4
        """
        return self.get_move_seq().length()

    def number_of_stools(self: 'TOAHModel') -> int:
        """Returns the number of stools in the current game.

        >>> m = TOAHModel(4)
        >>> m.number_of_stools()
        4
        """
        return self._stoolnum

    def _cheese_at(self: 'TOAHModel', stool_index,
                   stool_height: int) -> 'Cheese':
        """
        If there are at least stool_height+1 cheeses
        on stool stool_index then return the (stool_height)-th one.
        Otherwise return None.

        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(5)
        >>> M._cheese_at(0,3).size
        2
        >>> M._cheese_at(0,0).size
        5
        """
        #Lucky for us, len() can get us the number of cheeses on
        #a particular stool easily. So we just need to make sure
        #that number is strictly greater than stool_height
        #(since stool_height begins at 0)
        if len(self._model[stool_index]) > stool_height:
            return self._model[stool_index][stool_height]
        else:
            return None

    def get_move_seq(self: 'TOAHModel') -> 'MoveSequence':
        """
        Returns the MoveSequence that represents all moves made
        in the current model.

        >>> m = TOAHModel(2)
        >>> m.fill_first_stool(1)
        >>> m.move(0, 1)
        >>> m.move(1, 0)
        >>> m.move(0, 1)
        >>> m.move(1, 0)
        >>> m.get_move_seq()
        MoveSequence([(0, 1), (1, 0), (0, 1), (1, 0)])
        """
        return self._move_seq

    def __eq__(self: 'TOAHModel', other: 'TOAHModel') -> bool:
        """
        We're saying two TOAHModels are equivalent if their current
        configurations of cheeses on stools look the same.
        More precisely, for all h,s, the h-th cheese on the s-th
        stool of self should be equivalent the h-th cheese on the s-th
        stool of other

        >>> m1 = TOAHModel(4)
        >>> m1.fill_first_stool(7)
        >>> m1.move(0,1)
        >>> m1.move(0,2)
        >>> m1.move(1,2)
        >>> m2 = TOAHModel(4)
        >>> m2.fill_first_stool(7)
        >>> m2.move(0,3)
        >>> m2.move(0,2)
        >>> m2.move(3,2)
        >>> m1 == m2
        True
        """
        #First tests the number of cheeses and stools match, since
        #that is the easiest way to tell if they outright don't match.
        if (self.number_of_cheeses() != other.number_of_cheeses() or
                self._stoolnum != other._stoolnum):
            return False

        #This block then checks if the stools have the same configuration
        #of cheeses.
        for stool in self._model:
            if stool in other._model:
                if self._model[stool] != other._model[stool]:
                    return False
        return True

    def equivalent_models(self: 'TOAHModel', other: 'TOAHModel') -> bool:
        """
        Determines if two models have the same configuration of cheeses
        on stools IGNORING order.

        >>> m1 = TOAHModel(4)
        >>> m1.fill_first_stool(7)
        >>> m1.move(0,1)
        >>> m1.move(0,2)
        >>> m1.move(1,2)
        >>> m2 = TOAHModel(4)
        >>> m2.fill_first_stool(7)
        >>> m2.move(0,2)
        >>> m2.move(0,3)
        >>> m2.move(2,3)
        >>> m1 == m2
        False
        """
        #First tests the number of cheeses, since that is the easiest way
        #to tell if they outright don't match
        if self.number_of_cheeses() != other.number_of_cheeses():
            return False

        #This block determines if all stacks are the same, and is guaranteed
        #to be right given that they have the same number of cheeses.
        values_self = self._model.values()
        values_other = other._model.values()

        for value in values_self:
            if value not in values_other:
                return False

        return True

    def __str__(self: 'TOAHModel') -> str:
        """
        Depicts only the current state of the stools and cheese.
        """
        stool_str = "=" * (2 * (self.number_of_cheeses()) + 1)
        stool_spacing = "  "
        stools_str = (stool_str + stool_spacing) * self.number_of_stools()

        def cheese_str(size: int):
            if size == 0:
                return " " * len(stool_str)
            cheese_part = "-" + "--" * (size - 1)
            space_filler = " " * int((len(stool_str) - len(cheese_part)) / 2)
            return space_filler + cheese_part + space_filler

        lines = ""
        for height in range(self.number_of_cheeses() - 1, -1, -1):
            line = ""
            for stool in range(self.number_of_stools()):
                c = self._cheese_at(stool, height)
                if isinstance(c, Cheese):
                    s = cheese_str(int(c.size))
                else:
                    s = cheese_str(0)
                line += s + stool_spacing
            lines += line + "\n"
        lines += stools_str

        return lines

    def same_strategy(self: 'TOAHModel', other: 'TOAHModel') -> bool:
        """
        **This is a BONUS problem.**
        Insert this method in TOAHModel if you intend to attempt it.

        same_strategy is an equivalence relation that compares the entire move
        sequences of the two models, but ignores superficial differences in
        them. self and other are equivalent as strategies iff all of the
        following are true:
        (1) they were initialized in the standard way by using
            TOAHModel.fill_first_stool.
        (2) they have the same number of moves, stools, and cheeses
        (3) their move sequences are both legal
        (4) in the i-th cheese configurations C1 and C2 of self and
            other, respectively, it's possible to permute the order of C2's
            stools in such a way that they look the same as C1's stools (i.e.
            two TOAHModels with current configurations C1 and C2 would be
            judged equivalent according to TOAHModel.__eq__)
        >>> m1 = TOAHModel(4)
        >>> m1.fill_first_stool(7)
        >>> m1.move(0,1)
        >>> m1.move(0,2)
        >>> m1.move(1,2)
        >>> m2 = TOAHModel(4)
        >>> m2.fill_first_stool(7)
        >>> m2.move(0,3)
        >>> m2.move(0,2)
        >>> m2.move(3,2)
        >>> m1.same_strategy(m2)
        True
        >>> m1.move(0,1)
        >>> m2.move(0,3)
        >>> m1.same_strategy(m2)
        True
        """
        #checks first condition
        if self._filled_stool != other._filled_stool:
            print("failed1")
            return False

        #checks second condition
        elif (self.number_of_stools() != other.number_of_stools() or
              self.number_of_cheeses() != other.number_of_cheeses() or
              self.get_move_seq().length() != other.get_move_seq().length()):
            return False

        #checks third condition and fourth condition simultaneously
        test1 = TOAHModel(self.number_of_stools())
        test2 = TOAHModel(other.number_of_stools())
        test1.fill_first_stool(self.number_of_cheeses())
        test2.fill_first_stool(other.number_of_cheeses())
        move_seq1 = self.get_move_seq()
        move_seq2 = other.get_move_seq()

        for move in range(move_seq1.length()):
            try:
                loc1 = move_seq1.get_move(move)[0]
                dest1 = move_seq1.get_move(move)[1]
                loc2 = move_seq2.get_move(move)[0]
                dest2 = move_seq2.get_move(move)[1]

                test1.move(loc1, dest1)
                test2.move(loc2, dest2)
            except IllegalMoveError:
                #This is the test of condition three
                return False
            if not test1.equivalent_models(test2):
                #This is the test of condition four
                return False

        return True


class Cheese:
    def __init__(self: 'Cheese', size: int):
        """
        Initialize a Cheese to diameter size.

        >>> c = Cheese(3)
        >>> isinstance(c, Cheese)
        True
        >>> c.size
        3
        """
        self.size = size

    def __repr__(self: 'Cheese') -> str:
        """
        Representation of this Cheese
        """
        return "Cheese(" + str(self.size) + ")"

    def __eq__(self: 'Cheese', other: 'Cheese') -> bool:
        """Is self equivalent to other? We say they are if they're the same
        size."""
        return isinstance(other, Cheese) and self.size == other.size


class IllegalMoveError(Exception):
    pass


class SillyUserError(Exception):
    pass


class MoveSequence(object):
    def __init__(self: 'MoveSequence', moves: list):
        # moves - a list of integer pairs, e.g. [(0,1),(0,2),(1,2)]
        self._moves = moves

    def get_move(self: 'MoveSequence', i: int):
        # Exception if not (0 <= i < self.length)
        return self._moves[i]

    def add_move(self: 'MoveSequence', src_stool: int, dest_stool: int):
        self._moves.append((src_stool, dest_stool))

    def length(self: 'MoveSequence') -> int:
        return len(self._moves)

    def generate_TOAHModel(self: 'MoveSequence', number_of_stools: int,
                           number_of_cheeses: int) -> 'TOAHModel':
        """
        An alternate constructor for a TOAHModel. Takes the two parameters for
        the game (number_of_cheeses, number_of_stools), initializes the game
        in the standard way with TOAHModel.fill_first_stool(number_of_cheeses),
        and then applies each of the moves in move_seq.
        """
        model = TOAHModel(number_of_stools)
        model.fill_first_stool(number_of_cheeses)
        for move in self._moves:
            model.move(move[0], move[1])
        return model

    def __repr__(self: 'MoveSequence') -> str:
        return "MoveSequence(" + repr(self._moves) + ")"


if __name__ == '__main__':
    import doctest
    doctest.testmod()
