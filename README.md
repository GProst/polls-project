## Installation
Run:
1. `pip install -r requirements.txt`
2. `python manage.py makemigrations`
3. `python manage.py migrate`

## Starting the app
1. `python manage.py runserver 0.0.0.0:4080`
2. The app should be accessible at `http://localhost:4080/`

## API Documentation
`/swagger-ui/` - view all APIs

## Authenticating a user
1. The app uses Token-based authentication, to get a token submit `{"username":"admin","password":"admin"}`
payload to `POST /api-token-auth` endpoint. The admin token will be returned.
2. Use `Authorization: Token {your-token}` header to use APIs that require admin permissions