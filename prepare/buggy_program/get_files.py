import os
import subprocess as sp
import glob


def d4j_path_prefix(proj, bug_num):
    bug_num = int(bug_num)
    if proj == "Chart":
        return "source/"
    elif proj == "Closure":
        return "src/"
    elif proj == "Lang":
        if bug_num <= 35:
            return "src/main/java/"
        else:
            return "src/java/"
    elif proj == "Math":
        if bug_num <= 84:
            return "src/main/java/"
        else:
            return "src/java/"
    elif proj == "Mockito":
        return "src/"
    elif proj == "Time":
        return "src/main/java/"
    elif proj == "Cli":
        if bug_num <= 29:
            return "src/java/"
        else:
            return "src/main/java/"
    elif proj == "Codec":
        if bug_num <= 10:
            return "src/java/"
        else:
            return "src/main/java/"
    elif proj == "Collections":
        return "src/main/java/"
    elif proj == "Compress":
        return "src/main/java/"
    elif proj == "Csv":
        return "src/main/java/"
    elif proj == "Gson":
        return "gson/src/main/java/"
    elif proj in ("JacksonCore", "JacksonDatabind", "JacksonXml"):
        return "src/main/java/"
    elif proj == "Jsoup":
        return "src/main/java/"
    elif proj == "JxPath":
        return "src/java/"
    else:
        raise ValueError(f"Unrecognized project {proj}")


with open("./bug_list.txt") as f:
    bugs = [e.strip() for e in f.readlines()]
for bug in bugs:
    # 코드베이스에서 소스 경로를 설정 - 프로젝트 단위로 (./Collect_Methods/repos/Time-25_buggy/src/main/java/)
    folder_path = f"./Collect_Methods/repos/{bug}_buggy/{d4j_path_prefix(bug.split('-')[0],bug.split('-')[1])}"

    file_list = []
    for root, dirs, files in os.walk(folder_path):
        # 구현체(.java) 가 나올때까지 안으로 탑색색
        # root  : 현재 헤드 (./Collect_Methods/repos/Time-25_buggy/src/main/java/org/joda/time)
        # dirs  : 현재 경로에서의 폴더/패키지들 (['base', 'chrono', 'convert', 'field', 'format', 'tz'])
        # files : 현재 경로에서의 파일들 (['Chronology.java', 'DateMidnight.java', 'DateTime.java', ... ])
        for file in files:
            # .java 아니면 생략
            if not file.endswith(".java"):
                continue

            # 경로를 변경 (Collect_Methods 를 경로상에서 삭제)
            file_path = os.path.join(root, file)
            file_path = "/".join([file_path.split("/")[0]] + file_path.split("/")[2:])
            file_list.append(file_path)

    # 모든 java 파일을 나열하는 행위
    # ./repos/Time-25_buggy/src/main/java/org/joda/time/ReadWritableInterval.java
    # ./repos/Time-25_buggy/src/main/java/org/joda/time/ReadablePeriod.java
    # ./repos/Time-25_buggy/src/main/java/org/joda/time/ReadableDuration.java
    with open(f"./file_lists_buggy/{bug}.txt", "w") as f:
        for file in file_list:
            f.writelines(file + "\n")

    folder_path = f"./Collect_Methods/repos/{bug}_fixed/{d4j_path_prefix(bug.split('-')[0],bug.split('-')[1])}"
    file_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if not file.endswith(".java"):
                continue
            file_path = os.path.join(root, file)
            file_path = "/".join([file_path.split("/")[0]] + file_path.split("/")[2:])
            file_list.append(file_path)
    with open(f"./file_lists_fixed/{bug}.txt", "w") as f:
        for file in file_list:
            f.writelines(file + "\n")
