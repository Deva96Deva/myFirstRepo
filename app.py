import json
import sqlite3
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs
import os

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "employees.db"
HOST = "0.0.0.0"
PORT = 8000


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone_number TEXT NOT NULL
            )
            """
        )
        conn.commit()


def add_employee(name, phone_number):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO employees (name, phone_number) VALUES (?, ?)",
            (name, phone_number),
        )
        conn.commit()


def get_employees():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            "SELECT id, name, phone_number FROM employees ORDER BY id"
        )
        return [dict(row) for row in cursor.fetchall()]


class EmployeeHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.path = "/templates/index.html"
            return super().do_GET()

        if self.path == "/employees":
            employees = get_employees()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(employees).encode("utf-8"))
            return

        return super().do_GET()

    def do_POST(self):
        if self.path != "/add":
            self.send_error(404, "Page not found")
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        data = parse_qs(body)
        name = data.get("name", [""])[0].strip()
        phone_number = data.get("phone_number", [""])[0].strip()

        if name and phone_number:
            add_employee(name, phone_number)

        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()


def run_server():
    os.chdir(BASE_DIR)
    init_db()
    server = HTTPServer((HOST, PORT), EmployeeHandler)
    print(f"Server is running at http://localhost:{PORT}")
    print("Press Ctrl+C to stop.")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
