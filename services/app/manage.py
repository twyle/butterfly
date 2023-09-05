from flask.cli import FlaskGroup
from butterfly.blueprints.database.models import (
    User, Post, Bookmark, Like, View, Comment
)
from butterfly.blueprints.database.database import create_all, drop_all
from butterfly import create_app
from butterfly.helpers.data_generator import generate_data

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command("create_db")
def create_db():
    create_all()
    
@cli.command("delete_db")
def delete_db():
    drop_all()
    
@cli.command("seed_db")
def seed_db():
    drop_all()
    create_all()
    generate_data()


if __name__ == "__main__":
    cli()