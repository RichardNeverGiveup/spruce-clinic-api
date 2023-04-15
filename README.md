## Backend Demo of Spruce Clinic.
This project is based on FastApi, Postgres, Alembic, Sqlalchemy.

## Run this Api demo.
1. config your own database and authentication settings in an .env file.
2. use alembic setup tables of your own
3. run `bash uvicorn app.main:app` to start api
4. check Swagger Api documentation with `{{url}}/docs#/`