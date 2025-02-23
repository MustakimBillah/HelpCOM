import subprocess
from datetime import datetime
import time

def git_log_executer(repo_path, start_line, end_line, file_path):
    # Construct the command
    #command = ['git', 'log', f'-L {start_line},{end_line}:{file_path}']
    command = ['git', 'blame', '-L', f'{start_line},{end_line}', file_path]
    
    total_commits = 0
    diff_count = 0
    unique_authors = 0
    first_commit_date = last_commit_date = time_frame = ''

    try:
        # Execute the command in the specified repository path 
        result = subprocess.run(command, check=True, text=True, capture_output=True, cwd=repo_path)
        
        # Print the output
        output = result.stdout
        print("Command: ",command)
        print("Git Log Output:\n")
        print(output)
        
        # Parse the output and get commit details
        commits, dates, diff_count, authors = parse_git_log_output(output)
        
        # Calculate and print the total number of commits
        total_commits = len(commits)
        #print(f"\nTotal Number of Commits: {total_commits}")
        
        # Calculate and print the number of diffs
        #print(f"Number of Diffs: {diff_count}")
        
        # Calculate and print the number of unique authors
        unique_authors = len(set(authors))
        #print(f"Number of Unique Authors: {unique_authors}")
        
        if dates:
            # Calculate and print the time frame between the first and last commit
            first_commit_date = min(dates)
            last_commit_date = max(dates)
            time_frame = last_commit_date - first_commit_date
            #print(f"First Commit Date: {first_commit_date}")
            #print(f"Last Commit Date: {last_commit_date}")
            #print(f"Time Frame Between First and Last Commit: {time_frame}")
        
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running git log: {e}")
        time.sleep(5)
        
    return total_commits, diff_count, unique_authors, first_commit_date, last_commit_date, time_frame

def parse_git_log_output(output):
    # Split the output into individual commits
    commits = output.split('\ncommit ')
    commit_details = []
    commit_dates = []
    diff_count = 0
    authors = []

    for commit in commits:
        if commit.strip():  # Skip any empty entries
            commit_info = {}
            lines = commit.split('\n')
            for line in lines:
                if line.startswith('commit '):
                    commit_info['hash'] = line.split()[1]
                elif line.startswith('Author:'):
                    author = line.split('Author:')[1].strip()
                    commit_info['author'] = author
                    authors.append(author)
                elif line.startswith('Date:'):
                    date_str = line.split('Date:')[1].strip()
                    commit_date = datetime.strptime(date_str, '%a %b %d %H:%M:%S %Y %z')
                    commit_info['date'] = commit_date
                    commit_dates.append(commit_date)
                elif line.startswith('diff --git'):
                    diff_count += 1
                    break

            commit_details.append(commit_info)
    
    return commit_details, commit_dates, diff_count, authors

# test code
total_commits, diff_count, unique_authors, first_commit_date, last_commit_date, time_frame =git_log_executer('/student/mjr175/phpProject/phpunit/',229,244,'src/Util/PHP/DefaultJobRunner.php')

print(diff_count,total_commits)