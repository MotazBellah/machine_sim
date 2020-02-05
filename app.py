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

    file = open("grid.txt", 'w')
    draw = ["__" for i in range(len(map))]
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
    # print (x)
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
            r = (n // set_range) + (n % set_range)
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
    app.run(host='0.0.0.0', port=8000)
