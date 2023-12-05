
Have you ever encountered corrupted git repositories before? This tool is for you!

By default it will create backup of the `.git` folder before and after commitment if it has passed integrity checks. It also checks necessarity of commitment, whether commitment is done right, automatically repairments and more!

----

For those lazy ones:

1. Install necessary binaries (`rclone`, `git`, `python3` (you may need Py3.8 or newer)) to your PATH
2. Setup necessary dependencies: `pip3 install -r requirements.txt`
3. Write platform specific/independent commit scripts: `commit.cmd`, `commit.sh`, `commit.py`, etc...
4. Test by running `python3 atomic_commit.py`
5. Run this in scheduler like `crond` or Windows Task Scheduler

----

Command line arguments:

```
usage: atomic_commit.py [-h] [--install_dir INSTALL_DIR]
                        [--skip_conflict_check SKIP_CONFLICT_CHECK]
                        [--rclone_flags RCLONE_FLAGS]
                        [--backup_update_check_mode BACKUP_UPDATE_CHECK_MODE]
                        [--git_head_hash_acquisition_mode GIT_HEAD_HASH_ACQUISITION_MODE]
                        [--dotenv DOTENV]

options:
  -h, --help            show this help message and exit
  --install_dir INSTALL_DIR
                        [  type ]       <class 'str'>
                        [default]
                        Directory for installation (if set, after installation the program will exit)
  --skip_conflict_check SKIP_CONFLICT_CHECK
                        [  type ]       <class 'bool'>
                        [default]       False
                        Skip duplication/conflict checks during installation.
  --rclone_flags RCLONE_FLAGS
                        [  type ]       <class 'str'>
                        [default]       -P
                        Commandline flags for rclone command
  --backup_update_check_mode BACKUP_UPDATE_CHECK_MODE
                        [  type ]       <enum 'BackupUpdateCheckMode'>       
                        [default]       commit_and_backup_flag_metadata      
                        Determines necessarity of backup
  --git_head_hash_acquisition_mode GIT_HEAD_HASH_ACQUISITION_MODE
                        [  type ]       <enum 'GitHeadHashAcquisitionMode'>  
                        [default]       rev_parse
                        How to acquire git HEAD (latest commit) hash
  --dotenv DOTENV       [  type ]       typing.Optional[str]
                        A single DotEnv file path
```


This repo intends to create atomic backup & recovery capability of the delicate `.git` directory, before and after commit operations.

Backup directory shall be ignored and specified in `.gitignore` file.

To maximize compatibility, `rclone` is preferred. to enjoy `linux-timemachine` like convenience, you need to improvise.

---

In the future, we may make this into git hook to be fool-proof and easy-installable

---

Timemachine is not working, maybe because the filesystem does not support hard links.

---

`--link-dest` is the secret sauce of timemachine. will `--copy-dest` work the same?

Rsync's incremental backup secret is '--link-dest', but let's make a hard-link free version.

---


Use `--backup-dir` or `--compare-dest` (better not!) for convenience.


## Star History

<img src="https://api.star-history.com/svg?repos=james4ever0/git_atomic_commit&Timeline" style="filter: invert(100%);"></img>