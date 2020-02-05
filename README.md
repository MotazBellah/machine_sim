# Machine Moving Simulation

Consider an infinite grid of white and black squares. The grid is initially all white and there is a machine in one cell facing right. It will move based on the following rules:

- If the machine is in a white square, turn 90° clockwise and move forward 1 unit;
- If the machine is in a black square, turn 90° counter-clockwise and move forward 1 unit;
- At every move flip the color of the base square.

Implement an application that will receive HTTP PUT requests with a number of steps the simulation should run, always starting from the same conditions, and output the resulting grid to a file.

## Code style

- This project is written in python 3.
- Use Flask framework.

## Implementation

- Create a function called `draw_grid` that responsible for draw the grid and print it out in text file and locate the locations where the squares should be black

- `draw_grid` function takes two Parameters `map` and `locations`, `map` is list of tuple in (x, y) represent the size of grid, and `locations` is list of tuple (x, y) represent the location on map where the machine step in to
