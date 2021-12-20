import aocd, itertools as it

data = aocd.get_data(year=2021, day=20)

# Split up data
algo, image = data.replace(".", "0").replace("#", "1").split("\n\n")
image = image.split("\n")

# Create a dict representation of the grid
grid = {(y, x): image[y][x] for y in range(len(image)) for x in range(len(image))}

# Add border to the grid, so we can expand into it properly
for y, x in it.product(range(-102, len(image) + 103), repeat=2):  # A double for loop
    grid[(y, x)] = grid.get((y, x), "0")

# Get all the values around the given grid point
def area(g, y, x):
    return [g.get((y + dy, x + dx), "0") for dy in [-1, 0, 1] for dx in [-1, 0, 1]]


# Check if the point is part of the end grid we care about
in_grid = lambda xy: -51 < xy < len(image) + 50

# Count the number of hashes (or 1s in my representation) in the grid
count = lambda g: [g[(y, x)] for y, x in g if in_grid(y) and in_grid(x)].count("1")

# Expand the grid
for step in range(50):
    # This line:
    # - Gets the area around a point
    # - Turns that into an integer
    # - Gets the new value from the image enhancement algorithm
    # - Places the new value in the updated grid
    grid = {(y, x): algo[int("".join(area(grid, y, x)), 2)] for y, x in grid}
    # Show answers
    print(count(grid)) if step in [1, 49] else None
