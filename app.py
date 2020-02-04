from flask import Flask
from math import sqrt

app = Flask(__name__)

def draw_grid(map, draw, locations):
    '''Locate the black squares in the white grid
       the black squares would have `**` instead of black color
       The function replace each draw which is the base of the square `__`
       with `**` according to the location in the map

       Parameters:
       map (list): List of tuple, each tuple represent the location of the squares
       in the grid (x, y)

       draw (list): List of `__` which represent the base of the squares and its length
       equal the length of row in the map (i.e map/2)

       locations (list): List of tuple, each tuple represent the location where the machine
       moves on it

       Output:
       string: generate a file which contains a string representation of the grid that located the
       black squares donated by `**`
    '''

    file = open("grid.txt", 'w')
    grid = ""
    for location in locations:
        if locations.count(location) % 2:
            index_player = map.index(location)
            draw[index_player] = '**'
    draw_tuple = tuple(draw)
    z = int(sqrt(len(map)))
    for i in range(z):
        grid += "|{}" *z +"\n"
    x = grid.format(*draw_tuple)
    print (x)
    file.write(x)
    file.close()


@app.route('/<int:steps>', methods = ['PUT'])
def move_machine(steps):

    r = 10 + (steps - 200) // 30
    e = 1 + (steps-200) // 30
    MAP = [(i, j) for i in range(-1*e, r) for j in range(-1*e, r)]
    draw = ["__" for i in range(len(MAP))]
    machine_location = MAP[len(MAP) // 2]
    # print(machine_location)
    check = []
    x, y = machine_location
    direction = 'right'

    for i in range(steps):

        # if (x,y) in check:
        if check.count((x,y)) % 2:
            check.append((x, y))
            if direction == 'left':
                x += 1
                direction = 'down'


            elif direction == 'up':
                y -= 1
                direction = 'left'


            elif direction == "right":
                x -= 1
                direction = 'up'


            elif direction == 'down':
                y += 1
                direction = 'right'

        else:
            check.append((x, y))
            if direction == 'right':
                x += 1
                direction = 'down'


            elif direction == 'down':
                y -= 1
                direction = 'left'


            elif direction == "left":
                x -= 1
                direction = 'up'


            elif direction == 'up':
                y += 1
                direction = 'right'
    # print(check)
    draw_grid(MAP, draw, check)

    return 'OK'


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
