#include <ctype.h>
#include <stdbool.h>
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

bool is_byr_valid(char passport[])
{
    char year_str[5];
    strncpy(year_str, strstr(passport, "byr:") + 4, 4);
    long year = strtol(year_str, NULL, BASE_10);
    return year >= 1920 && year <= 2002;
}

bool is_iyr_valid(char passport[])
{
    char year_str[5];
    strncpy(year_str, strstr(passport, "iyr:") + 4, 4);
    long year = strtol(year_str, NULL, BASE_10);
    return year >= 2010 && year <= 2020;
}

bool is_eyr_valid(char passport[])
{
    char year_str[5];
    strncpy(year_str, strstr(passport, "eyr:") + 4, 4);
    long year = strtol(year_str, NULL, BASE_10);
    return year >= 2020 && year <= 2030;
}

bool is_hgt_valid(char passport[])
{
    char height_str[6];
    strncpy(height_str, strstr(passport, "hgt:") + 4, 5);
    long height = strtol(height_str, NULL, BASE_10);
    bool is_valid = false;
    if (strstr(height_str, "cm") > 0)
        is_valid = height >= 150 && height <= 193;
    else if (strstr(height_str, "in") > 0)
        is_valid = height >= 59 && height <= 76;
    // printf("%d - %s\n", is_valid, height_str);
    return is_valid;
}

bool is_hcl_valid(char passport[])
{
    char colour_str[9];
    strncpy(colour_str, strstr(passport, "hcl:") + 4, 8);
    bool is_valid = true;
    // First char needs to be a #
    if (colour_str[0] != '#')
        is_valid = false;
    // The next six chars need to be hexidecimal values
    for (int i = 1; i < 7; i++)
    {
        if (!isxdigit(colour_str[i]))
            is_valid = false;
    }
    // There should only be 6 hexadecimals
    if (isxdigit(colour_str[7]))
        is_valid = false;
    // printf("%d - %s\n", is_valid, colour_str);
    return is_valid;
}

bool is_ecl_valid(char passport[])
{
    char colour_str[4];
    strncpy(colour_str, strstr(passport, "ecl:") + 4, 3);
    bool is_valid = false;
    if (strcmp(colour_str, "amb") == 0)
        is_valid = true;
    if (strcmp(colour_str, "blu") == 0)
        is_valid = true;
    if (strcmp(colour_str, "brn") == 0)
        is_valid = true;
    if (strcmp(colour_str, "gry") == 0)
        is_valid = true;
    if (strcmp(colour_str, "grn") == 0)
        is_valid = true;
    if (strcmp(colour_str, "hzl") == 0)
        is_valid = true;
    if (strcmp(colour_str, "oth") == 0)
        is_valid = true;
    // printf("%d - %s\n", is_valid, colour_str);
    return is_valid;
}

bool is_pid_valid(char passport[])
{
    char passport_id_str[11];
    strncpy(passport_id_str, strstr(passport, "pid:") + 4, 10);
    bool is_valid = true;
    for (int i = 0; i < 9; i++)
    {
        // There need to be 9 digits
        if (!isdigit(passport_id_str[i]))
            is_valid = false;
    }
    // But only 9 digits
    if (isdigit(passport_id_str[9]))
        is_valid = false;
    // printf("%d - %s\n", is_valid, passport_id_str);
    return is_valid;
}

long get_solution()
{
    // Populate passports from file
    char passports[MAX_PASSPORTS][MAX_PASSPORT_SIZE];
    populate_from_input_file(passports);

    int num_valid_passports = 0;

    int counter = 0;
    char current_passport[MAX_PASSPORT_SIZE];
    int section_index;
    while (strcmp(passports[counter], "") != 0) // Not the same
    {
        strcpy(current_passport, passports[counter]);
        counter++;

        // Test each condition and move on at first failure
        if (strstr(current_passport, "byr:") == NULL) // Substring not found
            continue;
        else if (!is_byr_valid(current_passport))
            continue;

        if (strstr(current_passport, "iyr:") == NULL)
            continue;
        else if (!is_iyr_valid(current_passport))
            continue;

        if (strstr(current_passport, "eyr:") == NULL)
            continue;
        else if (!is_eyr_valid(current_passport))
            continue;

        if (strstr(current_passport, "hgt:") == NULL)
            continue;
        else if (!is_hgt_valid(current_passport))
            continue;

        if (strstr(current_passport, "hcl:") == NULL)
            continue;
        else if (!is_hcl_valid(current_passport))
            continue;

        if (strstr(current_passport, "ecl:") == NULL)
            continue;
        else if (!is_ecl_valid(current_passport))
            continue;

        if (strstr(current_passport, "pid:") == NULL)
            continue;
        else if (!is_pid_valid(current_passport))
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
