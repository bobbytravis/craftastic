from flask import Flask
from config import Config
from models.db_setup import Database
from routes.api import api, ApiRoutes

# Initialize Flask App
app = Flask(__name__)

# Apply Configurations
app.config['MYSQL_HOST'] = Config.MYSQL_HOST
app.config['MYSQL_USER'] = Config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = Config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = Config.MYSQL_DB

# Initialize Database
db = Database(app)

# Register API Routes
api_routes = ApiRoutes(db)
api_routes.register_routes()
app.register_blueprint(api, url_prefix="/api")

@app.route('/')
def home():
    """Home Route"""
    return "Welcome to Craftastic Backend!"

if __name__ == "__main__":
    app.run(debug=True)
