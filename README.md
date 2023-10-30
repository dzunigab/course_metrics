# MD-APISECURITY

## Descripcion 

Incluir la descripción del microservicio security

## Ednpoints

- GET `/ping` | Component health status (**Debe retornar el nombre del MS**)
- GET `/security/ping` | API health status (**Importante para el despliegue**)
- GET `/security`/ | Get security information
- POST `/security`/ | Create security information
- GET `/security/security/{id}` | Get security information by id
- PUT `/security/security/{id}` | Modify security information by id
- DELETE `/security/security/{id}` | Delete security information by id
### AUTH
- GET `/security/candidate/auth` | Validate for Candidate
- GET `/security/company/auth` | Validate for Company
- GET `/security/abcjobs/auth` | Validate for AbcJobs

## Variables de entorno

- `PORT` : `9003` | Puerto de ejecución del microservicio
- `NODEPORT` : `30203` | Puerto del NodePort para acceder al microservicio en el cluster
- `CORE_APIUSER_URL` | Variable para comunicarse con el MS (valida que el usuario exista)

## Ejecución local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r src/requirements.txt
export DEV_DATABASE_URL=postgresql://postgres:postgres@localhost:5432/abc_jobs CORE_APIUSER_URL=http://127.0.0.1:9000/users 
export FLASK_APP=src/app.py PYTHONPATH=./ FLASK_ENV=development TESTING=False FLASK_DEBUG=True FLASK_APP_NAME=md-apisecurity
gunicorn --bind 0.0.0.0:9003 manage:app --log-level debug --reload
```

## Ejecución en contenedor

**Importante** no modificar la variable PORT para que coincida con la planificada en el despliegue

```bash
docker build -t md-apisecurity:1.0.0 .
docker run -e PORT=9003 -p 9003:9003 --name md-apisecurity md-apisecurity:1.0.0
```

## Ejecucion de pruebas unitarias

```bash
export FLASK_APP=src/app.py PYTHONPATH=./ FLASK_ENV=testing TESTING=True FLASK_DEBUG=False FLASK_APP_NAME=md-apisecurity
python3 -m unittest -v src/tests/*.py
coverage run -m unittest discover -v -s src/tests/ -p 'test_*.py'
coverage report --fail-under=80 --omit=src/tests/base.py,src/models.py
```
