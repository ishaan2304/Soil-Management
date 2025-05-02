import logging

# Configure logging for the application
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# Database Connection Function with Retry Logic
def connect_db(retries=3, delay=2):
    for attempt in range(retries):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            return conn
        except mysql.connector.Error as e:
            logging.error(f"Attempt {attempt+1}: Error connecting to database: {e}")
            if attempt < retries - 1:
                time.sleep(delay)  # Wait before retrying
            else:
                error_message = "Unable to connect to the database after multiple attempts."
                add_message(error_message, "error")
                return None


# Function to Insert Manual Soil Record with Enhanced Error Handling
def insert_manual_record(farm_location, test_date, nitrogen, phosphorus, potassium, pH, moisture):
    # Validate inputs
    if not farm_location:
        warning_message = "Farm Location field must be filled!"
        add_message(warning_message, "warning")
        return

    try:
        conn = connect_db()
        if not conn:
            return  # Exit if database connection fails

        cursor = conn.cursor()

        query = """
            INSERT INTO soil_health (farm_location, test_date, nitrogen_level, phosphorus_level, potassium_level, pH_level, moisture_content)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (farm_location, test_date, nitrogen, phosphorus, potassium, pH, moisture)

        cursor.execute(query, params)
        conn.commit()

        success_message = "Soil record inserted successfully!"
        add_message(success_message, "success")
    except mysql.connector.Error as e:
        error_message = f"Database error while inserting record: {e}"
        logging.error(error_message)
        add_message(error_message, "error")
    except Exception as e:
        error_message = f"Unexpected error: {e}"
        logging.error(error_message)
        add_message(error_message, "error")
    finally:
        if conn:
            conn.close()
