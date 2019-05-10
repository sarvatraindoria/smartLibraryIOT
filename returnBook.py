from psql import dbCon


class Return:
    def __init__(self, username):
        self.username = username

    def checkBID(self, bid):
        qu = ("""select bookid
            from book
            """)
        bIDs = dbCon().selectQ(qu)
        bIDList = []
        for ids in bIDs:
            bIDList.append(ids[0])
        if bid in bIDList:
            return True
        else:
            return False

    def returnBook(self):
        b = ("""Select bookborrowed.bookid, title
        from bookborrowed inner join book
        on bookborrowed.bookid = book.bookid
        where lmsuserid = %s and status = 'borrowed' """)

        qRtn = ("""UPDATE bookborrowed
        SET status = 'returned',
        returneddate = current_date
        where bookid = %s and status = 'borrowed' """)

        books = dbCon().selectQ(b, self.username)
        if len(books) > 0:
            print("| Bookid | Title |")
            for r in books:
                print(str(r[0])+" | "+r[1])

            allBooks = ("""SELECT * FROM bookborrowed """)
            print("Enter Book ID to return")
            bookID = input()
            bookID = int(bookID)
            if self.checkBID(bookID):
                inputid = bookID
                booksIdList = []
                for book in books:
                    booksIdList.append(book[0])
                # check if the book has been borrowed
                bookRows = dbCon().selectQ(allBooks, self.username, inputid)
                flag = True
                for i in bookRows:
                    status = i[3][0]
                    if inputid not in booksIdList:
                        print("Invalid Book ID !")
                        break
                    elif status is 'b':
                        dbCon().insUpDel(qRtn, inputid)
                        print("Book return successful")
                        flag = False
                        break
                if flag is True:
                    print("The book has not been borrowed yet")
            else:
                print("Invalid book ID")
        else:
            print("No book to return !")