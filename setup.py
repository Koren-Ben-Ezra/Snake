import random
from enum import Enum

FPS = 10
PLAYER_COLORS = ("purple", "pink", "orange")  # pygame.Color
BORDER_COLOR = "blue"  # pygame.Color
ISLAND_COLOR = "cyan"  # pygame.Color
APPLE_COLORS = ("green", "red", "yellow")  # pygame.Color
NUMBER_OF_ISLANDS_RANGE = (2, 5)
ISLAND_AREA_RANGE = (5, 30)

# padding for player's starting point
SNAKE_SPAWN_PADDING = 15
APPLE_SPAWN_PADDING = 0
ISLAND_SPAWN_PADDING = 5
SQUARE = 20
MARGIN = 1
WIDTH, HEIGHT = 1280, 720  # dividable by SQUARE
snake_speed = FPS
part_map = []  # excluding PT.SNAKE parts
part_map_xy = []
available_squares = []


class Direction(Enum):
    UP = 0
    UP_RIGHT = 1
    RIGHT = 2
    RIGHT_DOWN = 3
    DOWN = 4
    DOWN_LEFT = 5
    LEFT = 6
    LEFT_UP = 7


class PT(Enum):
    # Part Type
    BLANK = 0
    SNAKE = 1
    BORDER = 2
    APPLE = 3
    ISLAND = 4


class Part:
    def __init__(self, x, y, part_type: PT):
        self.x = x
        self.y = y
        self.part_type = part_type
        self.color = None
        self.Next = None
        self.Prev = None

    def check_overlap(self, other: 'Part') -> bool:
        """
            Returns True iff self and other overlap on the same square.
        """
        if other is None:
            raise TypeError()

        if self.x == other.x and self.y == other.y:
            return True
        return False

    @staticmethod
    def connect_parts(P_prev: 'Part', P_next: 'Part'):
        P_prev.Next = P_next
        P_next.Prev = P_prev


class Snake:
    def __init__(self):
        x, y = random.choice(available_squares)
        self.head = Part(x, y, PT.SNAKE)
        self.tail = self.head

        possible_directions = (Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT)
        self.Direction = random.choice(possible_directions)
        self.score = 1
        self.color = random.choice(list(PLAYER_COLORS))

    def move_in_direction(self, snake_ate: bool):
        if self.Direction == Direction.UP:
            x, y = self.head.x, self.head.y-1
        elif self.Direction == Direction.UP_RIGHT:
            x, y = self.head.x+1, self.head.y-1
        elif self.Direction == Direction.RIGHT:
            x, y = self.head.x+1, self.head.y
        elif self.Direction == Direction.RIGHT_DOWN:
            x, y = self.head.x+1, self.head.y+1
        elif self.Direction == Direction.DOWN:
            x, y = self.head.x, self.head.y+1
        elif self.Direction == Direction.DOWN_LEFT:
            x, y = self.head.x-1, self.head.y+1
        elif self.Direction == Direction.LEFT:
            x, y = self.head.x-1, self.head.y
        elif self.Direction == Direction.LEFT_UP:
            x, y = self.head.x-1, self.head.y-1
        else:
            raise ValueError()

        new_head = Part(x, y, PT.SNAKE)
        Part.connect_parts(new_head, self.head)
        self.head = new_head

        if not snake_ate:
            new_tail = self.tail.Prev
            new_tail.Next = None
            del self.tail
            self.tail = new_tail

        # diagonal speed control
        if self.Direction.value % 2 == 1:
            # Direction is diagonal
            global snake_speed
            snake_speed = FPS / (2 ** 0.5)
        else:
            snake_speed = FPS


def generate_part_map():
    # generate borders
    part_map.extend([Part(i, 0, PT.BORDER) for i in range(0, WIDTH//SQUARE+1)])
    part_map.extend([Part(i, HEIGHT//SQUARE-1, PT.BORDER) for i in range(0, WIDTH//SQUARE+1)])
    part_map.extend([Part(0, j, PT.BORDER) for j in range(1, HEIGHT//SQUARE-1)])
    part_map.extend([Part(WIDTH//SQUARE-1, j, PT.BORDER) for j in range(1, HEIGHT//SQUARE-1)])

    # generate islands
    number_of_islands = random.randint(NUMBER_OF_ISLANDS_RANGE[0], NUMBER_OF_ISLANDS_RANGE[1] + 1)
    for i in range(number_of_islands):
        generate_island()

    global available_squares, part_map_xy
    part_map_xy = [(part.x, part.y) for part in part_map]
    available_squares = [(i, j) for i in range(1, WIDTH // SQUARE-1) for j in range(1, HEIGHT // SQUARE-1) if (i, j) not in part_map_xy]


def generate_island():
    size = random.randint(ISLAND_AREA_RANGE[0], ISLAND_AREA_RANGE[1] + 1)

    x, y = generate_random_square(ISLAND_SPAWN_PADDING)
    part_map.append(Part(x, y, PT.ISLAND))
    size -= 1
    while size > 0:
        (x, y), squares_added = expand_island(x, y)
        size -= squares_added


def expand_island(root_x: int, root_y: int) -> tuple[tuple[int, int], int]:

    squares_added = []
    if (root_x, root_y+1) not in part_map_xy:
        squares_added.append((root_x, root_y+1))
    if (root_x, root_y-1) not in part_map_xy:
        squares_added.append((root_x, root_y-1))
    if (root_x+1, root_y) not in part_map_xy:
        squares_added.append((root_x+1, root_y))
    if (root_x-1, root_y) not in part_map_xy:
        squares_added.append((root_x-1, root_y))

    for (x, y) in squares_added:
        part_map.append(Part(x, y, PT.ISLAND))

    return random.choice(squares_added), len(squares_added)


def generate_random_square(padding: int) -> tuple[int, int]:
    # Excluding borders
    rand_x = random.randint(1 + padding, WIDTH // SQUARE - 1 - padding)
    rand_y = random.randint(1 + padding, HEIGHT // SQUARE - 1 - padding)
    return rand_x, rand_y
