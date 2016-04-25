#!/usr/bin/env bash
BRANCH=master
TARGET_REPO=zonca/zonca.github.io.git
PELICAN_OUTPUT_FOLDER=output

echo -e "Testing travis-encrypt"
echo ${GH_TOKEN}
echo ${GH_PASSWD}

git push -fq https://${GH_TOKEN}@github.com/${GH_OWNER}/${GH_PROJECT_NAME} master