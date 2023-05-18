# Library site

API service for local library site written on DRF
 
# Installing using GitHub

```python
git clone https://github.com/SlavikSherbak/Library-Service.git
cd Library-Service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
set SECRET_KEY=<your secret key>
python manage.py migrate
python manage.py runserver
```

## Getting access
    create user via /api/users/
    get access token via /api/users/token/

# Features
- JWT authenticated
- Admin panel /admin/
- Documentation is located at /api/doc/swagger/
- Book Catalog: The system maintains a comprehensive catalog of all the books available in the library.
- Book Search: Users can search for books using various criteria, such as title, author, or daily fee. The system provides a convenient search functionality to help users find the books they are interested in.
- Book Borrowing: Users can request to borrow books through the online system. They can select the desired book(s) from the catalog and specify the borrowing period. The system checks the availability of the book(s) and manages the borrowing process.
- Borrowing History: The system maintains a record of all the books borrowed by each user, including the borrowing period and due dates. This history allows users to keep track of their borrowings and return books on time.
