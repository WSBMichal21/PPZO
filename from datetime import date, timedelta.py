from datetime import date, timedelta

class Book:
    def __init__(self, book_id: int, title: str, author: str, year: int):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.is_available = True

    def __str__(self):
        if self.is_available:
            status = " Available "
        else:
            status = " Borrowed "

        tekst = f"[ID: {self.book_id}] \"{self.title}\" – {self.author} | ({self.year}) | {status}"

        return tekst


class Member:

    def __init__(self, member_id: int, name: str, email: str):
        self.member_id = member_id
        self.name = name
        self.email = email
        self.active_loans: list["Loan"] = []

    def __str__(self):
        liczba_wypozyczen = len(self.active_loans)

        wynik = f"[ID: {self.member_id}] {self.name} <{self.email}> | Active loans: {liczba_wypozyczen}"

        return wynik


class Loan:

    LOAN_DAYS = 14

    def __init__(self, loan_id: int, book: Book, member: Member):
        self.loan_id = loan_id
        self.book = book
        self.member = member
        self.loan_date: date = date.today()
        self.due_date: date = self.loan_date + timedelta(days=self.LOAN_DAYS)
        self.return_date: date | None = None

    @property
    def is_returned(self) -> bool:
        return self.return_date is not None

    @property
    def is_overdue(self) -> bool:
        if self.is_returned:
            return False
        return date.today() > self.due_date

    def __str__(self):
        if self.is_returned:
            status = f"Returned {self.return_date}"
        elif self.is_overdue:
            status = "Overdue"
        else:
            status = "Active"

        return (
            f"Loan #{self.loan_id}: \"{self.book.title}\" → {self.member.name} | "
            f"Due: {self.due_date} | {status}"
        )


class Library:
    def __init__(self, name: str):
        self.name = name
        self._books: dict[int, Book] = {}
        self._members: dict[int, Member] = {}
        self._loans: list[Loan] = []
        self._next_loan_id = 1

    def add_book(self, book: Book) -> None:
        self._books[book.book_id] = book
        print(f" Book added: {book}")

    def find_book(self, book_id: int) -> Book | None:
        return self._books.get(book_id)

    def register_member(self, member: Member) -> None:
        self._members[member.member_id] = member
        print(f" Member registered: {member}")

    def find_member(self, member_id: int) -> Member | None:
        return self._members.get(member_id)

    def borrow_book(self, book_id: int, member_id: int) -> Loan | None:
        book = self.find_book(book_id)
        member = self.find_member(member_id)

        if book is None:
            print(f" Book ID not found: {book_id}.")
            return None
        if member is None:
            print(f" Member ID not found: {member_id}.")
            return None
        if not book.is_available:
            print(f" Book \"{book.title}\" is already borrowed.")
            return None

        loan = Loan(self._next_loan_id, book, member)
        self._next_loan_id += 1

        book.is_available = False
        member.active_loans.append(loan)
        self._loans.append(loan)

        print(f" Book borrowed: {loan}")
        return loan

    def return_book(self, loan_id: int) -> bool:
        loan = next((l for l in self._loans if l.loan_id == loan_id), None)

        if loan is None:
            print(f" Loan #{loan_id} not found.")
            return False
        if loan.is_returned:
            print(f" Loan #{loan_id} has already been returned.")
            return False

        loan.return_date = date.today()
        loan.book.is_available = True
        loan.member.active_loans.remove(loan)

        info = " (overdue!)" if date.today() > loan.due_date else ""
        print(f" Returned \"{loan.book.title}\" by {loan.member.name}{info}")
        return True

    def list_books(self) -> None:
        print(f"\n{'='*55}")
        print(f"  BOOK CATALOG – {self.name}")
        print(f"{'='*55}")
        for book in self._books.values():
            print(f"{book}")

    def list_members(self) -> None:
        print(f"\n{'='*55}")
        print(f" MEMBERS – {self.name}")
        print(f"{'='*55}")
        for member in self._members.values():
            print(f"  {member}")

    def list_loans(self) -> None:
        print(f"\n{'='*55}")
        print(f" LOAN HISTORY – {self.name}")
        print(f"{'='*55}")
        if not self._loans:
            print("  No loans.")
        for loan in self._loans:
            print(f"  {loan}")

    def list_overdue(self) -> None:
        overdue = [l for l in self._loans if l.is_overdue]
        print(f"\n{'─'*55}")
        print(f" OVERDUE LOANS")
        print(f"{'─'*55}")
        if not overdue:
            print(" No overdue loans. ")
        for loan in overdue:
            print(f"{loan}")


if __name__ == "__main__":
    print("=" * 55)
    print(" Virtual Library ")
    print("=" * 55)

    lib = Library("Virtual Library")

    print("\n Adding books ")
    lib.add_book(Book(1, "The Witcher: The Last Wish", "Andrzej Sapkowski", 1993))
    lib.add_book(Book(2, "Konrad Wallenrod",           "Adam Mickiewicz",   1961))
    lib.add_book(Book(3, "Pan Tadeusz",                "Adam Mickiewicz",   1834))
    lib.add_book(Book(4, "The Doll",                   "Bolesław Prus",     1890))

    print("\n[ Member Registration ]")
    lib.register_member(Member(101, "Anna Kowalska",    "anna@example.com"))
    lib.register_member(Member(102, "Jan Nowak",        "jan@example.com"))
    lib.register_member(Member(103, "Maria Wiśniewska", "maria@example.com"))

    print("\n[ Borrowing ]")
    loan1 = lib.borrow_book(1, 101)
    loan2 = lib.borrow_book(2, 102)
    loan3 = lib.borrow_book(1, 103)
    loan4 = lib.borrow_book(3, 103)

    lib.list_books()
    lib.list_members()

    print(" Returns ")
    lib.return_book(1)