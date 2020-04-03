import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def nearby_cells(self, cell):
        """
        Returns all cells which are one row and column of a given cell
        """
        nearby_cells_ = set()
        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        nearby_cells_.add((i,j))

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        known_mines_ = set()
        for cell in self.cells:
            if len(self.cells) == self.count:
                known_mines_ = set(self.cells)
        return known_mines_


    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        known_safes_ = set()
        for cell in self.cells:
            if self.count == 0:
                known_safes_ = set(self.cells)
        return known_safes_

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count = self.count - 1


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def nearby_cells(self, cell):
        """
        Returns all cells which are one row and column of a given cell
        """
        nearby_cells_ = []
        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Add cell if in bounds
                if 0 <= i < self.height and 0 <= j < self.width:
                    nearby_cells_.append((i,j))

        return nearby_cells_

    def check_known_safe(self, cell):
        safe = False
        for sentence in self.knowledge:
            if cell in sentence.known_safes():
                safe = True
        return safe

    def check_known_mine(self, cell):
        mine = False
        for sentence in self.knowledge:
            if cell in sentence.known_mines():
                mine = True
        return mine

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        i, j = cell
        # 1
        self.moves_made.add(cell)

        # 2
        self.mark_safe(cell)

        # 3
        nearby_cells_ = self.nearby_cells(cell)
        self.knowledge.append(Sentence(nearby_cells_, count))

        # 4
        for cell in nearby_cells_:
            if self.check_known_mine(cell):
                self.mark_mine(cell)
            if self.check_known_safe(cell):
                self.mark_safe(cell)

        # 5

        self.knowledge = [
        x for x in self.knowledge if ((not(len(x.cells) == 0)) and (not(x.count == 0)) and (not(len(x.cells)==x.count)))
        ] # Trim down extra knowledge


        new_sentences = []
        for sentence1 in self.knowledge:
            set1, count1 = sentence1.cells, sentence1.count
            for sentence2 in self.knowledge:
                set2, count2 = sentence2.cells, sentence2.count
                if (set1.issubset(set2) and set1 != set2):
                    new_sentences.append(Sentence(set2 - set1, count2 - count1))
        for sentence in new_sentences:
            if len(sentence.cells) > 0:
                self.knowledge.append(sentence)

        # TODO: make part 5 more effecient


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        cell = None
        for safe in self.safes:
            if safe not in self.moves_made:
                cell = safe
                break
        return cell

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        all_moves = set()
        for i in range(self.height):
            for j in range(self.width):
                all_moves.add((i,j))
        possible_moves = all_moves - self.mines
        possible_moves = possible_moves - self.moves_made
        possible_moves = list(possible_moves)
        return random.choice(possible_moves)
