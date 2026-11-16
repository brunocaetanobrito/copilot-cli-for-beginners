from books import Book


def print_menu() -> None:
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    return input("Choose an option (1-5): ").strip()


def get_book_details() -> tuple[str, str, int]:
    title = input("Enter book title: ").strip()
    while not title:
        print("Title cannot be empty.")
        title = input("Enter book title: ").strip()

    author = input("Enter author: ").strip()
    while not author:
        print("Author cannot be empty.")
        author = input("Enter author: ").strip()

    while True:
        year_input = input("Enter publication year (leave blank if unknown): ").strip()
        if not year_input:
            year = 0
            break

        try:
            year = int(year_input)
        except ValueError:
            print("Invalid year. Please enter a whole number or leave it blank.")
            continue

        if year < 0:
            print("Invalid year. Please enter a non-negative number.")
            continue
        break

    return title, author, year


def print_books(books: list[Book]) -> None:
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if book.read else "📖 Unread"
        print(f"{index}. {book.title} by {book.author} ({book.year}) - {status}")
