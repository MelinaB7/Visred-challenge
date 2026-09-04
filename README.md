# VISRED — Challenge Full Stack (Scaffold)

Base del challenge: **Django + PostgreSQL + Docker**, ya configurada y corriendo.
Tu trabajo es construir la funcionalidad encima de esta base (app `policies/`).

## Requisitos

- Docker y Docker Compose instalados. Nada más (no necesitás Python ni Postgres locales).

## Cómo levantarlo

1. Copiá el archivo de entorno de ejemplo:

   ```bash
   cp .env.example .env
   ```

2. Levantá los servicios:

   ```bash
   docker compose up --build
   ```

   La primera vez descarga imágenes y construye; puede tardar un poco. El
   contenedor espera a que Postgres esté listo, aplica las migraciones y arranca
   el servidor.

3. Abrí <http://localhost:8000> — deberías ver un **"Hello world"**.

Listo, ya estás corriendo sobre el stack.

## Comandos útiles

Todo se ejecuta dentro del contenedor `web`:

```bash
# Crear migraciones después de tocar modelos
docker compose exec web python manage.py makemigrations

# Aplicar migraciones (también corre solo al levantar)
docker compose exec web python manage.py migrate

# Crear un superusuario para el admin de Django
docker compose exec web python manage.py createsuperuser

# Abrir una shell de Django
docker compose exec web python manage.py shell

# Ver logs
docker compose logs -f web
```

Para frenar todo: `docker compose down` (agregá `-v` si querés borrar también la
base de datos).

## Estructura

```
.
├── app/                    # Código Django (montado en el contenedor)
│   ├── config/             # Proyecto (settings, urls, wsgi)
│   ├── policies/           # App donde vas a trabajar
│   ├── templates/          # Templates HTML
│   ├── static/             # Assets locales (acá va Tabler, sin CDN)
│   └── manage.py
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh           # Espera la DB + migra + arranca
├── .env.example
└── requirements.txt
```

## Notas

- La configuración se lee de variables de entorno (ver `.env.example`).
- El código de `app/` está montado como volumen: los cambios se reflejan sin
  reconstruir la imagen (el `runserver` recarga solo).
- Si agregás dependencias en `requirements.txt`, reconstruí:
  `docker compose up --build`.
