### Project setup
1. Install [Docker](https://docs.docker.com/get-docker/) and docker-compose
2. Rename .env.example to .env and fill values
3. Run command `docker-compose build && docker-compose up -d`
4. Enter address `localhost:8000/docs/swagger` in your browser to test API
5. Enter command `docker-compose exec app pytest` to test API and tasks with different test cases

### Notes
Instead of using `threading` module, I decided to use the celery library to run tasks in other threads.