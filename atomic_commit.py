import os
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