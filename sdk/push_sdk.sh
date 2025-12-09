#!/bin/sh

version_type=$1

# Update package version
version=$(npm version $version_type --no-git-tag-version)

# Commit changes
# git add .
# git commit -m "Update SDK to version $version"

# Push changes
# git push
npm publish