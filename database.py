import sqlite3

def create_connection():
    return sqlite3.connect("health_plan.db")

def initialize_database():
    conn = create_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        start_date_plan DATE NOT NULL,
        current_weight_kg REAL NOT NULL
    )
    ''')

    # Create exercise logs table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS exercise_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        date DATE NOT NULL,
        exercise_id INTEGER REFERENCES exercise_plan(id),
        sets_completed INTEGER,
        reps_completed INTEGER,
        duration_completed_seconds INTEGER,
        pain_notes TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    ''')

    # Create food logs table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS food_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        date DATE NOT NULL,
        meal_type TEXT NOT NULL,
        description TEXT,
        calories_kcal INTEGER,
        protein_g REAL,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    ''')

    conn.commit()
    conn.close()

def initialize_exercise_plan():
    conn = create_connection()
    cursor = conn.cursor()

    # Create exercise_plan table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS exercise_plan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        week_start INTEGER NOT NULL,
        week_end INTEGER NOT NULL,
        exercise_name TEXT NOT NULL,
        description TEXT NOT NULL,
        notes TEXT,
        UNIQUE(exercise_name, week_start, week_end)
    )
    ''')

    # Insert or update exercise plan data
    exercises = [
        (1, 4, "Abrazos de rodillas", "Acuéstate boca arriba, lleva las rodillas al pecho, mantén 20-30 segundos, repite 3-5 veces.", "Relaja la espalda baja, detente si hay dolor."),
        (1, 4, "Postura del niño", "Arrodíllate, siéntate sobre los talones, estira los brazos hacia adelante, mantén 10-30 segundos, repite 3-5 veces.", "Estira la espalda y las caderas, evita forzar."),
        (1, 4, "Estiramiento gato-vaca", "En posición de cuatro puntos, arquea la espalda hacia arriba y luego hacia abajo, realiza durante 30 segundos, 3-5 series.", "Mejora la movilidad espinal, realiza suavemente."),
        (1, 4, "Inclinación pélvica", "Acuéstate boca arriba, contrae los músculos abdominales, inclina la pelvis hacia arriba, mantén 5 segundos, repite 5-10 veces.", "Fortalece el core sin presión en la espalda."),
        (5, 8, "Puente", "Acuéstate boca arriba con las rodillas dobladas, levanta las caderas, mantén 5 segundos, realiza 1-2 series de 10 repeticiones.", "Fortalece glúteos y core, evita arquear la espalda."),
        (5, 8, "Rodillas al lado", "Acuéstate boca arriba con las rodillas dobladas, baja las piernas a un lado, mantén 5 segundos, cambia de lado, realiza durante 30 segundos, 3-5 series.", "Mejora la movilidad lumbar, realiza lentamente."),
        (9, 12, "Conchas", "Acuéstate de lado con las rodillas dobladas, levanta la rodilla superior, realiza 1-2 series de 10-15 repeticiones.", "Fortalece los glúteos, evita movimientos bruscos."),
        (9, 12, "Elevaciones de pierna", "Acuéstate de lado, levanta la pierna superior, realiza 1-2 series de 10-15 repeticiones.", "Fortalece las caderas, realiza con control."),
        (9, 12, "Sentadilla contra la pared", "Apóyate en una pared, deslízate hasta una posición sentada, mantén 10-30 segundos.", "Fortalece las piernas, detente si hay dolor.")
    ]

    for exercise in exercises:
        cursor.execute('''
        INSERT INTO exercise_plan (week_start, week_end, exercise_name, description, notes)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(exercise_name, week_start, week_end) DO UPDATE SET
            description = excluded.description,
            notes = excluded.notes
        ''', exercise)

    conn.commit()
    conn.close()

def update_exercise_plan_schema():
    conn = create_connection()
    cursor = conn.cursor()

    # Check if the notes column already exists
    cursor.execute("PRAGMA table_info(exercise_plan)")
    columns = [column[1] for column in cursor.fetchall()]
    if "notes" not in columns:
        # Add notes column to exercise_plan table
        cursor.execute('''
        ALTER TABLE exercise_plan ADD COLUMN notes TEXT
        ''')

    # Check if the media_path column already exists
    if "media_path" not in columns:
        # Add media_path column to exercise_plan table
        cursor.execute('''
        ALTER TABLE exercise_plan ADD COLUMN media_path TEXT
        ''')

    # Update media paths for exercises
    exercises_with_media = [
        ("Abrazos de rodillas", "media/abrazos_de_rodillas.jpg"),
        ("Postura del niño", "media/postura_del_nino.jpg"),
        ("Estiramiento gato-vaca", "media/estiramiento_gato_vaca.jpg"),
        ("Inclinación pélvica", "media/inclinacion_pelvica.jpg"),
        ("Puente", "media/puente.jpg"),
        ("Rodillas al lado", "media/rodillas_al_lado.jpg"),
        ("Conchas", "media/conchas.jpg"),
        ("Elevaciones de pierna", "media/elevaciones_de_pierna.jpg"),
        ("Sentadilla contra la pared", "media/sentadilla_contra_la_pared.jpg")
    ]

    for exercise_name, media_path in exercises_with_media:
        cursor.execute('''
        UPDATE exercise_plan SET media_path = ? WHERE exercise_name = ?
        ''', (media_path, exercise_name))

    conn.commit()
    conn.close()

def update_exercise_logs_schema():
    conn = create_connection()
    cursor = conn.cursor()

    # Check if the exercise_id column already exists
    cursor.execute("PRAGMA table_info(exercise_logs)")
    columns = [column[1] for column in cursor.fetchall()]
    if "exercise_id" not in columns:
        # Add exercise_id column to exercise_logs table
        cursor.execute('''
        ALTER TABLE exercise_logs ADD COLUMN exercise_id INTEGER REFERENCES exercise_plan(id)
        ''')

    conn.commit()
    conn.close()

def remove_exercise_name_column():
    conn = create_connection()
    cursor = conn.cursor()

    # Check if the exercise_name column exists
    cursor.execute("PRAGMA table_info(exercise_logs)")
    columns = [column[1] for column in cursor.fetchall()]
    if "exercise_name" in columns:
        # Create a temporary table without the exercise_name column
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS exercise_logs_temp (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date DATE NOT NULL,
            exercise_id INTEGER REFERENCES exercise_plan(id),
            sets_completed INTEGER,
            reps_completed INTEGER,
            duration_completed_seconds INTEGER,
            pain_notes TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
        ''')

        # Copy data from the old table to the new table
        cursor.execute('''
        INSERT INTO exercise_logs_temp (log_id, user_id, date, exercise_id, sets_completed, reps_completed, duration_completed_seconds, pain_notes)
        SELECT log_id, user_id, date, exercise_id, sets_completed, reps_completed, duration_completed_seconds, pain_notes
        FROM exercise_logs
        ''')

        # Drop the old table and rename the new table
        cursor.execute("DROP TABLE exercise_logs")
        cursor.execute("ALTER TABLE exercise_logs_temp RENAME TO exercise_logs")

    conn.commit()
    conn.close()

def check_for_duplicates_in_exercise_plan():
    conn = create_connection()
    cursor = conn.cursor()

    # Query to find duplicate entries in the exercise_plan table
    cursor.execute('''
    SELECT exercise_name, week_start, week_end, COUNT(*)
    FROM exercise_plan
    GROUP BY exercise_name, week_start, week_end
    HAVING COUNT(*) > 1
    ''')

    duplicates = cursor.fetchall()
    conn.close()

    return duplicates

def clean_up_exercise_plan_duplicates():
    conn = create_connection()
    cursor = conn.cursor()

    # Remove duplicate entries, keeping only the first occurrence
    cursor.execute('''
    DELETE FROM exercise_plan
    WHERE id NOT IN (
        SELECT MIN(id)
        FROM exercise_plan
        GROUP BY exercise_name, week_start, week_end
    )
    ''')

    # Add a unique constraint to prevent future duplicates
    cursor.execute('''
    CREATE UNIQUE INDEX IF NOT EXISTS unique_exercise_plan
    ON exercise_plan (exercise_name, week_start, week_end)
    ''')

    conn.commit()
    conn.close()

def add_default_columns_to_exercise_plan():
    conn = create_connection()
    cursor = conn.cursor()

    # Check if the default columns already exist
    cursor.execute("PRAGMA table_info(exercise_plan)")
    columns = [column[1] for column in cursor.fetchall()]

    if "default_sets" not in columns:
        cursor.execute("ALTER TABLE exercise_plan ADD COLUMN default_sets INTEGER DEFAULT 1")

    if "default_reps" not in columns:
        cursor.execute("ALTER TABLE exercise_plan ADD COLUMN default_reps INTEGER DEFAULT 1")

    if "default_duration" not in columns:
        cursor.execute("ALTER TABLE exercise_plan ADD COLUMN default_duration INTEGER DEFAULT 0")

    conn.commit()
    conn.close()

def update_default_values_in_exercise_plan():
    conn = create_connection()
    cursor = conn.cursor()

    # Update default values for each exercise
    default_values = [
        (3, 5, 30, "Abrazos de rodillas"),
        (3, 5, 30, "Postura del niño"),
        (3, 5, 30, "Estiramiento gato-vaca"),
        (5, 10, 5, "Inclinación pélvica"),
        (1, 10, 5, "Puente"),
        (3, 5, 30, "Rodillas al lado"),
        (1, 10, 0, "Conchas"),
        (1, 10, 0, "Elevaciones de pierna"),
        (1, 1, 10, "Sentadilla contra la pared")
    ]

    for sets, reps, duration, exercise_name in default_values:
        cursor.execute('''
        UPDATE exercise_plan
        SET default_sets = ?, default_reps = ?, default_duration = ?
        WHERE exercise_name = ?
        ''', (sets, reps, duration, exercise_name))

    conn.commit()
    conn.close()

def verify_and_update_exercise_plan_schema():
    conn = create_connection()
    cursor = conn.cursor()

    # Check if the default columns exist
    cursor.execute("PRAGMA table_info(exercise_plan)")
    columns = [column[1] for column in cursor.fetchall()]

    missing_columns = []
    if "default_sets" not in columns:
        missing_columns.append("default_sets")
        cursor.execute("ALTER TABLE exercise_plan ADD COLUMN default_sets INTEGER DEFAULT 1")

    if "default_reps" not in columns:
        missing_columns.append("default_reps")
        cursor.execute("ALTER TABLE exercise_plan ADD COLUMN default_reps INTEGER DEFAULT 1")

    if "default_duration" not in columns:
        missing_columns.append("default_duration")
        cursor.execute("ALTER TABLE exercise_plan ADD COLUMN default_duration INTEGER DEFAULT 0")

    conn.commit()
    conn.close()

    if missing_columns:
        print(f"Added missing columns to exercise_plan: {', '.join(missing_columns)}")
    else:
        print("All required columns are already present in exercise_plan.")

def get_user_id(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    user_id = cursor.fetchone()
    conn.close()
    return user_id[0] if user_id else None

# Add indexes to frequently queried columns for optimization
def optimize_database():
    conn = sqlite3.connect("health_plan.db")
    cursor = conn.cursor()

    # Add index to user_id in exercise_logs
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_exercise_logs_user_id ON exercise_logs (user_id)")

    # Add index to date in exercise_logs
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_exercise_logs_date ON exercise_logs (date)")

    # Add index to user_id in food_logs
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_food_logs_user_id ON food_logs (user_id)")

    # Add index to date in food_logs
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_food_logs_date ON food_logs (date)")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
    update_exercise_logs_schema()  # Ensure schema is updated before initializing the exercise plan
    remove_exercise_name_column()  # Remove redundant exercise_name column
    update_exercise_plan_schema()
    add_default_columns_to_exercise_plan()  # Ensure default columns are added to the schema
    verify_and_update_exercise_plan_schema()  # Verify and update schema
    initialize_exercise_plan()

    # Update default values in the exercise_plan table
    update_default_values_in_exercise_plan()

    # Clean up duplicates in the exercise_plan table
    clean_up_exercise_plan_duplicates()

    # Check for duplicates in the exercise_plan table
    duplicates = check_for_duplicates_in_exercise_plan()
    if duplicates:
        print("Duplicate entries found in exercise_plan after cleanup:")
        for duplicate in duplicates:
            print(duplicate)
    else:
        print("No duplicate entries found in exercise_plan after cleanup.")

    # Call the optimization function
    optimize_database()