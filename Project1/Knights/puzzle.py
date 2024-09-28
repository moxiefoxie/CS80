from Project1.Knights.logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave." = And(AKnight, AKnave)
knowledge0 = And(
    # The person must be either a knight OR a knave
    Or(AKnight, AKnave),
    # The person cannot be both a knight AND a knave
    Not(And(AKnight, AKnave)),
    # If the person is a knight, then the statement MUST be true
    Implication(AKnight, And(AKnight, AKnave)),
    # If the person is a knave, then the statement MUST be false
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves." = And(AKnave, BKnave)
# B says nothing.
knowledge1 = And(
    # Person A  must be either a knight OR a knave
    Or(AKnight, AKnave),
    # Person A cannot be both a knight AND a knave
    Not(And(AKnight, AKnave)),
    # Person B must be either a knight OR a knave
    Or(BKnight, BKnave),
    # Person B cannot be both a knight AND a knave
    Not(And(BKnight, BKnave)),
    # If A is a knight, then A and B are both knaves
    Implication(AKnight, And(AKnave, BKnave)),
    # If A in a knave, then B is a knight
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind." = Or(And(AKnave, BKnave), And(AKnight, BKnight))
# B says "We are of different kinds." =
knowledge2 = And(
    # A is either a Knight or a Knave
    Or(AKnight, AKnave),
    # Person A cannot be both a knight AND a knave
    Not(And(AKnight, AKnave)),
    # B is either a Knight or a Knave
    Or(BKnight, BKnave),
    # Person B cannot be both a knight AND a knave
    Not(And(BKnight, BKnave)),

    # If A is a Knight, then B is a Knight
    Implication(AKnight, BKnight),
    # If A is a Knave, then B is a Knave
    Implication(AKnave, BKnight),
    # If B is a Knight, then A is not a knight
    Implication(BKnight, AKnave),
    # If B is a Knave, then A and B are the same kind and not knaves (must be knights)
    Implication(BKnave, AKnave)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which. (They can't say I'm a knave)
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # A is either a Knight or a Knave
    Or(AKnight, AKnave),
    # Person A cannot be both a knight AND a knave
    Not(And(AKnight, AKnave)),
    # B is either a Knight or a Knave
    Or(BKnight, BKnave),
    # Person B cannot be both a knight AND a knave
    Not(And(BKnight, BKnave)),
    # Cis either a Knight or a Knave
    Or(CKnight, CKnave),
    # Person C cannot be both a knight AND a knave
    Not(And(CKnight, CKnave)),

    Implication(AKnight, AKnight),
    Implication(AKnave, Not(AKnight)),

    Implication(BKnight, AKnave),
    Implication(BKnave, Not(AKnave)),

    Implication(BKnight, CKnight),
    Implication(BKnave, Not(CKnave)),

    Implication(CKnight, AKnight)

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
