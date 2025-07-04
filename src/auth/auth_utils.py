import csv
import json
import os

USER_FILE = "data/user_data.csv"

def ensure_user_file():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["username", "password", "high_score"])

def export_users_to_json(json_path="auth/user_data.json"):
    ensure_user_file()
    users = []
    with open(USER_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            users.append({
                "username": row["username"],
                "password": row["password"],
                "high_score": int(row["high_score"])
            })

    with open(json_path, "w") as json_file:
        json.dump(users, json_file, indent=4)

    return json_path


def register_user(username, password):
    ensure_user_file()
    with open(USER_FILE, "r") as f:
        for row in csv.reader(f):
            if row and row[0] == username:
                return False  # user exists

    with open(USER_FILE, "a", newline='') as f:
        csv.writer(f).writerow([username, password, 0])
    return True

def login_user(username, password):
    ensure_user_file()
    with open(USER_FILE, "r") as f:
        for row in csv.reader(f):
            if row and row[0] == username and row[1] == password:
                return {"username": username, "high_score": int(row[2])}
    return None

def update_user_score(username, score):
    rows = []
    with open(USER_FILE, "r") as f:
        for row in csv.reader(f):
            if row and row[0] == username:
                high_score = max(int(row[2]), score)
                rows.append([row[0], row[1], high_score])
            else:
                rows.append(row)
    with open(USER_FILE, "w", newline='') as f:
        csv.writer(f).writerows(rows)

def get_all_users():
    ensure_user_file()
    with open(USER_FILE, "r") as f:
        return list(csv.reader(f))[1:]  
