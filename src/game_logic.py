from enum import Enum, auto
import uuid
from typing import List, Dict, Tuple

class PieceType(Enum):
    PAWN      = "p"
    ROOK      = "r"
    KNIGHT    = "n"
    BISHOP    = "b"
    QUEEN     = "q"
    KING      = "k"

class Team(Enum):
    BLACK = "b"
    WHITE = "w"
    

class Piece:
    def __init__(self, type: PieceType, team: Team, position: str) -> None:
        self.id = uuid.uuid4()
        self.type = type
        self.team = team
        self.position = position
        self.is_taken = False        # piece is on the board true/false
        self.is_focused = False        # has the piece been clicked (or is it beingh dragged)(mousedown) (to make the move)
    
    def __repr__(self) -> str:
        return f"{self.team.value}_{self.type.value} on square {self.position}, uiid: {self.id}"
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def change_position(self, newPosition: str):
        self.position = newPosition



GRID: dict = {}
GRID_N: list[list] = []

INGAME_PIECES: List[Piece] = []


# TODO: implement pieces
#       render them
#       mouse input
#       main game logic

# TODO: refactor this



# ==== LOGIC ====

def init_pieces():
    # append pawns
    for i in "72":
        for j in "abcdefgh":
            INGAME_PIECES.append(Piece(PieceType.PAWN, Team.BLACK if i == "7" else Team.WHITE, position=f"{j + i}"))
    
    for i in "81":
        INGAME_PIECES.append(Piece(PieceType.ROOK, Team.BLACK if i == "8" else Team.WHITE, position=f"{'a' + i}"))
        INGAME_PIECES.append(Piece(PieceType.KING, Team.BLACK if i == "8" else Team.WHITE, position=f"{'b' + i}"))
        INGAME_PIECES.append(Piece(PieceType.BISHOP, Team.BLACK if i == "8" else Team.WHITE, position=f"{'c' + i}"))
        INGAME_PIECES.append(Piece(PieceType.QUEEN, Team.BLACK if i == "8" else Team.WHITE, position=f"{'d' + i}"))
        INGAME_PIECES.append(Piece(PieceType.KING, Team.BLACK if i == "8" else Team.WHITE, position=f"{'e' + i}"))
        INGAME_PIECES.append(Piece(PieceType.BISHOP, Team.BLACK if i == "8" else Team.WHITE, position=f"{'f' + i}"))
        INGAME_PIECES.append(Piece(PieceType.KNIGHT, Team.BLACK if i == "8" else Team.WHITE, position=f"{'g' + i}"))
        INGAME_PIECES.append(Piece(PieceType.ROOK, Team.BLACK if i == "8" else Team.WHITE, position=f"{'h' + i}"))

# try to implement it with this grid, then maybe try default [1][1]
def init_grid():
    """Generates a dictionary of dictionaries like:
    
        grid = {
            '1': {'a': 'a1', 'b': 'b1', 'c': 'c1'},
            '2': {'a': 'a2', 'b': 'b2', 'c': 'c2'},
            '3': {'a': 'a3', 'b': 'b3', 'c': 'c3'},
            ...
        }
    """
    for row in "12345678":
        GRID[row] = {}
        for column in "abcdefgh":
            pos = row + column
            GRID[row][column] = pos




def get_grid_matrix() -> list[list]:
    return []


def init():
    init_grid()
    init_pieces()