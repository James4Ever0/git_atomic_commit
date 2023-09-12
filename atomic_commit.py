import os
import sys
from log_utils import logger_print
import shutil
from enum import auto
from strenum import StrEnum

# import parse
from config_utils import EnvBaseModel, getConfig
import filelock
import pathlib


class BackupUpdateCheckMode(StrEnum):
    commit_and_backup_flag_metadata = auto()
    git_commit_hash = auto()


# class BackupMode(StrEnum):
#     incremental = auto()
#     last_time_only = auto()


class GitHeadHashAcquisitionMode(StrEnum):
    rev_parse = auto()
    log = auto()


from pydantic import Field

# you may need to sync description with title to use `pydantic_argparse`.


class AtomicCommitConfig(EnvBaseModel):
    # BACKUP_MODE: BackupMode = Field(
    #     default=BackupMode.last_time_only,
    #     title="Backup mode configuration"
    #     # default=BackupMode.last_time_only, description="Backup mode configuration"
    # )
    INSTALL_DIR: str = Field(
        default="",
        title="Directory for installation (if set, after installation the program will exit)",
    )
    RCLONE_FLAGS: str = Field(
        default="-P", title="Commandline flags for rclone command"
    )
    BACKUP_UPDATE_CHECK_MODE: BackupUpdateCheckMode = Field(
        default=BackupUpdateCheckMode.commit_and_backup_flag_metadata,
        title="Determines necessarity of backup",
    )
    GIT_HEAD_HASH_ACQUISITION_MODE: GitHeadHashAcquisitionMode = Field(
        default=GitHeadHashAcquisitionMode.rev_parse,
        title="How to acquire git HEAD (latest commit) hash",
    )


# from pydantic_argparse import ArgumentParser
# # import humps
# parser = ArgumentParser(
#         model=AtomicCommitConfig,
#         # prog="Example Program",
#         # description="Example Description",
#         # description = " ".join(humps.kebabize(AtomicCommitConfig.__name__).split("-")),
#         version="0.0.1",
#         # epilog="Example Epilog",
#     )
# args = parser.parse_typed_args()

# Print Args
# logger_print(args)
# exit()

config = getConfig(AtomicCommitConfig)


# instead of 'where', we have `shutil.which`

# def _access_check(fn, mode):
#     return os.path.exists(fn) and os.access(fn, mode) and not os.path.isdir(fn)


# from typing import Iterator


# def where(cmd, mode=os.F_OK | os.X_OK, path=None) -> Iterator[str]:
#     """Given a command, mode, and a PATH string, generate all paths which
#     conforms to the given mode on the PATH.

#     `mode` defaults to os.F_OK | os.X_OK. `path` defaults to the result
#     of os.environ.get("PATH"), or can be overridden with a custom search
#     path.

#     """
#     # If we're given a path with a directory part, look it up directly rather
#     # than referring to PATH directories. This includes checking relative to the
#     # current directory, e.g. ./script
#     if os.path.dirname(cmd):
#         if _access_check(cmd, mode):
#             return cmd
#         return None

#     use_bytes = isinstance(cmd, bytes)

#     if path is None:
#         path = os.environ.get("PATH", None)
#         if path is None:
#             try:
#                 path = os.confstr("CS_PATH")
#             except (AttributeError, ValueError):
#                 # os.confstr() or CS_PATH is not available
#                 path = os.defpath
#         # bpo-35755: Don't use os.defpath if the PATH environment variable is
#         # set to an empty string

#     # PATH='' doesn't match, whereas PATH=':' looks in the current directory
#     if not path:
#         return None

#     if use_bytes:
#         path = os.fsencode(path)
#         path = path.split(os.fsencode(os.pathsep))
#     else:
#         path = os.fsdecode(path)
#         path = path.split(os.pathsep)

#     if sys.platform == "win32":
#         # The current directory takes precedence on Windows.
#         curdir = os.curdir
#         if use_bytes:
#             curdir = os.fsencode(curdir)
#         if curdir not in path:
#             path.insert(0, curdir)

#         # PATHEXT is necessary to check on Windows.
#         pathext_source = os.getenv("PATHEXT") or _WIN_DEFAULT_PATHEXT
#         pathext = [ext for ext in pathext_source.split(os.pathsep) if ext]

#         if use_bytes:
#             pathext = [os.fsencode(ext) for ext in pathext]
#         # See if the given file matches any of the expected path extensions.
#         # This will allow us to short circuit when given "python.exe".
#         # If it does match, only test that one, otherwise we have to try
#         # others.
#         if any(cmd.lower().endswith(ext.lower()) for ext in pathext):
#             files = [cmd]
#         else:
#             files = [cmd + ext for ext in pathext]
#     else:
#         # On other platforms you don't have things like PATHEXT to tell you
#         # what file suffixes are executable, so just pass on cmd as-is.
#         files = [cmd]

#     seen = set()
#     for dir in path:
#         normdir = os.path.normcase(dir)
#         if not normdir in seen:
#             seen.add(normdir)
#             for thefile in files:
#                 name = os.path.join(dir, thefile)
#                 if _access_check(name, mode):
#                     yield name


# for path in where('git'): # multiple git now.
#   logger_print(path)

# use rclone instead?
REQUIRED_BINARIES = [RCLONE := "rclone", GIT := "git"]
# REQUIRED_BINARIES = ["bash", "timemachine", "rsync", "git"]
# if on windows, we check if bash is not coming from wsl.
# WSL_BASH = ...

for reqbin in REQUIRED_BINARIES:
    assert (
        shutil.which(reqbin) is not None
    ), f"Required binary '{reqbin}' is not in PATH."

# import pytz
# import datetime

# TIMEZONE = ...

FSCK = f"{GIT} fsck"
LOG_HASH = f'{GIT} log -1 --format=format:"%H"'
REV_PARSE_HASH = f"{GIT} rev-parse HEAD"

GITIGNORE = ".gitignore"
GITIGNORE_INPROGRESS = ".inprogress_gitignore"
GITDIR = ".git"
COMMIT_FLAG = ".atomic_commit_flag"
LOCKFILE = ".atomic_commit_lock"
LOCK_TIMEOUT = 5
BACKUP_BASE_DIR = ".git_backup"
BACKUP_GIT_DIR = os.path.join(BACKUP_BASE_DIR, GITDIR)
BACKUP_FLAG = os.path.join(BACKUP_BASE_DIR, ".atomic_backup_flag")
INPROGRESS_DIR = os.path.join(BACKUP_BASE_DIR, ".inprogress")
# INPROGRESS_INCREMENTAL_DIR = os.path.join(BACKUP_BASE_DIR, ".inprogress_incremental")
# INCREMENTAL_BACKUP_DIR_FORMAT = ...
# INCREMENTAL_BACKUP_DIR_GENERATOR = lambda: ...
LOG_DIR = "logs"
IGNORED_PATHS = [LOG_DIR, BACKUP_BASE_DIR, COMMIT_FLAG, LOCKFILE, GITIGNORE_INPROGRESS]
GIT_RM_CACHED_CMDGEN = lambda p: f"{GIT} rm -r --cached {p}"


def git_fsck():
    exit_code = os.system(FSCK)
    success = exit_code == 0
    logger_print(f"git fsck {'success' if success else 'failed'}")
    return success


from contextlib import contextmanager


@contextmanager
def chdir_context(dirpath: str):
    cwd = os.getcwd()
    os.chdir(dirpath)
    try:
        yield
    finally:
        os.chdir(cwd)


if config.INSTALL_DIR is not "":
    if os.path.exists(config.INSTALL_DIR):
        with chdir_context(config.INSTALL_DIR):
            assert os.path.isdir(GITDIR), "Git directory not found!"
            success = git_fsck()
            if not success:
                raise Exception("Target git repository is corrupted.")

        localfiles = os.listdir(".")
        target_dir_files = os.listdir(config.INSTALL_DIR)
        install_files = [f for f in localfiles if f.endswith(".py")]
        conflict_files = [f for f in install_files if f in target_dir_files]
        if set(conflict_files) == set(install_files):
            raise Exception(
                "You probably have installed at directory %s" % config.INSTALL_DIR
            )
        if conflict_files != []:
            err = [
                f"Conflict file '{f}' found in target directory '{config.INSTALL_DIR}'"
                for f in conflict_files
            ]
            raise Exception("\n".join(err))
        for f in install_files:
            target_fpath = os.path.join(config.INSTALL_DIR, f)
            shutil.copy(f, target_fpath)
        logger_print(f"Atomic commit script installed at: '{config.INSTALL_DIR}'")
    else:
        raise Exception(
            f"Could not find installation directory at '{config.INSTALL_DIR}'"
        )
    exit(0)

assert os.path.isdir(GITDIR), "Git directory not found!"
if os.path.exists(BACKUP_BASE_DIR):
    if not os.path.isdir(BACKUP_BASE_DIR):
        raise Exception(
            f"Backup base directory path '{BACKUP_BASE_DIR}' is not a directory."
        )
else:
    os.mkdir(BACKUP_BASE_DIR)

gitignore_content = ""
existing_ignored_paths = []
if os.path.exists(GITIGNORE):
    if os.path.isfile(GITIGNORE):
        with open(GITIGNORE, "r") as f:
            gitignore_content = f.read()
            existing_ignored_paths = gitignore_content.split("\n")
            existing_ignored_paths = [t.strip() for t in existing_ignored_paths]
            existing_ignored_paths = [t for t in existing_ignored_paths if len(t) > 0]

line = lambda s: f"{s.strip()}\n"
missing_ignored_paths = []

for p in IGNORED_PATHS:
    if p not in existing_ignored_paths:
        missing_ignored_paths.append(p)
        cmd = GIT_RM_CACHED_CMDGEN(p)
        ret = os.system(cmd)
        assert ret in [0, 128], f"error while removing path '{p}' from git cache"

if missing_ignored_paths != []:
    with open(GITIGNORE_INPROGRESS, "w+") as f:
        if gitignore_content != "":
            f.write(line(gitignore_content))
        for p in existing_ignored_paths + missing_ignored_paths:
            f.write(line(p))
    shutil.move(GITIGNORE_INPROGRESS, GITIGNORE)


import subprocess


def get_git_head_hash():
    if config.GIT_HEAD_HASH_ACQUISITION_MODE == GitHeadHashAcquisitionMode.log:
        cmd = LOG_HASH
    else:
        cmd = REV_PARSE_HASH

    proc = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
    assert (
        code := proc.returncode
    ) == 0, f"Checking lastest commit hash failed with exit code {code}."
    _hash = proc.stdout.strip().decode("utf8")
    return _hash


# you may find usable bash shell next to our git executable on windows, and it is preferred
# because wsl bash sucks


def get_script_path_and_exec_cmd(script_prefix):
    """
    Get the script path and the command to execute the script.

    Args:
        script_prefix (str): The prefix of the script name.

    Returns:
        tuple: A tuple containing the script path (str) and the command to execute the script (str).
    """
    script_path = f"{script_prefix}.py"
    exec_prefix = sys.executable
    if not os.path.exists(script_path):
        if os.name == "nt":
            script_suffix = "cmd"
            exec_prefix = "cmd /C"
        else:
            script_suffix = "sh"
            exec_prefix = "bash"
        script_path = f"{script_prefix}.{script_suffix}"
        assert os.path.exists(
            script_path
        ), f"failed to find os native implementation of commit script: {script_path}"
    else:
        logger_print(f"using os independent implementation of commit: '{script_path}'")

    cmd = f"{exec_prefix} {script_path}"
    return script_path, cmd


# deadlock: if both backup integrity & fsck failed, what to do?
# when backup is done, put head hash as marker
# default skip check: mod-time & size
rclone_flags = " " + config.RCLONE_FLAGS if config.RCLONE_FLAGS != "" else ""
BACKUP_COMMAND_COMMON = f"{RCLONE} sync {GITDIR} {INPROGRESS_DIR}" + rclone_flags

ROLLBACK_COMMAND = f"{RCLONE} sync {BACKUP_GIT_DIR} {GITDIR}" + rclone_flags

# if config.BACKUP_MODE == BackupMode.last_time_only:
BACKUP_COMMAND_GEN = lambda: BACKUP_COMMAND_COMMON
# else:
#     # take care of last backup!
#     BACKUP_COMMAND_GEN = (
#         lambda: f"{BACKUP_COMMAND_COMMON} '--backup-dir={INPROGRESS_INCREMENTAL_BACKUP_DIR}'"
#     )


def backup():
    if os.path.exists(BACKUP_GIT_DIR):
        shutil.move(BACKUP_GIT_DIR, INPROGRESS_DIR)
    backup_command = BACKUP_COMMAND_GEN()
    ret = os.system(backup_command)
    success = ret == 0
    assert success, f"Backup command failed with exit code {ret}"
    # then we move folders into places.
    shutil.move(INPROGRESS_DIR, BACKUP_GIT_DIR)
    # if config.BACKUP_MODE == BackupMode.incremental:
    #     incremental_backup_dir = INCREMENTAL_BACKUP_DIR_GENERATOR()
    #     shutil.move(INPROGRESS_INCREMENTAL_BACKUP_DIR, incremental_backup_dir)
    # create backup flag.
    if (
        config.BACKUP_UPDATE_CHECK_MODE
        == BackupUpdateCheckMode.commit_and_backup_flag_metadata
    ):
        pathlib.Path(BACKUP_FLAG).touch()
        # use os.path.getmtime(BACKUP_FLAG) to get the latest timestamp
    else:  # write git hash to flag.
        with open(BACKUP_FLAG, "w+") as f:
            git_hash = get_git_head_hash()
            f.write(git_hash)
    return success


def get_last_backup_commit_hash():
    _hash = None
    if os.path.isfile(BACKUP_FLAG):
        with open(BACKUP_FLAG, "r") as f:
            _hash = f.read().strip()
    return _hash


INF = 1e20
from typing import Optional


def get_file_mtime_with_default(fpath: str, default: Optional[float] = None):
    if os.path.exists(fpath):
        if os.path.isfile(fpath):
            return os.path.getmtime(fpath)
        else:
            raise Exception(
                "Cannot get mtime of file '%s' because non-file object is taking place of it."
                % fpath
            )
    else:
        if default is not None:
            return default
        else:
            raise Exception(
                "Cannot get mtime of file '%s' because it does not exist and default mtime is not set."
                % fpath
            )


def atomic_backup():
    """
    atomic backup:

    assumed passed fsck

    1. inprogress check: if has .inprogress folder, just continue backup
    2. backup integrity check: check if marker equals to git head/status. if not, then backup.
    """
    need_backup = False
    success = False

    if os.path.exists(INPROGRESS_DIR):
        need_backup = True
    else:
        if config.BACKUP_UPDATE_CHECK_MODE == BackupUpdateCheckMode.git_commit_hash:
            last_backup_commit_hash = get_last_backup_commit_hash()
            current_commit_hash = get_git_head_hash()
            if current_commit_hash != last_backup_commit_hash:
                need_backup = True
        else:
            # compare mtime.
            mtime_backup_flag = get_file_mtime_with_default(BACKUP_FLAG, default=-INF)
            mtime_commit_flag = get_file_mtime_with_default(COMMIT_FLAG, default=INF)
            if mtime_commit_flag > mtime_backup_flag:
                need_backup = True

    if need_backup:
        success = backup()
    else:
        success = True
    return success


#####################################
# RCLONE BACKUP RESTORATION DIAGRAM #
#####################################
#
# time
#  |   current   | back_0 | back_1 | back_2 |  state   |
#  |-------------|--------|--------|--------|----------|
# 0| a b c       |  *     |  *     |        | *a *b *c |
# 1|       +d    |        |        |     *  | a b c *d |
# 2|     -c      |  c     |        |        |  a b d   |
# 3|   +b+c      |        |  b     |        | a *b d *c|
# 4|       -d    |        |        |     d  |  a b    c|
#
# unless you make modification records with timestamp per state, you cannot restore every state.
# given its complexity, let's not do it.
#


def rollback():
    # do we have incomplete backup? if so, we cannot rollback.
    success = False
    incomplete = os.path.exists(INPROGRESS_DIR)
    if incomplete:
        raise Exception("Backup is incomplete. Cannot rollback.")
    else:
        return_code = os.system(ROLLBACK_COMMAND)
        assert (
            return_code == 0
        ), f"Running rollback command failed with exit code {return_code}"
        # if config.BACKUP_MODE == BackupMode.incremental:
        # ...  # group files based on modification time, or `--min-age`
        # # selected files in main dir along with files from backup dir
        git_not_corrupted = git_fsck()
        success = git_not_corrupted
    return success


_, COMMIT_CMD = get_script_path_and_exec_cmd("commit")


def commit():
    success = False
    return_code = os.system(COMMIT_CMD)
    assert (
        return_code == 0
    ), f"Failed to execute commit script with exit code {return_code}"
    success = True
    return success


# TODO: formulate this into a state machine.
def atomic_commit():
    r"""
      fsck 
    /      \
  succ     fail
      \     | rollback (most recent backup)
  d_comm > d_back? # can be replaced by metadata check or `git rev-parse HEAD` (equivalent to: `git log -1 --format=format:"%H"` alongside metadata check with depth=1 (if possible to retrieve from timemachine current backup)
      | y     | n
    backup (atomic) & update d_back nothing
      \       /
      commit
          |
        fsck
    succ/  \fail
        |    | rollback (most recent backup) & exit
    update d_comm
      | backup (atomic)
      | update d_back
      | exit
  """
    success = False
    commit_success = False
    can_commit = atomic_commit_common()

    if can_commit:
        hash_before = get_git_head_hash()
        commit_success = commit()
        hash_after = get_git_head_hash()
        commit_hash_changed = hash_after != hash_before
        if commit_success:
            if commit_hash_changed:
                pathlib.Path(COMMIT_FLAG).touch()
        else:
            return success

    finalize_commit_success = atomic_commit_common()
    if finalize_commit_success:
        success = True

    return success


def atomic_commit_common():
    git_not_corrupted = False
    can_commit = False
    git_not_corrupted = git_fsck()

    if not git_not_corrupted:
        if rollback():
            can_commit = True
    else:
        if atomic_backup():
            can_commit = True
    return can_commit


if __name__ == "__main__":
    with filelock.FileLock(LOCKFILE, timeout=LOCK_TIMEOUT) as lockfile:
        success = atomic_commit()
        if not success:
            raise Exception("Failed to perform atomic commit.")
