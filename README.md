# Uh-huh

## Web User guide:

To be deployed...

## CLI User guide:

0. Set up a vritual environment (Optional!)
1. Run `pip install -r requirements`
2. Run `python uhhuh_cli.py [Your time in H:MM:SS format] [trka.rs race result URL]`
   - Example: `python uhhuh_cli.py 0:30:00 https://trka.rs/results/803/gender/M/`

## Dev guide:

### Set up virtual environment:

1.  Run `python -m venv .venv`
2.  Run `pip install -r requirements`

### Initialize SQLite database:

1. Run `flask --app uhhuh init-db`

### Start flask server:

1. Run `flask --app uhhuh run --debug`
2. Goto http://127.0.0.1:5000

## Deployment guide:

### Set up virtual environment:

1.  Run `python -m venv .venv`
2.  Run `pip install -r requirements`

### Build:

1. Run `pip install build`
2. Run `python -m build --wheel`

   You can find the file in `dist/uhhuh-1.0.0-py2.py3-none-any.whl`.

   Copy this file to another machine, set up a new virtual environment, then install the file.

3. Run `pip install uhhuh-1.0.0-py2.py3-none-any.whl`

   Initialize new SQLite database

4. Run `flask --app uhhuh init-db`

### Configure the Secret Key

1. Run `python -c 'import secrets; print(secrets.token_hex())'` to output a random secret key

2. Create the `config.py` file in `.venv/var/uhhuh-instance/`. Copy the generated value into it. `SECRET_KEY = 'generated value goes here'`

### Run with a Production Server

1. Run `pip install waitress`
2. Run `waitress-serve --call 'uhhuh:create_app'`
3. Go to http://127.0.0.1:8080
