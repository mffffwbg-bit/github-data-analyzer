# ==========================================
# Project: GitHub User Data Analyzer (v2.0)
# Updated: Database Context Managers, CSV Export, Better UI
# Language: English
# ==========================================

import requests
import sqlite3
import csv
import os
from datetime import datetime

# GITHUB TOKEN (Optional - Add your token here to avoid API rate limits)
# Example: "ghp_xxxxxxxxxxxx"
GITHUB_TOKEN = "" 

class GitHubAPI:
    def __init__(self):
        self.base_url = "https://api.github.com/users"
        self.headers = {}
        
        # If a token is provided, add it to the headers
        if GITHUB_TOKEN:
            self.headers['Authorization'] = f'token {GITHUB_TOKEN}'
    
    def get_user_data(self, username):
        """Fetch user data from GitHub API"""
        try:
            response = requests.get(f"{self.base_url}/{username}", headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                print(f"[!] User not found: {username}")
                return None
            elif response.status_code == 403:
                print("[!] API rate limit exceeded. Wait a while or add a Token.")
                return None
            else:
                print(f"[!] Error occurred. Status Code: {response.status_code}")
                return None
        except Exception as e:
            print(f"[!] Connection error: {e}")
            return None

class DatabaseManager:
    def __init__(self, db_name="github_users.db"):
        self.db_name = db_name
        self.create_table()
    
    def get_connection(self):
        """Create a database connection"""
        return sqlite3.connect(self.db_name)

    def create_table(self):
        """Create database table (using Context Manager)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    name TEXT,
                    followers INTEGER,
                    public_repos INTEGER,
                    created_at TEXT,
                    saved_at TEXT
                )
            """)
    
    def save_user(self, user_data):
        """Save user data to the database"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO users 
                    (username, name, followers, public_repos, created_at, saved_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    user_data['login'],
                    user_data.get('name', 'N/A'), # Use .get to prevent errors if null
                    user_data['followers'],
                    user_data['public_repos'],
                    user_data['created_at'],
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ))
            print(f"[+] '{user_data['login']}' successfully saved to database.")
        except Exception as e:
            print(f"[!] Database error: {e}")
    
    def fetch_all_users(self):
        """Fetch data (Common function for Export and View)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT username, name, followers, public_repos, saved_at FROM users")
                return cursor.fetchall()
        except Exception as e:
            print(f"[!] Data fetch error: {e}")
            return []

    def view_all_users(self):
        """Display all saved users in the console"""
        users = self.fetch_all_users()
        if users:
            print(f"\n{'Username':<20} {'Name':<20} {'Followers':<10} {'Repos':<8} {'Saved Date':<20}")
            print("-" * 85)
            for user in users:
                # Truncate long names to prevent table misalignment
                u_name = str(user[1]) if user[1] else "N/A"
                print(f"{user[0][:19]:<20} {u_name[:19]:<20} {user[2]:<10} {user[3]:<8} {user[4]:<20}")
        else:
            print("[i] Database is empty.")

    def export_to_csv(self, filename="github_users_export.csv"):
        """Export data to a CSV file"""
        users = self.fetch_all_users()
        if not users:
            print("[i] No data to export.")
            return

        try:
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # Headers
                writer.writerow(["Username", "Name", "Followers", "Public Repos", "Saved At"])
                # Data rows
                writer.writerows(users)
            print(f"[+] Data successfully exported to '{filename}'!")
        except Exception as e:
            print(f"[!] File creation error: {e}")

class DataAnalyzer:
    @staticmethod
    def analyze_user(user_data):
        if not user_data: return
        
        print("\n" + "="*30)
        print(f" USER: {user_data['login']}")
        print("="*30)
        print(f"Name:        {user_data.get('name', 'N/A')}")
        print(f"Bio:         {user_data.get('bio', 'N/A')}")
        print(f"Location:    {user_data.get('location', 'N/A')}")
        print(f"Followers:   {user_data['followers']}")
        print(f"Repos:       {user_data['public_repos']}")
        print(f"Created:     {user_data['created_at'][:10]}") # Only take the date part
        print("-" * 30)

def main():
    api = GitHubAPI()
    db = DatabaseManager()
    
    while True:
        print("\n=== GitHub User Data Analyzer v2 ===")
        print("1. Search & Analyze User")
        print("2. View Saved Users (Database)")
        print("3. Export Database to CSV")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            username = input("Enter GitHub username: ").strip()
            if username:
                user_data = api.get_user_data(username)
                if user_data:
                    DataAnalyzer.analyze_user(user_data)
                    save = input("Save to database? (y/n): ")
                    if save.lower() == 'y':
                        db.save_user(user_data)
        
        elif choice == '2':
            db.view_all_users()
            
        elif choice == '3':
            db.export_to_csv()
            
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("[!] Invalid choice.")

if __name__ == "__main__":
    main()