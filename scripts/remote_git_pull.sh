#!/usr/bin/bash

PATH=$(/usr/bin/getconf PATH || /bin/kill $$)

die() {
	echo "[!] Something went wrong, exiting..."
	exit 1
}

echo "[+] Connected to iscsc.fr"

if [ $# -ne 1 ]; then
	echo "[!] Must provide one and only one argument: repo path on remote";
	die;
fi
REPO_PATH="$1"; shift

echo "[+] Change directory"
cd ${REPO_PATH} || die

REMOTE_URL="iscsc/blog.iscsc.fr"
REMOTE_NAME=$(git remote -v | grep --ignore-case "${REMOTE_URL}" | grep "(fetch)" | awk '{print $1}')
MAIN_BRANCH_NAME=main

echo "[+] iScsc remote name is '${REMOTE_NAME}'"
echo "[+] Fetch '${MAIN_BRANCH_NAME}' from '${REMOTE_NAME}'"
git fetch "${REMOTE_NAME}" "${MAIN_BRANCH_NAME}" || die

echo "[+] Checkout on '${MAIN_BRANCH_NAME}'"
git checkout "${MAIN_BRANCH_NAME}" || die

REMOTE_MAIN_REF_NAME="${REMOTE_NAME}/${MAIN_BRANCH_NAME}"

echo "[+] Remote ref is '${REMOTE_MAIN_REF_NAME}'"
echo "[+] Rebase on '${REMOTE_MAIN_REF_NAME}'"
git rebase "${REMOTE_MAIN_REF_NAME}" || die

echo "[+] git log from here:"
git log --color --decorate --oneline --max-count=20 main

