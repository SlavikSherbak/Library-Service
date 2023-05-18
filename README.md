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
- Managing orders and tickets
- Creating movies with genres, actors
-	Creating cinema halls
-	Adding movie sessions
-	Filtering movies and movie sessions
