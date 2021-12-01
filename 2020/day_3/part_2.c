#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define BASE_10 10

#define MAP_HEIGHT 324
#define MAP_WIDTH 31

#define TREE '#'

void populate_from_input_file(char map[MAP_HEIGHT][MAP_WIDTH])
{
    // Used to juggle file strings into PasswordEntry structs
    int counter = 0;
    char buffer[MAP_WIDTH];

    FILE *file_pointer = fopen("input.txt", "r");

    // while (fgets(buffer, MAP_WIDTH, (FILE *)file_pointer))
    while (fgets(buffer, MAP_WIDTH + 100, file_pointer) != NULL)
    {
        for (int i = 0; i < MAP_WIDTH; i++)
        {
            map[counter][i] = buffer[i];
        }
        counter++;
    }
}

long get_solution()
{
    // Populate map from file
    char map[MAP_HEIGHT][MAP_WIDTH];
    populate_from_input_file(map);

    // List of all of the angles to check
    int angles[5][2] = {{1, 1}, {3, 1}, {5, 1}, {7, 1}, {1, 2}};

    long multiplication_of_trees = 1; // 1 so we can just multiply as we go

    for (int i = 0; i < 5; i++)
    {
        char current_space;
        int col = 0;
        long num_trees = 0;

        int dx = angles[i][0];
        int dy = angles[i][1];

        // printf("Running slope {%d, %d}...\n", dx, dy);

        for (int row = 0; row < MAP_HEIGHT; row = row + dy)
        {
            current_space = map[row][col];
            if (current_space == TREE)
                num_trees++;

            // Move to the right, we'll go down with the loop
            col = (col + dx) % MAP_WIDTH;
        }

        // printf("Num trees: %d\n", num_trees);

        multiplication_of_trees *= num_trees;
    }

    return multiplication_of_trees;
}

int main()
{
    time_t start_time = time(NULL);

    long solution = get_solution();
    solution ? printf("Solution is: %ld\n", solution) : printf("No solution found.\n");

    printf("Time taken: %lds\n", time(NULL) - start_time);

    return 0;
}
