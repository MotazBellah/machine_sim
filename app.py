from flask import Flask, render_template, redirect, url_for, request, jsonify
from math import sqrt

app = Flask(__name__)

def draw_grid(map, locations):
    '''Locate the black squares in the white grid
       the black squares would have `**` instead of black color
       The function replace each draw which is the base of the square `__`
       with `**` according to the location in the map

       Parameters:
       map (list): List of tuple, each tuple represent the location of the squares
       in the grid (x, y)

       locations (list): List of tuple, each tuple represent the location where the machine
       moves on it

       Output:
       string: generate a file which contains a string representation of the grid that located the
       black squares donated by `**`
    '''
    # Create a grid text file
    file = open("grid.txt", 'w')
    # List represent the base of each square in the grid
    draw = ["__" for i in range(len(map))]
    grid = ""
    # loop through the locations where the machine steps on it
    # if the number of steps is an odd number, then the square should be black
    # get the location of the black squares `index` in the map
    # for each one replace the base `__` with `**` that represent the black squares
    for location in locations:
        if locations.count(location) % 2:
            index_player = map.index(location)
            draw[index_player] = '**'
    # Convert the updated draw list which contain `**` to be tuple
    # to unpack the values in the grid string
    draw_tuple = tuple(draw)
    # get the map_range by getting the square root of the map
    # grid_size = map_range * map_range
    map_range = int(sqrt(len(map)))
    # for each column, create a row
    for i in range(map_range):
        grid += "|{}" * map_range + "\n"

    x = grid.format(*draw_tuple)
    file.write(x)
    file.close()


@app.route('/', methods = ['GET', 'PUT'])
def move_machine():

    if request.method == 'PUT':
        # Ge the value of steps from url
        steps = int(request.args.get('steps'))
        if steps < 100:
            r = 10
        else:
            set_range = int(str(1) + '0' * (len(str(steps)) -2))
            r = (steps // set_range) + (steps % set_range)
        # Create a gird in form x, y
        MAP = [(i, j) for i in range(-r, r+1) for j in range(-r, r+1)]
        # Start from the half of the grid
        machine_location = MAP[len(MAP) // 2]
        # list to hold all steps the machine made
        check = []
        # unpack to x, y value
        x, y = machine_location
        # start with right direction
        direction = 'right'

        # loop through the number of steps
        # turn clockwise or counter-clockwise based on the number of (x,y) occurrence
        # If the occurrence is odd, then grid should be black, turn counter-clockwise
        # If the occurrence is even, then grid should be white, turn clockwise
        for i in range(steps):
            # If the occurrence is odd, then grid should be black, turn counter-clockwise
            # right => up => left => down
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
            # If the occurrence is even, then grid should be white, turn clockwise
            # right => down => left => up
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

        draw_grid(MAP, check)

        return jsonify({'result': 'success'})
    # Get request render the steps html
    return render_template('steps.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
