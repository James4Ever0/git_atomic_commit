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
