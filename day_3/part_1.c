#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define BASE_10 10

#define MAP_HEIGHT 324
#define MAP_WIDTH 31

#define TREE '#'
#define EMPTY '.'

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

    char current_space;
    int col = 0;
    int num_trees = 0;

    for (int row = 0; row < MAP_HEIGHT; row++)
    {
        current_space = map[row][col];
        if (current_space == TREE)
        {
            // We've hit a tree
            num_trees++;
        }
        else if (current_space != EMPTY)
        {
            // We shouldn't encounter anything but trees or empty spaces
            printf("Current space not recognised: %c\n", current_space);
        }

        // Move to the right, we'll go down with the loop
        col = (col + 3) % MAP_WIDTH;
    }

    return num_trees;
}

int main()
{
    time_t start_time = time(NULL);

    long solution = get_solution();
    solution ? printf("Solution is: %ld\n", solution) : printf("No solution found.\n");

    printf("Time taken: %lds\n", time(NULL) - start_time);

    return 0;
}
