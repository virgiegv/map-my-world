# map-my-world
This is a project for management of locations of interest around the world.

## Instructions to run

### Option 1: Run with Docker
```docker-compose up --build```

### Option 2: Run manually

1) Install fastapi:
```pip install "fastapi[standard]"```

2) Install requirements
```pip install requirements.txt```

3) Install PostgreSQL v16

4) Create a database named "mapmyworld" and substitute user and password in the DATABASE_URL variable in .env file.
You can also change the database name if you wish. 

5) Run the app:
```fastapi dev main.py```

### Access API
Once the project is running, it will be accessible on http://localhost:8000 or http://127.0.0.1:8000. 


## Run tests:
1) Create database for tests named "testmapmyworld" and substitute user and password in the SQLALCHEMY_TEST_DATABASE_URL variable in src/tests/conf_test.py
You can also change this database name.
2) ```pip install pytest```
3) ```pytest src/tests/test_crud.py```


## Documentation

API docs will be available at http://127.0.0.1/docs 

A Postman collection with examples is available at: https://documenter.getpostman.com/view/36652229/2sA3s7jpLS

See other docs at this repo's wiki. 
