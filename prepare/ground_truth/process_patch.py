import json
import subprocess as sp
with open('./bug_list.txt') as f:
    bugs = [e.strip() for e in f.readlines()]
with open('./patch.json') as f:
    patch_buggy = json.load(f)
res = {}
for bug in bugs:
    print(bug)
    project, bugid = bug.split('-')
    file = f'../../tools/defects4j/framework/projects/{project}/patches/{bugid}.src.patch'
    with open(file) as f:
        patch = f.read()
    edit_buggy = {}
    edit_fix = {}
    for diff in patch.split('diff --git'):
        # diff --git 구분으로 생긴 빈 문자열은 제거
        if diff.strip() == '':
            continue
        a_file = None
        b_file = None
        for line in diff.split('\n'):
            # --- a/src/main/java/org/joda/time/Partial.java -> a_file = /src/main/java/org/joda/time/Partial.java
            # +++ b/src/main/java/org/joda/time/Partial.java -> b_file = /src/main/java/org/joda/time/Partial.java (동일)
            if line.startswith('--- a'):
                a_file = line.lstrip('--- a').strip()
            elif line.startswith('+++ b'):
                b_file = line.lstrip('+++ b')
            elif line.startswith('--- '):
                a_file = line.lstrip('--- ').split()[0]
            elif line.startswith('+++ '):
                b_file = line.lstrip('+++ ').split()[0]
        # 파일이 java 가 아니면 생략        
        if a_file and not a_file.endswith('java') or b_file and not b_file.endswith('java'):
            continue
        if a_file!=b_file:
            if (a_file and patch_buggy[bug] == 'b') or (b_file and patch_buggy[bug] == 'a'):
                continue
        assert(a_file==b_file)

        lines = diff.split('\n')
        a_lines = []
        b_lines = []
        for i in range(len(lines)):
            if lines[i].startswith('@@'):
                # @@ -214,20 +214,11 @@ public final class Partial
                # a_start = 214
                # b_start = 214
                assert(lines[i].split()[0]=='@@')
                assert(lines[i].split()[3]=='@@')
                a_start = int(lines[i].split()[1].split(',')[0][1:])  # +,- 부호도 제거
                b_start = int(lines[i].split()[2].split(',')[0][1:])  # +,- 부호도 제거
                a_index = 0
                b_index = 0
                for j in range(len(lines)-i-1):
                    if lines[i+1+j].startswith('-'):
                        a_lines.append(a_start + a_index)
                        a_index += 1
                    elif lines[i+1+j].startswith('+'):
                        b_lines.append(b_start + b_index)
                        b_index += 1
                    elif lines[i+1+j].startswith('@@'):
                        break
                    else:
                        if lines[i+1+j].startswith('\ No newline at end of file'):
                            continue
                        a_index += 1
                        b_index += 1
        if patch_buggy[bug] == 'a':
            edit_buggy[a_file] = a_lines
            edit_fix[b_file] = b_lines
        else:
            edit_buggy[b_file] = b_lines
            edit_fix[a_file] = a_lines
    with open(f'./edit_Defects4j/{bug}.json', 'w') as f:
        json.dump({
           "buggy" : edit_buggy,
           "fixed": edit_fix
        }, f, indent=4)