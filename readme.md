# Competitive Programming Profile Data Collector

This repository automates the collection of your competitive programming profile data from **Codeforces** and **LeetCode**, storing it in a structured, versioned format within your GitHub repository.

---

## 🎯 Purpose of Data Collection

The primary goal of collecting this data is to build a **personal data dashboard**. This dashboard provides a comprehensive and evolving overview of your competitive programming journey. By centralizing this information, you can:

- **📈 Visualize Progress and Trends**  
  Track your rating changes, submission patterns, problem-solving distribution across difficulties, and overall performance over time. This helps in identifying strengths and areas for improvement.

- **📊 Analyze Performance Metrics**  
  Gain insights into your problem-solving speed, accuracy, and consistency. Understand which types of problems you excel at and where you might need more practice.

- **🏆 Showcase Achievements**  
  Create a dynamic portfolio of your competitive programming accomplishments, which can be valuable for personal reflection, sharing with peers, or demonstrating skills to potential employers.

- **📚 Identify Learning Opportunities**  
  By analyzing your submission history and problem statistics, you can pinpoint specific topics or problem types where you frequently struggle, guiding your future learning efforts.

---

## 📦 Data Collected

Currently, this repository collects and stores versioned data under the `data/` directory:

### ✅ Codeforces:
- `data/codeforces/codeforces_info_*.json` — User Information (Rating, Rank, Max Rating, etc.)
- `data/codeforces/codeforces_submissions_*.json` — Submission Status (all your submission data)

### ✅ LeetCode:
- `data/leetcode/leetcode_info_*.json` — User Profile Statistics (Total Solved, Ranking, Difficulty-wise Stats, etc.)
- `data/leetcode/leetcode_recent_submissions_*.json` — Recent Accepted Submissions (latest successful problem attempts)

Each time the script runs, new files are generated with an incremented version number (e.g., `_1.json`, `_2.json`, etc.), preserving your full history over time.

---

## ⚙️ Automation with GitHub Actions

The data collection process is fully automated using **GitHub Actions**:

- A workflow runs on a schedule (e.g., every hour or once a day)
- It executes the `update_profile_data.py` script
- Fresh data is fetched from Codeforces and LeetCode
- Results are saved as versioned JSON files under the appropriate folders
- Changes are committed and pushed automatically to the repository

---

## 🚀 Setup Instructions

To set up this automation for your own profile:

1. **⭐ Fork this repository**  
   Click "Fork" on the top right of this repo to copy it to your GitHub account.

2. **🛠 Update `update_profile_data.py`:**  
   Edit this section with your handles:
   ```python
   CODEFORCES_HANDLE = "your_codeforces_handle"
   LEETCODE_USERNAME = "your_leetcode_username"
