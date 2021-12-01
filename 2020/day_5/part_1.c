#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define NUM_SEATS 850
#define SEAT_NAME_LENGTH 12

void populate_from_input_file(char seats[NUM_SEATS][SEAT_NAME_LENGTH])
{
    int counter = 0;
    char buffer[SEAT_NAME_LENGTH];

    FILE *file_pointer = fopen("input.txt", "r");

    while (fgets(buffer, SEAT_NAME_LENGTH, file_pointer) != NULL)
    {
        strcpy(seats[counter++], buffer);
    }
}

long get_solution()
{
    // Populate from file
    char seats[NUM_SEATS][SEAT_NAME_LENGTH];
    populate_from_input_file(seats);

    int row, col;
    int seat_id, highest_seat_id = 0;

    for (int i = 0; i < NUM_SEATS; i++)
    {
        row = 0;
        if (seats[i][0] == 'B')
            row += 64;
        if (seats[i][1] == 'B')
            row += 32;
        if (seats[i][2] == 'B')
            row += 16;
        if (seats[i][3] == 'B')
            row += 8;
        if (seats[i][4] == 'B')
            row += 4;
        if (seats[i][5] == 'B')
            row += 2;
        if (seats[i][6] == 'B')
            row += 1;

        col = 0;
        if (seats[i][7] == 'R')
            col += 4;
        if (seats[i][8] == 'R')
            col += 2;
        if (seats[i][9] == 'R')
            col += 1;

        seat_id = (row * 8) + col;

        if (seat_id > highest_seat_id)
            highest_seat_id = seat_id;

        // printf("%s (%d / %d) %d\n", seats[i], row, col, seat_id);
    }

    return highest_seat_id;
}

int main()
{
    time_t start_time = time(NULL);

    long solution = get_solution();
    solution ? printf("Solution is: %ld\n", solution) : printf("No solution found.\n");

    printf("Time taken: %lds\n", time(NULL) - start_time);

    return 0;
}
