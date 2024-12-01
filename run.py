from app import app, db
import logging 
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.debug("+++ Starting Application +++")
    print("=== Starting Application ===", flush=True)
    db.init_db()
    app.run(debug=True)