this repo intends to create atomic backup & recovery capability of the delicate `.git` directory, before and after commit operations.

backup directory shall be ignored and specified in `.gitignore` file.

to maximize compatbility, `rclone` is preferred. to enjoy `linux-timemachine` like convenience, you need to improvise.

---

in the future, we may make this into git hook to be fool-proof and easy-installable
