import requests
import json
import os
import subprocess
import time

# --- Configuration ---
CODEFORCES_HANDLE = "mandargurjar" # Replace with your Codeforces handle
LEETCODE_USERNAME = "mandargurjar" # Replace with your LeetCode username

# --- File Paths ---
CODEFORCES_INFO_FILE = "data/codeforces_info.json"
CODEFORCES_SUBMISSIONS_FILE = "data/codeforces_submissions.json"
LEETCODE_INFO_FILE = "data/leetcode_info.json"
LEETCODE_RECENT_SUBMISSIONS_FILE = "data/leetcode_recent_submissions.json"

# Ensure the 'data' directory exists
os.makedirs("data", exist_ok=True)

def run_git_command(command, commit_message=None):
    """
    Helper function to run git commands and handle potential errors.
    If commit_message is provided, it will also stage and commit.
    """
    try:
        # Configure Git user for the commit
        subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=True)
        subprocess.run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"], check=True)

        if commit_message:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            print(f"Git commit successful: '{commit_message}'")
        else:
            subprocess.run(command, check=True)
            print(f"Git command successful: {' '.join(command)}")

    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {e}")
        print(f"Command output (stdout): {e.stdout.decode()}")
        print(f"Command output (stderr): {e.stderr.decode()}")
        # Exit if git command fails, especially for crucial operations
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

def fetch_codeforces_data():
    """Fetches Codeforces user info and submission status."""
    print("Fetching Codeforces data...")
    cf_info_url = f"https://codeforces.com/api/user.info?handles={CODEFORCES_HANDLE}"
    cf_status_url = f"https://codeforces.com/api/user.status?handle={CODEFORCES_HANDLE}"

    try:
        info_response = requests.get(cf_info_url)
        info_response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        cf_info_data = info_response.json()

        with open(CODEFORCES_INFO_FILE, "w") as f:
            json.dump(cf_info_data, f, indent=4)
        print(f"Codeforces user info saved to {CODEFORCES_INFO_FILE}")
        run_git_command(None, f"feat: Update Codeforces user info for {CODEFORCES_HANDLE}") # Commit 1

        status_response = requests.get(cf_status_url)
        status_response.raise_for_status()
        cf_status_data = status_response.json()

        with open(CODEFORCES_SUBMISSIONS_FILE, "w") as f:
            json.dump(cf_status_data, f, indent=4)
        print(f"Codeforces submissions saved to {CODEFORCES_SUBMISSIONS_FILE}")
        run_git_command(None, f"feat: Update Codeforces submissions for {CODEFORCES_HANDLE}") # Commit 2

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Codeforces data: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding Codeforces JSON: {e}")

def fetch_leetcode_data():
    """Fetches LeetCode user profile statistics and recent accepted submissions via GraphQL."""
    print("Fetching LeetCode data...")
    graphql_url = "https://leetcode.com/graphql"

    # Query for user profile statistics
    profile_query = """
    query userProfile($username: String!) {
      matchedUser(username: $username) {
        username
        submitStats: submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
            submissions
          }
        }
        profile {
          ranking
          userAvatar
        }
        totalSolved
        easySolved
        mediumSolved
        hardSolved
        contributionPoint
        reputation
      }
    }
    """

    # Query for recent accepted submissions (limited to 20 for practicality)
    recent_submissions_query = """
    query recentAcSubmissions($username: String!) {
      recentAcSubmissionList(username: $username, limit: 20) {
        id
        title
        titleSlug
        timestamp
        statusDisplay
        lang
      }
    }
    """

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        # Fetch user profile data
        profile_payload = {
            "query": profile_query,
            "variables": {"username": LEETCODE_USERNAME}
        }
        profile_response = requests.post(graphql_url, headers=headers, json=profile_payload)
        profile_response.raise_for_status()
        leetcode_info_data = profile_response.json()

        with open(LEETCODE_INFO_FILE, "w") as f:
            json.dump(leetcode_info_data, f, indent=4)
        print(f"LeetCode user info saved to {LEETCODE_INFO_FILE}")
        run_git_command(None, f"feat: Update LeetCode user info for {LEETCODE_USERNAME}") # Commit 3

        # Fetch recent accepted submissions
        submissions_payload = {
            "query": recent_submissions_query,
            "variables": {"username": LEETCODE_USERNAME}
        }
        submissions_response = requests.post(graphql_url, headers=headers, json=submissions_payload)
        submissions_response.raise_for_status()
        leetcode_submissions_data = submissions_response.json()

        with open(LEETCODE_RECENT_SUBMISSIONS_FILE, "w") as f:
            json.dump(leetcode_submissions_data, f, indent=4)
        print(f"LeetCode recent submissions saved to {LEETCODE_RECENT_SUBMISSIONS_FILE}")
        run_git_command(None, f"feat: Update LeetCode recent submissions for {LEETCODE_USERNAME}") # Commit 4

    except requests.exceptions.RequestException as e:
        print(f"Error fetching LeetCode data: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding LeetCode JSON: {e}")

def main():
    """Main function to orchestrate data fetching and pushing."""
    print("Starting automated profile data update...")

    # Fetch data and commit in sequence to create multiple commits
    fetch_codeforces_data()
    time.sleep(1) # Small delay to ensure distinct commit timestamps if needed
    fetch_leetcode_data()

    # Final push after all commits are made
    print("Pushing changes to GitHub...")
    try:
        subprocess.run(["git", "push"], check=True)
        print("Successfully pushed all changes to GitHub!")
    except subprocess.CalledProcessError as e:
        print(f"Error pushing to GitHub: {e}")
        print(f"Command output (stdout): {e.stdout.decode()}")
        print(f"Command output (stderr): {e.stderr.decode()}")
        exit(1)

if __name__ == "__main__":
    main()
