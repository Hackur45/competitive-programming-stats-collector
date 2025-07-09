import requests
import json
import os
import subprocess
import time

# --- Configuration ---
CODEFORCES_HANDLE = "mandargurjar"
LEETCODE_USERNAME = "mandargurjar"

# --- Ensure 'data' directory exists ---
os.makedirs("data", exist_ok=True)

# --- Get next versioned filename ---
def get_next_versioned_filename(base_path, prefix):
    existing_files = [f for f in os.listdir(base_path) if f.startswith(prefix) and f.endswith(".json")]
    version_numbers = [
        int(f.split("_")[-1].split(".")[0])
        for f in existing_files
        if f.split("_")[-1].split(".")[0].isdigit()
    ]
    next_version = max(version_numbers, default=0) + 1
    return os.path.join(base_path, f"{prefix}_{next_version}.json")

# --- Run Git commands ---
def run_git_command(command, commit_message=None):
    try:
        subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=True)
        subprocess.run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"], check=True)

        if commit_message:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            print(f"✅ Git commit: '{commit_message}'")
        elif command:
            subprocess.run(command, check=True)
            print(f"✅ Git command successful: {' '.join(command)}")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error running git command: {e}")
        if e.stdout:
            print(f"stdout: {e.stdout.decode()}")
        if e.stderr:
            print(f"stderr: {e.stderr.decode()}")
    except Exception as e:
        print(f"❌ Unexpected error running git command: {e}")

# --- Fetch Codeforces Data ---
def fetch_codeforces_data():
    print("🔵 Fetching Codeforces data...")
    try:
        cf_info_url = f"https://codeforces.com/api/user.info?handles={CODEFORCES_HANDLE}"
        cf_status_url = f"https://codeforces.com/api/user.status?handle={CODEFORCES_HANDLE}"

        # Fetch and save user info
        info_response = requests.get(cf_info_url)
        info_response.raise_for_status()
        cf_info_data = info_response.json()
        info_file = get_next_versioned_filename("data", "codeforces_info")
        with open(info_file, "w") as f:
            json.dump(cf_info_data, f, indent=4)
        print(f"✅ Saved Codeforces info to {info_file}")
        run_git_command(None, f"feat: Add Codeforces info version {info_file.split('_')[-1].split('.')[0]}")

        # Fetch and save submissions
        status_response = requests.get(cf_status_url)
        status_response.raise_for_status()
        cf_status_data = status_response.json()
        status_file = get_next_versioned_filename("data", "codeforces_submissions")
        with open(status_file, "w") as f:
            json.dump(cf_status_data, f, indent=4)
        print(f"✅ Saved Codeforces submissions to {status_file}")
        run_git_command(None, f"feat: Add Codeforces submissions version {status_file.split('_')[-1].split('.')[0]}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching Codeforces data: {e}")
    except Exception as e:
        print(f"❌ Unexpected error in Codeforces fetch: {e}")

# --- Fetch LeetCode Data ---
def fetch_leetcode_data():
    print("🟠 Fetching LeetCode data...")
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
        # Fetch and save profile
        print(f"🔍 Fetching profile for: {LEETCODE_USERNAME}")
        profile_payload = {"query": profile_query, "variables": {"username": LEETCODE_USERNAME}}
        profile_response = requests.post(graphql_url, headers=headers, json=profile_payload)
        profile_response.raise_for_status()
        profile_data = profile_response.json()

        if "errors" in profile_data or not profile_data.get("data", {}).get("matchedUser"):
            print("❌ Error: No matched user or GraphQL errors in profile")
        else:
            profile_file = get_next_versioned_filename("data", "leetcode_info")
            with open(profile_file, "w") as f:
                json.dump(profile_data, f, indent=4)
            print(f"✅ Saved LeetCode info to {profile_file}")
            run_git_command(None, f"feat: Add LeetCode info version {profile_file.split('_')[-1].split('.')[0]}")

        # Fetch and save recent submissions
        print("📥 Fetching recent submissions...")
        submissions_payload = {"query": recent_submissions_query, "variables": {"username": LEETCODE_USERNAME}}
        submissions_response = requests.post(graphql_url, headers=headers, json=submissions_payload)
        submissions_response.raise_for_status()
        submissions_data = submissions_response.json()

        if "errors" in submissions_data or not submissions_data.get("data", {}).get("recentAcSubmissionList"):
            print("❌ Error: No recent submissions or GraphQL errors")
        else:
            submissions_file = get_next_versioned_filename("data", "leetcode_recent_submissions")
            with open(submissions_file, "w") as f:
                json.dump(submissions_data, f, indent=4)
            print(f"✅ Saved LeetCode recent submissions to {submissions_file}")
            run_git_command(None, f"feat: Add LeetCode submissions version {submissions_file.split('_')[-1].split('.')[0]}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching LeetCode data: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"📄 Status Code: {e.response.status_code}")
            print(f"📄 Response Body:\n{e.response.text}")
    except Exception as e:
        print(f"❌ Unexpected error in LeetCode fetch: {e}")

# --- Main Execution ---
def main():
    print("🚀 Starting profile data update...")
    fetch_codeforces_data()
    time.sleep(1)
    fetch_leetcode_data()

    print("📤 Pushing changes to GitHub...")
    try:
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
        if result.stdout.strip():
            print("📌 Final commit for remaining changes...")
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
