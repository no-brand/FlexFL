import json
import subprocess as sp
with open('./bug_list.txt') as f:
    bugs = [e.strip() for e in f.readlines()]
res = {}
for bug in bugs:
    # 수정(patch) 내역을 찾아서
    project, bugid = bug.split('-')
    file = f'../../tools/defects4j/framework/projects/{project}/patches/{bugid}.src.patch'
    with open(file) as f:
        patch = f.read()
    buggy_repos = f"../buggy_program/Collect_Methods/repos/{bug}_buggy"
    out = sp.run(f"git apply --check ../../../{file}".split(), stdout=sp.PIPE, stderr=sp.PIPE, cwd=buggy_repos)
    if len(out.stderr.decode()) != 0:
        res[bug] = 'b' # which means edition lines of 'b' in the patch belongs to the buggy version of the buggy program
    else:
        res[bug] = 'a'

# *.src.patch 를 이용해서 git apply --check 수행합니다.
# {
#     "Time-1": "b",
#     "Time-2": "b",
#     "Time-3": "b",
#     "Time-4": "b",
#     "Time-5": "b",
#     "Time-25": "b"
# }        
with open('./patch.json', 'w') as f:
    json.dump(res, f, indent=4)