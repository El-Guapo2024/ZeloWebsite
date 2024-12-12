from app import app, db

if __name__ == "__main__":
    print("=== Starting Application ===", flush=True)
    app.run(debug=True)