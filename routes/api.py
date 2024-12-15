from flask import Blueprint, request, jsonify
from models.db_setup import Database
import re

# Define the Blueprint
api = Blueprint('api', __name__)

# Input Validator Class
class InputValidator:
    @staticmethod
    def validate_save_input(data):
        """
        Validate input for saving data.
        Ensures 'product_details', 'niche', and 'tone' are present and valid.
        """
        errors = []

        # Check for required fields
        if not data.get("product_details"):
            errors.append("product_details is required.")
        if not data.get("niche"):
            errors.append("niche is required.")
        if not data.get("tone"):
            errors.append("tone is required.")

        # Additional validation (e.g., length or pattern)
        if data.get("niche") and not re.match("^[A-Za-z0-9 ]+$", data["niche"]):
            errors.append("niche must only contain letters, numbers, and spaces.")

        return errors

# API Routes encapsulated in a class
class ApiRoutes:
    def __init__(self, db):
        self.db = db

    def register_routes(self):
        @api.route('/test', methods=['GET'])
        def test_route():
            """Test route to check if the API is working."""
            return jsonify({"message": "API is working!"})

        @api.route('/save_input', methods=['POST'])
        def save_input():
            """Route to save user inputs to the database."""
            data = request.json

            # Validate input data
            errors = InputValidator.validate_save_input(data)
            if errors:
                return jsonify({"errors": errors}), 400

            try:
                cursor = self.db.get_connection().connection.cursor()
                query = "INSERT INTO user_inputs (product_details, niche, tone) VALUES (%s, %s, %s)"
                cursor.execute(query, (data["product_details"], data["niche"], data["tone"]))
                self.db.get_connection().connection.commit()
                cursor.close()
                return jsonify({"message": "Data saved successfully!"}), 201

            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @api.route('/get_inputs', methods=['GET'])
        def get_inputs():
            """Route to fetch paginated user inputs."""
            try:
                page = int(request.args.get("page", 1))
                limit = int(request.args.get("limit", 5))
                offset = (page - 1) * limit

                cursor = self.db.get_connection().connection.cursor()
                query = "SELECT * FROM user_inputs LIMIT %s OFFSET %s"
                cursor.execute(query, (limit, offset))
                rows = cursor.fetchall()
                cursor.close()

                data = [
                    {
                        "id": row[0],
                        "product_details": row[1],
                        "niche": row[2],
                        "tone": row[3],
                        "created_at": row[4]
                    }
                    for row in rows
                ]
                return jsonify({"data": data, "page": page, "limit": limit}), 200

            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @api.route('/update_input/<int:id>', methods=['PUT'])
        def update_input(id):
            """Route to update existing user input by ID."""
            data = request.json

            # Validate input data
            errors = InputValidator.validate_save_input(data)
            if errors:
                return jsonify({"errors": errors}), 400

            try:
                cursor = self.db.get_connection().connection.cursor()

                # Check if the record exists
                check_query = "SELECT * FROM user_inputs WHERE id = %s"
                cursor.execute(check_query, (id,))
                record = cursor.fetchone()

                if not record:
                    return jsonify({"error": f"Record with ID {id} not found."}), 404

                # Update the record
                update_query = """
                    UPDATE user_inputs
                    SET product_details = %s, niche = %s, tone = %s
                    WHERE id = %s
                """
                cursor.execute(update_query, (data["product_details"], data["niche"], data["tone"], id))
                self.db.get_connection().connection.commit()
                cursor.close()

                return jsonify({"message": f"Data with ID {id} updated successfully!"}), 200

            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @api.route('/delete_input/<int:id>', methods=['DELETE'])
        def delete_input(id):
            """Route to delete user input by ID."""
            try:
                cursor = self.db.get_connection().connection.cursor()

                # Check if the record exists
                check_query = "SELECT * FROM user_inputs WHERE id = %s"
                cursor.execute(check_query, (id,))
                record = cursor.fetchone()

                if not record:
                    return jsonify({"error": f"Record with ID {id} not found."}), 404

                # Delete the record
                delete_query = "DELETE FROM user_inputs WHERE id = %s"
                cursor.execute(delete_query, (id,))
                self.db.get_connection().connection.commit()
                cursor.close()

                return jsonify({"message": f"Data with ID {id} deleted successfully!"}), 200

            except Exception as e:
                return jsonify({"error": str(e)}), 500
