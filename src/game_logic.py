from enum import Enum, auto
import uuid
from typing import List, Dict, Tuple, Union

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
        self.is_taken = False           # piece is on the board true/false
        self.is_focused = False         # has the piece been clicked (or is it being dragged)(mousedown) (to make the move)
        self.moves = []
        
    @classmethod
    def copy_from(cls, other):
        return cls(other.type, other.team, other.position)
    
    def __repr__(self) -> str:
        return f"{self.team.value}_{self.type.value} on square {self.position}, uiid: {self.id}"
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def change_position(self, newPosition: str):
        self.position = newPosition


INGAME_PIECES: List[Piece] = []



# TODO:main game logic
# TODO:piece movement
# TODO: refactor this

GRID = {}

def init_grid():
    for row in "12345678":
        GRID[row] = {}
        for col in "abcdefgh":
            GRID[row][col] = col + row

# ==== LOGIC ====

def init_pieces():
    for i in "7":
        for j in "abcdefgh":
            INGAME_PIECES.append(Piece(PieceType.PAWN, Team.BLACK if i == "7" else Team.WHITE, position=f"{j + i}"))
    
    for i in "81":
        INGAME_PIECES.append(Piece(PieceType.ROOK, Team.BLACK if i == "8" else Team.WHITE, position=f"{'a' + i}"))
        INGAME_PIECES.append(Piece(PieceType.KNIGHT, Team.BLACK if i == "8" else Team.WHITE, position=f"{'b' + i}"))
        INGAME_PIECES.append(Piece(PieceType.BISHOP, Team.BLACK if i == "8" else Team.WHITE, position=f"{'c' + i}"))
        INGAME_PIECES.append(Piece(PieceType.QUEEN, Team.BLACK if i == "8" else Team.WHITE, position=f"{'d' + i}"))
        INGAME_PIECES.append(Piece(PieceType.KING, Team.BLACK if i == "8" else Team.WHITE, position=f"{'e' + i}"))
        INGAME_PIECES.append(Piece(PieceType.BISHOP, Team.BLACK if i == "8" else Team.BLACK, position=f"{'f' + i}"))
        #INGAME_PIECES.append(Piece(PieceType.KNIGHT, Team.BLACK if i == "8" else Team.WHITE, position=f"{'g' + i}"))
        INGAME_PIECES.append(Piece(PieceType.ROOK, Team.BLACK if i == "8" else Team.WHITE, position=f"{'e' + '4'}"))

def init():
    init_grid() # TODO: prolly dont need this, consider deleting later
    init_pieces()

def find_move(piece: Piece):
    if piece.type == PieceType.PAWN:
        find_move_pawn(piece)
    elif piece.type == PieceType.ROOK:
        find_move_rook(piece)
    elif piece.type == PieceType.KNIGHT:
        find_move_knight(piece)
    elif piece.type == PieceType.BISHOP:
        find_move_bishop(piece)
    elif piece.type == PieceType.QUEEN:
        find_move_queen(piece)        
    elif piece.type == PieceType.KING:
        find_move_king(piece)

def find_move_pawn(pc: Piece):
    
    # if hasnt moved, +-2 allowed,
    # distinguish teams
    
    # TODO: this so fucked up in so many ways, refactor
    # TODO: check for en passant
    
    to_move = 1 if pc.team == Team.WHITE else -1
    pos_letter_ord = ord(pc.position[0])
    
    take1 = f"{chr(pos_letter_ord + 1)}{int(pc.position[1]) + to_move}"
    take2 = f"{chr(pos_letter_ord - 1)}{int(pc.position[1]) + to_move}"
    
    moves = [f"{pc.position[0]}{int(pc.position[1]) + to_move}"]   # cell to take
    
    if int(pc.position[1]) == 2 or int(pc.position[1]) == 7:
        moves.append(f"{pc.position[0]}{int(pc.position[1]) + to_move * 2}")
    
    if pawn_can_take(pc, take1) and pawn_can_take(pc,take2):
        moves.append(take1)
        moves.append(take2)
        
    print(moves)
    
    pc.moves.clear()
    for m in moves:
        if check_move_availability(pc, m):
            pc.moves.append(m)

def pawn_can_take(pc: Piece, to_position: str):
    if not cell_is_empty(to_position):
        return cell_is_takeable(pc, to_position)
    return False

def find_move_rook(pc: Piece):
    moves = []
    
    moves = find_moves_hor_ver_new(pc)
    pc.moves.clear()
    for m in moves:
        #if check_move_availability(pc, m):
        pc.moves.append(m)
    


"""
    ================== MOVES ==================
    hor_ver moves
        need to calculate moves starting from 
        the piece that is being moved in order 
        to detect the first piece met.
        
        Is there a way to do that from 
        check_move_availability()? Considering 
        the patterns are not the same 
        (e.g. bishop and rook)
    diag moves
        The idea is pretty much the same
"""



# TODO: this is too bad omfg, FIX
def find_moves_hor_ver_new(pc: Piece) -> List[str]:
    moves = []
    
    pos_x_ord = ord(pc.position[0])
    pos_y = int(pc.position[1])

    left = pos_x_ord - 1
    right = pos_x_ord + 1
    
    top = pos_y + 1
    bottom = pos_y - 1
    
    flag_top = True
    flag_bottom = True
    flag_left = True
    flag_right = True
    
    # literally copy and paste 4 times 
    while flag_top:
        if top > 8 or not cell_is_empty(f"{chr(pos_x_ord)}{top}"):
            if cell_is_takeable(pc, f"{chr(pos_x_ord)}{top}"):
                moves.append(f"{chr(pos_x_ord)}{top + 1}")
                flag_top = False
                break
            else:
                flag_top = False
                break
        else:
            moves.append(f"{chr(pos_x_ord)}{top}")
        top += 1
    
    while flag_bottom:
        if bottom < 1 or not cell_is_empty(f"{chr(pos_x_ord)}{bottom}"):
            if cell_is_takeable(pc, f"{chr(pos_x_ord)}{bottom}"):
                moves.append(f"{chr(pos_x_ord)}{bottom}")
                flag_bottom = False
                break
            else:
                flag_bottom = False
                break
        else:
            moves.append(f"{chr(pos_x_ord)}{bottom}")
        bottom -= 1
    
    while flag_left:
        if left < ord("a") or not cell_is_empty(f"{chr(left)}{pos_y}"):
            if cell_is_takeable(pc, f"{chr(left)}{pos_y}"):
                moves.append(f"{chr(left)}{pos_y}")
                flag_left = False
                break
            else:
                flag_left = False
                break
        else:
            moves.append(f"{chr(left)}{pos_y}")
        left -= 1
        
    while flag_right:
        if right > ord("h") or not cell_is_empty(f"{chr(right)}{pos_y}"):
            if cell_is_takeable(pc, f"{chr(right)}{pos_y}"):
                moves.append(f"{chr(right)}{pos_y}")
                flag_right = False
                break
            else:
                flag_right = False
                break
        else:
            moves.append(f"{chr(right)}{pos_y}")
        right += 1
    return moves



def find_moves_hor_ver(pc: Piece) -> List[str]:
    moves = []
    
    pos_x_ord = ord(pc.position[0])
    pos_y = int(pc.position[1])
    
    left = pos_x_ord - 1
    right = pos_x_ord + 1
    
    top = pos_y + 1
    bottom = pos_y - 1
    
    flag_top = True
    flag_bottom = True
    flag_left = True
    flag_right = True
    
    while flag_top or flag_bottom or flag_left or flag_right:
        
        
        # TODO: I feel like there is a bug in this ifs, keep in mind 
        if left < ord("a") :
            flag_left = False
        if right > ord("h"):
            flag_right = False
        if top > 8 or not cell_is_empty(f"{chr(pos_x_ord)}{top}"):
            
            flag_top = False
        if bottom < 1:
            flag_bottom = False
        
        
        if flag_left:
            moves.append(f"{chr(left)}{pos_y}")
        if flag_right:
            moves.append(f"{chr(right)}{pos_y}")
        if flag_top:
            moves.append(f"{chr(pos_x_ord)}{top}")
        if flag_bottom:
            moves.append(f"{chr(pos_x_ord)}{bottom}")
        
        left -= 1
        right += 1
        top += 1
        bottom -= 1
    return moves

def find_move_knight(pc: Piece):
    pass

def find_move_bishop(pc: Piece):
    pass

def find_move_queen(pc: Piece):
    pass

def find_move_king(pc: Piece):
    pass


def check_move_availability(pc: Piece, to_pos: str):
    if cell_exists(to_pos):
        if cell_is_empty(to_pos): # and no discoveries and so on, TODO: fix later
            return True
        elif not cell_is_empty(to_pos):
            return cell_is_takeable(pc, to_pos)
    return False

    #return cell_exists(position) and cell_is_takeable(position)

def met_obsticle(position: str):
    return not cell_is_empty(position)

def cell_exists(position: str):
    if ord(position[0]) < ord("a") or ord(position[0]) > ord("h") or \
        int(position[1]) < 1 or int(position[1]) > 8:
        return False
    return True

def cell_is_empty(position: str):
    if find_piece_by_position(position) == None:
        return True
    return False

def find_piece_by_position(position: str) -> Union[Piece, None]:
    for p in INGAME_PIECES:
        if p.position == position:
            return p
    return None

def cell_is_takeable(piece_taking: Piece, position_to_take: str):
    if cell_is_empty(position_to_take):
        print("Cant take empty")
        return False
    if piece_taking.team != Piece.copy_from(find_piece_by_position(position_to_take)).team:
        return True
    return False

def move_discovers_check():
    return False

def is_check():
    pass

def is_checkmate():
    pass

def check_enpassant():
    return False