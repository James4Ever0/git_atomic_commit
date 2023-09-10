import os
import sys

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
#                                                      / n nothing - commit
# fsck - succ -          d_comm > d_back? - y backup  /
#      - fail - rollback /

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
 d_comm > d_back? # can be replaced by metadata check
    | y     |n
  backup (atomic) & update d_back nothing
    \       /
    commit
        |
      fsck
   succ/  \fail
      |    |rollback (most recent backup) & exit
   update d_comm
    | backup (atomic)
    | update d_back
    | exit
"""
