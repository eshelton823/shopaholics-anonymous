[![Build Status](https://travis-ci.com/uva-cs3240-f19/project-102-shopaholics-anonymous-project.svg?token=pyQDwdxMaHxzptDxnTDV&branch=master)](https://travis-ci.com/uva-cs3240-f19/project-102-shopaholics-anonymous-project)
### Shopaholics Anonymous presents...

# Shopper Share

#### To set up local environment...
1. Install a local PostgreSQL environment and enable the service (will vary based on OS).
2. Get into psql (`sudo -u postgres psql` in Linux)
3. Run `CREATE USER app WITH PASSWORD 'NotAPassword!';` to create the app user.
4. Run `CREATE DATABASE shopaholics_anonymous WITH OWNER app;`
5. Grant necessary permissions with `GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app;`
6. To grant the ability to create the test database, add `psql -c "ALTER USER app CREATEDB;" -U postgres`.
7. Run the server to confirm operation.
