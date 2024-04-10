from db_manager import fetch_and_store_recipes

def main():
    print("Welcome to the Interactive Recipe Fetcher!")
    while True:
        query = input("Enter a recipe query (or type 'exit' to quit): ").strip()
        if query.lower() == 'exit':
            print("Exiting the program. Goodbye!")
            break

        if not query:
            print("Please enter a valid query.")
            continue

        while True:
            try:
                num_recipes = int(input("How many recipes would you like to retrieve? (Up to 10): "))
                if 1 <= num_recipes <= 10:
                    break
                else:
                    print("Please enter a number between 1 and 10.")
            except ValueError:
                print("Invalid input. Please enter a numerical value.")

        try:
            fetch_and_store_recipes(query, num_recipes)
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please try again.")
        else:
            print(f"{num_recipes} recipes fetched and stored successfully.")

if __name__ == '__main__':
    main()
