import mysql.connector

def connect_db():
    """Connects to the MySQL database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="JobMatchingDB"
    )

def create_tables():
    """Creates the required tables if they don't exist."""
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root"
    )
    cursor = db.cursor()

    # Create database if not exists
    cursor.execute("CREATE DATABASE IF NOT EXISTS JobMatchingDB;")
    cursor.execute("USE JobMatchingDB;")

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            name VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL,
            experience INT NOT NULL,
            role ENUM('job_seeker', 'employer', 'admin') NOT NULL
        );
    """)

    # Create jobs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            job_id INT AUTO_INCREMENT PRIMARY KEY,
            employer_id INT NOT NULL,
            job_title VARCHAR(100) NOT NULL,
            job_description TEXT NOT NULL,
            required_skills TEXT NOT NULL,
            experience_required INT NOT NULL,
            FOREIGN KEY (employer_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
    """)

    # Create applications table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            job_id INT NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE CASCADE
        );
    """)

    # Create interviews table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interviews (
            interview_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            job_id INT NOT NULL,
            employer_id INT NOT NULL,
            interview_date DATE NOT NULL,
            interview_time TIME NOT NULL,
            mode ENUM('Online', 'In-Person') NOT NULL,
            status ENUM('Scheduled', 'Completed', 'Cancelled') DEFAULT 'Scheduled',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE CASCADE,
            FOREIGN KEY (employer_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
    """)

    db.commit()
    db.close()

if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully.")
