createdb -h localhost -p 5432 -U postgres lookingglass 
create user lookingglassdev WITH password 'password';

ALTER ROLE lookingglassdev SET client_encoding TO 'utf8';
ALTER ROLE lookingglassdev SET default_transaction_isolation TO 'read committed';
ALTER ROLE lookingglassdev SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE lookingglass TO lookingglassdev;

%superuser: lookingglassadmin, P@ssw0rd
