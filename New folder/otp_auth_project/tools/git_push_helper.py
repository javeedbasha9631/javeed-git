import subprocess
import os
import sys

PROJECT_DIR = r"c:\Users\HP\OneDrive\Desktop\New folder\otp_auth_project"

def run(cmd):
    print('--- running:', cmd)
    p = subprocess.run(cmd, shell=True, cwd=PROJECT_DIR, capture_output=True, text=True)
    print('returncode:', p.returncode)
    if p.stdout:
        print('stdout:\n', p.stdout)
    if p.stderr:
        print('stderr:\n', p.stderr)
    return p

# 1. check git repo
p = run('git rev-parse --is-inside-work-tree')
if p.returncode != 0:
    print('Not a git repository; initializing...')
    run('git init')
    # create main branch if git default is master; try to create 'main'
    run('git checkout -b main')
else:
    print('Already a git repository.')

# 2. add all files and commit
run('git add .')
# Check if there is anything to commit
p = run('git status --porcelain')
if p.stdout.strip() == '':
    print('No changes to commit.')
else:
    run('git commit -m "Initial commit: OTP auth project"')

# 3. check remote
p = run('git remote -v')
if p.stdout.strip() == '':
    print('\nNo git remote found. To push your code, add a remote and push:')
    print("  git remote add origin <your-repo-url>")
    print("  git push -u origin main")
    sys.exit(0)
else:
    print('\nGit remotes:')
    print(p.stdout)
    # try to push current branch
    # determine current branch
    q = run('git branch --show-current')
    branch = q.stdout.strip() if q.returncode == 0 else 'main'
    print('Current branch:', branch)
    print('Attempting to push to origin')
    r = run(f'git push -u origin {branch}')
    if r.returncode == 0:
        print('Push successful.')
    else:
        print('Push failed. You may need to authenticate or set a remote. See instructions above.')
