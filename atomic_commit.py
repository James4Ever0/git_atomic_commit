import os
import sys

# import shutil

# instead of 'where', we have `shutil.which`


def _access_check(fn, mode):
    return os.path.exists(fn) and os.access(fn, mode) and not os.path.isdir(fn)


from typing import Iterator


def where(cmd, mode=os.F_OK | os.X_OK, path=None) -> Iterator[str]:
    """Given a command, mode, and a PATH string, generate all paths which
    conforms to the given mode on the PATH.

    `mode` defaults to os.F_OK | os.X_OK. `path` defaults to the result
    of os.environ.get("PATH"), or can be overridden with a custom search
    path.

    """
    # If we're given a path with a directory part, look it up directly rather
    # than referring to PATH directories. This includes checking relative to the
    # current directory, e.g. ./script
    if os.path.dirname(cmd):
        if _access_check(cmd, mode):
            return cmd
        return None

    use_bytes = isinstance(cmd, bytes)

    if path is None:
        path = os.environ.get("PATH", None)
        if path is None:
            try:
                path = os.confstr("CS_PATH")
            except (AttributeError, ValueError):
                # os.confstr() or CS_PATH is not available
                path = os.defpath
        # bpo-35755: Don't use os.defpath if the PATH environment variable is
        # set to an empty string

    # PATH='' doesn't match, whereas PATH=':' looks in the current directory
    if not path:
        return None

    if use_bytes:
        path = os.fsencode(path)
        path = path.split(os.fsencode(os.pathsep))
    else:
        path = os.fsdecode(path)
        path = path.split(os.pathsep)

    if sys.platform == "win32":
        # The current directory takes precedence on Windows.
        curdir = os.curdir
        if use_bytes:
            curdir = os.fsencode(curdir)
        if curdir not in path:
            path.insert(0, curdir)

        # PATHEXT is necessary to check on Windows.
        pathext_source = os.getenv("PATHEXT") or _WIN_DEFAULT_PATHEXT
        pathext = [ext for ext in pathext_source.split(os.pathsep) if ext]

        if use_bytes:
            pathext = [os.fsencode(ext) for ext in pathext]
        # See if the given file matches any of the expected path extensions.
        # This will allow us to short circuit when given "python.exe".
        # If it does match, only test that one, otherwise we have to try
        # others.
        if any(cmd.lower().endswith(ext.lower()) for ext in pathext):
            files = [cmd]
        else:
            files = [cmd + ext for ext in pathext]
    else:
        # On other platforms you don't have things like PATHEXT to tell you
        # what file suffixes are executable, so just pass on cmd as-is.
        files = [cmd]

    seen = set()
    for dir in path:
        normdir = os.path.normcase(dir)
        if not normdir in seen:
            seen.add(normdir)
            for thefile in files:
                name = os.path.join(dir, thefile)
                if _access_check(name, mode):
                    yield name


# for path in where('git'): # multiple git now.
#   print(path)


REQUIRED_BINARIES = ["bash", "timemachine", "rsync", "git"]
# if on windows, we check if bash is not coming from wsl.
FSCK = "git fsck"

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

    cmd = f"{exec_prefix} {script_path}"
    return script_path, cmd


# deadlock: if both backup integrity & fsck failed, what to do?
# when backup is done, put head hash as marker

r"""
atomic backup:

assumed passed fsck

1. inprogress check: if has .inprogress folder, just continue backup
2. backup integrity check: check if marker equals to git head/status. if not, then backup.

"""
r"""
     fsck 
   /      \
 succ     fail
     \     | rollback (most recent backup)
 d_comm > d_back? # can be replaced by metadata check or `git rev-ref HEAD` alongside metadata check with depth=1 (if possible to retrieve from timemachine current backup)
    | y     |n
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
