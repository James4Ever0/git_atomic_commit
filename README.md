
for those lazy ones:

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


this repo intends to create atomic backup & recovery capability of the delicate `.git` directory, before and after commit operations.

backup directory shall be ignored and specified in `.gitignore` file.

to maximize compatibility, `rclone` is preferred. to enjoy `linux-timemachine` like convenience, you need to improvise.

---

in the future, we may make this into git hook to be fool-proof and easy-installable

---

timemachine is not working, maybe because the filesystem does not support hard links.

---

`--link-dest` is the secret sauce of timemachine. will `--copy-dest` work the same?

rsync's incremental backup secret is '--link-dest', but let's make a hard-link free version.

---



use `--backup-dir` or `--compare-dest` (better not!) for convenience.
