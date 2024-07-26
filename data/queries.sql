-- #! sqlite

-- #{ create_table
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    status TEXT NOT NULL,
    done BOOLEAN NOT NULL,
    date TEXT NOT NULL
);
-- #}

-- #{ add_task
INSERT INTO tasks (text, status, done, date) VALUES (?, ?, ?, ?);
-- #}

-- #{ get_all_tasks
SELECT * FROM tasks;
-- #}

-- #{ update_task
UPDATE tasks SET status = ?, done = ? WHERE id = ?;
-- #}

-- #{ remove_task
DELETE FROM tasks WHERE id = ?;
-- #}

-- #{ clear_tasks_table
DELETE FROM tasks;
-- #}
