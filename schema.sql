CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    phone TEXT,
    email TEXT UNIQUE NOT NULL,
    password TEXT,
    active INTEGER DEFAULT 1,
    date_created DATE,
    hire_date DATE,
    user_type INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS Competency_Cat (
     category_id INTEGER PRIMARY KEY AUTOINCREMENT,
     cat_name TEXT,
     active INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS Comp_Assessment_Data (
    assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    assess_name TEXT,
    date_created TEXT,
    category_id INTEGER,
    active INTEGER DEFAULT 1,
    FOREIGN KEY (category_id)
        REFERENCES Competency_Cat (category_id)
);

CREATE TABLE IF NOT EXISTS Results_Comp_Assess (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    assessment_id INTEGER,
    score INTEGER DEFAULT 0,
    date_taken DATE,
    manager INTEGER,
    FOREIGN KEY (user_id)
        REFERENCES Users (user_id),
    FOREIGN KEY (assessment_id)
        REFERENCES Comp_Assessment_Data (assessment_id),
    FOREIGN KEY (manager)
        REFERENCES Users (user_id)
);