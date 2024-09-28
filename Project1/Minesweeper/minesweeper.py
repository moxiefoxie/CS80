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
        This only gets returned when we know all of the cells that are known to be mines
        If the number of cells in the sentence equals the number of mines, then they are all mines
        so we will return the set. If the number doesn't equal, then we return an empty set because
        nothing can be inferred.
        """
        if len(self.cells) == self.count:
            return self.cells.copy()
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        If the number of mines in the set is 0, then the set is all safe.
        """
        if self.count == 0:
            return self.cells.copy()
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # Check to see if cell is one of the cells in the sentence
        if cell in self.cells:
        # If yes, remove cell from sentence and decrease number of mines
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # Check to see if cell is one of the cells in the sentence
        if cell in self.cells:
            #If yes, remove cell from sentence but leave mine count
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
        # Mark the cell as a move
        self.moves_made.add(cell)

        # Mark the cell safe
        self.safes.add(cell)

        # add a new sentence to the AI's knowledge base based on the value of `cell` and `count`
        # this loops through and creates a set of all neighboring cells that we know not to be safe, mines,
        # or already made (redundant since it would be marked safe or mine but still there)
        neighbors = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell or not (0 <= i < self.height and 0 <= j < self.width):
                    continue
                if (i, j) not in self.safes and (i, j) not in self.mines and (i, j) not in self.moves_made:
                    neighbors.add((i, j))

        # add a sentence for each neighbor
        if neighbors:
            new_sentence = Sentence(neighbors, count)
            self.knowledge.append(new_sentence)

        # mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base
        # add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge
        self.update_knowledge()

    def update_knowledge(self):
        """Handles steps 4 and 5 from add_knowledge"""
        # Track changes. It loops through all sentences until no more changes can be made
        changed = True
        while changed:
            changed = False
            for sentence in self.knowledge.copy():
                known_mines = sentence.known_mines()
                known_safes = sentence.known_safes()

                # check all known mines to mark knowledge
                if known_mines:
                    for mine in known_mines:
                        self.mark_mine(mine)
                    changed = True

                # check all known safes to mark knowledge
                if known_safes:
                    for safe in known_safes:
                        self.mark_safe(safe)
                    changed = True

            # Remove empty sentences and infer new ones
            self.knowledge = [s for s in self.knowledge if s.cells]
            for sentence1 in self.knowledge.copy():
                for sentence2 in self.knowledge.copy():
                    #makes new inferences by checking for subsets of existing sentences
                    if sentence1 != sentence2 and sentence2.cells.issubset(sentence1.cells):
                        inferred_sentence = Sentence(sentence1.cells - sentence2.cells,
                                                     sentence1.count - sentence2.count)
                        if inferred_sentence not in self.knowledge:
                            self.knowledge.append(inferred_sentence)
                            changed = True

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        all_cells = set(itertools.product(range(self.height), range(self.width)))
        available_moves = all_cells - self.moves_made - self.mines
        if available_moves:
            return random.choice(list(available_moves))
        return None
