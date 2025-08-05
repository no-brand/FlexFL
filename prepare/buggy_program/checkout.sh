CURRENT_PATH=$(readlink -f "$0")         # 현재 실행 파일의 절대 경로 (/mnt/c/development/repo/FlexFL/prepare/buggy_program/checkout.sh)
CURRENT_DIR=$(dirname "$CURRENT_PATH")   # 현재 실행 파일의 디렉토리 (/mnt/c/development/repo/FlexFL/prepare/buggy_program)

TOOL_DIR=$(cd $CURRENT_DIR; cd ..; cd ..; pwd)/tools  # 툴 디렉토리 (/mnt/c/development/repo/FlexFL/tools)
export D4J_HOME=$TOOL_DIR/defects4j                   # defects4j 홈 디렉토리 (/mnt/c/development/repo/FlexFL/tools/defects4j-2.0.0)
REPO_DIR=$CURRENT_DIR/Collect_Methods/repos           # 리파지토리 checkout 디렉토리 (/mnt/c/development/repo/FlexFL/prepare/buggy_program/Collect_Methods/repos)

cat "./bug_list.txt" | while read bug
do
    project=${bug%-*}                           # -* Prefix (Time)
    bugid=${bug#*-}                             # -* Suffix (25)
    checkout_dir=$REPO_DIR/${project}-${bugid}  # Checkout 경로 (/mnt/c/development/repo/FlexFL/prepare/buggy_program/Collect_Methods/repos/Time-25)
    echo $project-$bugid                        # Time-25

    # Checking out 552be4b6 to /mnt/c/development/repo/FlexFL/prepare/buggy_progr OK
    # Init local repository...................................................... OK
    # Tag post-fix revision...................................................... OK
    # Fix broken build........................................................... OK
    # Run post-checkout hook..................................................... OK
    # Excluding broken/flaky tests............................................... OK
    # Excluding broken/flaky tests............................................... OK
    # Excluding broken/flaky tests............................................... OK
    # Initialize fixed program version........................................... OK
    # Apply patch................................................................ OK
    # Initialize buggy program version........................................... OK
    # Diff 552be4b6:c7a581e5..................................................... OK
    # Apply patch................................................................ OK
    # Tag pre-fix revision....................................................... OK
    # Check out program version: Time-25b........................................ OK
    rm -rf "${checkout_dir}_buggy"; mkdir -p "${checkout_dir}_buggy"
    "$D4J_HOME/framework/bin/defects4j" checkout -p "$project" -v "${bugid}b" -w "${checkout_dir}_buggy"

    # Checking out 552be4b6 to /mnt/c/development/repo/FlexFL/prepare/buggy_progr OK
    # Init local repository...................................................... OK
    # Tag post-fix revision...................................................... OK
    # Fix broken build........................................................... OK
    # Run post-checkout hook..................................................... OK
    # Excluding broken/flaky tests............................................... OK
    # Excluding broken/flaky tests............................................... OK
    # Excluding broken/flaky tests............................................... OK
    # Initialize fixed program version........................................... OK
    # Apply patch................................................................ OK
    # Initialize buggy program version........................................... OK
    # Diff 552be4b6:c7a581e5..................................................... OK
    # Apply patch................................................................ OK
    # Tag pre-fix revision....................................................... OK
    # Check out program version: Time-25f........................................ OK    
    rm -rf "${checkout_dir}_fixed"; mkdir -p "${checkout_dir}_fixed"
    "$D4J_HOME/framework/bin/defects4j" checkout -p "$project" -v "${bugid}f" -w "${checkout_dir}_fixed"
done