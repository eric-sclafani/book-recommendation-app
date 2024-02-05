from src import init_app  # pyright: ignore

app = init_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, load_dotenv=True)