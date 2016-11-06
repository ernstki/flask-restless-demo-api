# usage: source envvars.sh

USAGE='
Usage:  $ source path/to/envvars.sh
'

if [[ ! $0 =~ ^- ]]; then
    # if *run* as a script, instead of sourced:
    echo "$USAGE" 2>&1
    exit 1
fi

MYDIR=$( dirname "${BASH_SOURCE[0]}" )

export FLASK_APP=demoapi.py
