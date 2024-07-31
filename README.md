# imperia_tfm

### As for now TFM folder contains a very basic and provisional infrastructure that looks as follows:
- imperia_db.sql script that creates three tables for the main data provided by Imperia. Further exploration is needed. 
- Docker-compose.yml file setting up a PostgreSQL service relying on the adjacent Dockerfile.
- Dockerfile.postgres file providing the initialisation scripts and the csv files.
- A init_db.sh db intialisation file that loads the data onto the recently created tables.

#### (Moreover you will find the csv files containing the data and a python notebook)

## How to deploy the db:
Open up a new terminal inside TFM folder. (Creating a virtual environment is higly recommended atm and will become necessary soon.) Now start docker on your machine and run the following command: `docker compose up --build`
Now this should be the last message shown on your terminal screen: `postgres_container  | 2024-07-03 10:03:36.648 UTC [1] LOG:  database system is ready to accept connections`

Now you should be able to connect to the database through your SQL client, such as DBeaver or similar. Generic .env should be created, though hidden on the repo which is not as for now. Check you're using the correct environment variable values. 

### There are still few issues to address:
- The punto_venta table is not being loaded its data for problems related to the primary key.
- A way of including all the data and csv files should be found.

## Next steps:
- Connect the notebook to the database and start an EDA taking that connection as the input is the current idea.
- Find feasible or more convenient alternatives to deploying a db. Otherwise, decide and implement the DB either on cloud or on local servers according to what might be more convenient. 
  

## API Deployment (JAVI)
Desde la carpeta TFM/Deploy, ejecutar `docker build -t modelo-ventas3 . ` para construir el contenedor y luego runear `docker run -p 5000:5000 modelo-ventas3` . Una vez hecho, se puede testear la API en http://127.0.0.1:5000 (localhost).