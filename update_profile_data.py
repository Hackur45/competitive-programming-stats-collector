import requests
import json
import os
import subprocess
import time

# --- Configuration ---
CODEFORCES_HANDLE = "mandargurjar"
LEETCODE_USERNAME = "mandargurjar"

# --- File Paths ---
CODEFORCES_INFO_FILE = "data/codeforces_info.json"
CODEFORCES_SUBMISSIONS_FILE = "data/codeforces_submissions.json"
LEETCODE_INFO_FILE = "data/leetcode_info.json"
LEETCODE_RECENT_SUBMISSIONS_FILE = "data/leetcode_recent_submissions.json"

# Ensure the 'data' directory exists
os.makedirs("data", exist_ok=True)

def run_git_command(command, commit_message=None):
    try:
        subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=True)
        subprocess.run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"], check=True)

        if commit_message:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            print(f"Git commit successful: '{commit_message}'")
        elif command:
            subprocess.run(command, check=True)
            print(f"Git command successful: {' '.join(command)}")

    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {e}")
        if e.stdout:
            print(f"Command output (stdout): {e.stdout.decode()}")
        if e.stderr:
            print(f"Command output (stderr): {e.stderr.decode()}")
    except Exception as e:
        print(f"An unexpected error occurred while running git command: {e}")

def fetch_codeforces_data():
    print("Fetching Codeforces data...")
    try:
        cf_info_url = f"https://codeforces.com/api/user.info?handles={CODEFORCES_HANDLE}"
        cf_status_url = f"https://codeforces.com/api/user.status?handle={CODEFORCES_HANDLE}"

        info_response = requests.get(cf_info_url)
        info_response.raise_for_status()
        cf_info_data = info_response.json()
        with open(CODEFORCES_INFO_FILE, "w") as f:
            json.dump(cf_info_data, f, indent=4)
        print(f"✅ Codeforces user info saved to {CODEFORCES_INFO_FILE}")
        run_git_command(None, f"feat: Update Codeforces user info for {CODEFORCES_HANDLE}")

        status_response = requests.get(cf_status_url)
        status_response.raise_for_status()
        cf_status_data = status_response.json()
        with open(CODEFORCES_SUBMISSIONS_FILE, "w") as f:
            json.dump(cf_status_data, f, indent=4)
        print(f"✅ Codeforces submissions saved to {CODEFORCES_SUBMISSIONS_FILE}")
        run_git_command(None, f"feat: Update Codeforces submissions for {CODEFORCES_HANDLE}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching Codeforces data: {e}")
    except Exception as e:
        print(f"❌ Unexpected error in Codeforces fetch: {e}")

def fetch_leetcode_data():
    print("Fetching LeetCode data...")
    graphql_url = "https://leetcode.com/graphql"

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
          realName
          aboutMe
          school
          websites
          countryName
          company
          jobTitle
          skillTags
          postViewCount
          reputation
          solutionCount
          categoryDiscussCount
        }
      }
    }
    """

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
        "User-Agent": "Mozilla/5.0"
    }

    try:
        print(f"🔍 Fetching LeetCode profile for: {LEETCODE_USERNAME}")
        profile_payload = {"query": profile_query, "variables": {"username": LEETCODE_USERNAME}}
        profile_response = requests.post(graphql_url, headers=headers, json=profile_payload)
        profile_response.raise_for_status()
        profile_data = profile_response.json()

        if "errors" in profile_data:
            print(f"❌ GraphQL Errors in Profile Query:\n{json.dumps(profile_data['errors'], indent=2)}")
        elif not profile_data.get("data", {}).get("matchedUser"):
            print(f"❌ No matched user found for LeetCode username: {LEETCODE_USERNAME}")
        else:
            with open(LEETCODE_INFO_FILE, "w") as f:
                json.dump(profile_data, f, indent=4)
            print(f"✅ LeetCode profile saved to {LEETCODE_INFO_FILE}")
            run_git_command(None, f"feat: Update LeetCode user info for {LEETCODE_USERNAME}")

        print(f"🔍 Fetching LeetCode recent submissions...")
        submissions_payload = {"query": recent_submissions_query, "variables": {"username": LEETCODE_USERNAME}}
        submissions_response = requests.post(graphql_url, headers=headers, json=submissions_payload)
        submissions_response.raise_for_status()
        submissions_data = submissions_response.json()

        if "errors" in submissions_data:
            print(f"❌ GraphQL Errors in Submissions Query:\n{json.dumps(submissions_data['errors'], indent=2)}")
        elif not submissions_data.get("data", {}).get("recentAcSubmissionList"):
            print(f"❌ No recent submissions found.")
        else:
            with open(LEETCODE_RECENT_SUBMISSIONS_FILE, "w") as f:
                json.dump(submissions_data, f, indent=4)
            print(f"✅ LeetCode recent submissions saved to {LEETCODE_RECENT_SUBMISSIONS_FILE}")
            run_git_command(None, f"feat: Update LeetCode recent submissions for {LEETCODE_USERNAME}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching LeetCode data: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"📄 Status Code: {e.response.status_code}")
            print(f"📄 Response Body:\n{e.response.text}")
    except Exception as e:
        print(f"❌ Unexpected error in LeetCode fetch: {e}")

def main():
    print("🚀 Starting automated profile data update...")
    fetch_codeforces_data()
    time.sleep(1)
    fetch_leetcode_data()

    print("📤 Pushing changes to GitHub...")
    try:
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
        if result.stdout.strip():
            print("📌 Changes detected. Making final commit...")
            run_git_command(None, "chore: Final commit for remaining changes")
        else:
            print("✅ No changes to commit.")

        current_branch = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
        subprocess.run(["git", "push", "origin", current_branch], check=True)
        print("✅ Successfully pushed all changes!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git push failed: {e}")
        if e.stdout:
            print(f"stdout: {e.stdout.decode()}")
        if e.stderr:
            print(f"stderr: {e.stderr.decode()}")
    except Exception as e:
        print(f"❌ Unexpected error during git push: {e}")

if __name__ == "__main__":
    main()
