#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX_EXPENSE_LENGTH 10
#define NUM_EXPENSES 200

long *get_expenses_from_input_file()
{
    // Used to juggle file strings into long array
    int counter = 0;
    char buffer[MAX_EXPENSE_LENGTH];

    // Actual thing we want (static so I can return an array)
    static long expenses[NUM_EXPENSES];

    FILE *file_pointer = fopen("input.txt", "r");

    while (fgets(buffer, MAX_EXPENSE_LENGTH, (FILE *)file_pointer))
    {
        expenses[counter++] = strtol(buffer, NULL, 10); // Base 10 conversion
    }

    return expenses;
}

long get_solution()
{
    long *expenses = get_expenses_from_input_file();
    long expense_1, expense_2;

    for (int i = 0; i < NUM_EXPENSES; i++)
    {
        expense_1 = *(expenses + i);
        for (int j = 0; j < NUM_EXPENSES - i; j++)
        {
            expense_2 = *(expenses + i + j);
            if (expense_1 + expense_2 == 2020)
            {
                return expense_1 * expense_2;
            }
        }
    }

    return 0;
}

int main()
{
    time_t start_time = time(NULL);

    long solution = get_solution();
    solution ? printf("Solution is: %ld\n", solution) : printf("No solution found.\n");

    printf("Time taken: %lds\n", time(NULL) - start_time);

    return 0;
}
