#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define BASE_10 10

#define MAX_PASSPORTS 2000
#define MAX_PASSPORT_SIZE 1000

void populate_from_input_file(char passports[][MAX_PASSPORT_SIZE])
{
    // Used to juggle file strings into current passport string
    int counter = 0;
    char buffer[MAX_PASSPORT_SIZE];
    char current_passport[MAX_PASSPORT_SIZE] = "";

    FILE *file_pointer = fopen("input.txt", "r");

    while (fgets(buffer, MAX_PASSPORT_SIZE, file_pointer) != NULL)
    {
        if (strcmp(buffer, "\n") == 0) // Same
        {
            // End of a passport reached, add it to list and reset current passport
            strcpy(passports[counter], current_passport);
            strcpy(current_passport, "");
            counter++;
        }
        else
        {
            // Add info chunk to current passport
            strcat(current_passport, buffer);
        }
    }

    // Add final buffer to passports if it's not in there already
    // Note: This should be taken care of in the above loop, but I'm not sure how to do it
    if (strcmp(passports[counter], current_passport) != 0)
    {
        strcpy(passports[counter], current_passport);
    }
}

long get_solution()
{
    // Populate passports from file
    char passports[MAX_PASSPORTS][MAX_PASSPORT_SIZE];
    populate_from_input_file(passports);

    int num_valid_passports = 0;

    int counter = 0;
    char current_passport[MAX_PASSPORT_SIZE];
    while (strcmp(passports[counter], "") != 0) // Not the same
    {
        strcpy(current_passport, passports[counter]);
        counter++;

        // Test each condition and move on at first failure
        if (strstr(current_passport, "byr:") == NULL) // Substring not found
            continue;
        if (strstr(current_passport, "iyr:") == NULL)
            continue;
        if (strstr(current_passport, "eyr:") == NULL)
            continue;
        if (strstr(current_passport, "hgt:") == NULL)
            continue;
        if (strstr(current_passport, "hcl:") == NULL)
            continue;
        if (strstr(current_passport, "ecl:") == NULL)
            continue;
        if (strstr(current_passport, "pid:") == NULL)
            continue;

        // Increment as no failures
        num_valid_passports++;
    }

    return num_valid_passports;
}

int main()
{
    time_t start_time = time(NULL);

    long solution = get_solution();
    solution ? printf("Solution is: %ld\n", solution) : printf("No solution found.\n");

    printf("Time taken: %lds\n", time(NULL) - start_time);

    return 0;
}
