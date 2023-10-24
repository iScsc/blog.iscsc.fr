TERM="xterm-256color"
#OFF=$(tput sgr0)
OFF=""
#RED=$(tput setaf 1)
RED=""

BUILD_FOLDER="./build/blog"

if [ -z "$(ls -A $BUILD_FOLDER 2>/dev/null)" ]; then
    echo "$RED[WARNING]$OFF '$BUILD_FOLDER' empty: nothing will be served by nginx server"
fi

nginx -g "daemon off;"
