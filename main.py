import sqlalchemy as sa
import sqlalchemy.orm as so

from src import app, db
from src.models import Post, User


@app.shell_context_processor
def make_shell_context():
    """When 'flask shell' is called, this func registers these items to the shell"""
    return {"sa": sa, "so": so, "db": db, "User": User, "Post": Post}


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, load_dotenv=True)
