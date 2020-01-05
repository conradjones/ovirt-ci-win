#!/usr/bin/env bash

currentDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

gitlab-runner register -n \
    --url "${1}" \
    --registration-token "${2}" \
    --executor custom \
    --description "${3}" \
    --builds-dir "/builds" \
    --cache-dir "/cache" \
    --custom-run-exec "${currentDir}/run.sh" \
    --custom-prepare-exec "${currentDir}/prepare.sh" \
    --custom-cleanup-exec "${currentDir}/cleanup.sh" \
    --tag-list "${3}"