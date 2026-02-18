PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS tasks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT,
  due_date TEXT,            -- format YYYY-MM-DD
  is_done INTEGER DEFAULT 0,
  created_at TEXT DEFAULT (datetime('now'))
);
