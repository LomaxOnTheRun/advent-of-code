#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define BASE_10 10

#define MAX_PASSWORD_ENTRY_LENGTH 100
#define NUM_PASSWORDS 1000

struct PasswordEntry
{
    long min_occurences;
    long max_occurences;
    char letter;
    char password[MAX_PASSWORD_ENTRY_LENGTH];
};

struct PasswordEntry *get_password_entries_from_input_file()
{
    // Used to juggle file strings into PasswordEntry structs
    int counter = 0;
    char buffer[MAX_PASSWORD_ENTRY_LENGTH];
    char *token;

    // Actual thing we want (static so I can return an array)
    static struct PasswordEntry password_entries[NUM_PASSWORDS];

    FILE *file_pointer = fopen("input.txt", "r");

    while (fgets(buffer, MAX_PASSWORD_ENTRY_LENGTH, (FILE *)file_pointer))
    {
        struct PasswordEntry password_entry;

        // Build password entry by parsing input strings
        token = strtok(buffer, "-");
        password_entry.min_occurences = strtol(token, NULL, BASE_10);
        token = strtok(NULL, " ");
        password_entry.max_occurences = strtol(token, NULL, BASE_10);
        token = strtok(NULL, ": ");
        password_entry.letter = *token;
        token = strtok(NULL, "");
        strcpy(password_entry.password, token);

        password_entries[counter++] = password_entry;
    }

    return password_entries;
}

long get_solution()
{
    struct PasswordEntry *password_entries = get_password_entries_from_input_file();
    struct PasswordEntry password_entry;

    int counter;
    char current_char;

    // The thing we actually care about
    int valid_passwords = 0;

    for (int i = 0; i < NUM_PASSWORDS; i++)
    {
        password_entry = *(password_entries + i);

        // Count the number of occurences of the letter in the password
        counter = 0;
        current_char = '_'; // Anything that isn't '\0'
        for (int j = 0; current_char != '\0'; j++)
        {
            current_char = password_entry.password[j];
            if (current_char == password_entry.letter)
            {
                counter++;
            }
        }

        // Only count passwords with valid numbers of the required letter
        if (counter >= password_entry.min_occurences && counter <= password_entry.max_occurences)
        {
            valid_passwords++;
        }
    }

    return valid_passwords;
}

int main()
{
    time_t start_time = time(NULL);

    long solution = get_solution();
    solution ? printf("Solution is: %ld\n", solution) : printf("No solution found.\n");

    printf("Time taken: %lds\n", time(NULL) - start_time);

    return 0;
}
