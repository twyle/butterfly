# butterfly

## Overview

A web application for sharing images and messages with your friends.

<p align=center>
  <img src="assets/videos/butterfly.gif" />
</p>

You can also like, bookmark and comments on posts.

## Getting Started

To get started, clone the repo:
1. Clone the project repo:

  ```sh
  git clone https://github.com/twyle/butterfly.git
  ```

2. Navigate to the project directory, then create the project secrets:

  ```sh
  cd butterfly
  touch ./services/app/.env
  ```

  And then paste the following:
  ```sh
  FLASK_DEBUG=True
  FLASK_ENV=development
  FLASK_APP=manage.py 
  SECRET_KEY=secret-key 
  POSTGRES_HOST=localhost
  POSTGRES_USER=lyle
  POSTGRES_PASSWORD=lyle
  POSTGRES_DB=lyle
  POSTGRES_PORT=5432
  ```

3. Start the database server:
  ```sh
  docker-compose -f services/database/docker-compose up
  ```

4. Create and seed the database:
  ```sh
  python services/app/manage.py create_db
  python services/app/manage.py seed_db
  ```

5. Start the application:
  ```sh
  python services/app/manage.py run
  ```

5. Navigate to ```http://127.0.0.1:5000/``` to see the application.

## Author :black_nib:

* **Lyle Okoth** <[twyle](https://github.com/twyle)>