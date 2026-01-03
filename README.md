# GitHub User Data Analyzer v2.0

A Python application that fetches GitHub user data via API, stores it in SQLite database, and exports to CSV.

## Features

- 🔍 Search GitHub users by username
- 📊 Display user statistics (followers, repos, location, etc.)
- 💾 Save user data to SQLite database
- 📥 View all saved users in formatted table
- 📄 Export database to CSV file
- 🔐 Optional GitHub Token support (for higher API limits)

## How to Run

### 1. Install Requirements
```bash
pip install requests
```

### 2. Run the Program
```bash
python src/main.py
```

### 3. Menu Options

1. **Search & Analyze User** - Look up a GitHub user by username
2. **View Saved Users** - Display all users saved in database
3. **Export Database to CSV** - Export data to CSV file
4. **Exit** - Close the program

## Example Usage
```
=== GitHub User Data Analyzer v2 ===
1. Search & Analyze User
2. View Saved Users (Database)
3. Export Database to CSV
4. Exit

Seçiminiz (1-4): 1
GitHub kullanıcı adı: torvalds

==============================
 USER: torvalds
==============================
Name:        Linus Torvalds
Location:    Portland, OR
Followers:   269715
Repos:       9
Created:     2011-09-03
```

## Database

- **Database File:** `github_users.db`
- **Table:** `users` (username, name, followers, public_repos, created_at, saved_at)

## CSV Export

Running option 3 creates `github_users_export.csv` with all saved user data.

## Technologies Used

- Python 3.11
- `requests` - HTTP requests to GitHub API
- `sqlite3` - Local database
- `csv` - CSV file export

## Optional: GitHub Token

To increase API rate limits, add your GitHub Personal Access Token:

1. Go to https://github.com/settings/tokens
2. Create a new token with `public_repo` access
3. Add it to the code:
```python
GITHUB_TOKEN = "ghp_your_token_here"
```

## Project Structure
```
github-data-analyzer/
├── src/
│   └── main.py
├── README.md
└── .gitignore
```

## Learning Outcomes

- RESTful API consumption
- Database operations with SQLite
- File I/O (CSV export)
- Error handling and validation
- Object-oriented programming

## Author

mffffwbg-bit

## License

MIT
```

**Yapıştır, Cmd+S ile kaydet.**

---

**Sonra:**
```
git add README.md
git commit -m "Add comprehensive README documentation"
git push