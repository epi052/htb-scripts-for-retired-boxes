#!/bin/bash

repo="magento-mirror"
styles_file="skin/frontend/default/default/css/styles.css"
target_hash="d9c659f7c70e070394eff4290a0a601a"

if [[ ! -d "${repo}" ]]; then
  git clone https://github.com/OpenMage/magento-mirror.git
fi

pushd "${repo}" >/dev/null || exit

for tag in $(git tag -l); do
  git checkout tags/"${tag}" 2>/dev/null

  if [[ ! -e "$(pwd)/${styles_file}" ]]; then
    continue
  fi

  ver_hash=$(md5sum "$(pwd)/${styles_file}" | awk '{print $1}')

  if [[ "${ver_hash}" == "${target_hash}" ]]; then
    echo "Found version: ${tag}"
  fi
done

popd >/dev/null || exit