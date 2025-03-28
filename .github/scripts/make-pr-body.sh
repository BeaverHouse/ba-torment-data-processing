#!/bin/bash

BRANCH=$1

ISSUE_NUMBER=$(echo "$BRANCH" | grep -o '^[0-9]*')

# Get the commits with message between main and the branch
# If fails, retry with origin/master
BASE_BRANCH="main"
COMMITS=$(git log --oneline origin/$BASE_BRANCH..$BRANCH)
if [ -z "$COMMITS" ]; then
    echo "Failed to get commits between origin/$BASE_BRANCH and $BRANCH, retry with origin/master"
    BASE_BRANCH="master"
    COMMITS=$(git log --oneline origin/$BASE_BRANCH..$BRANCH)
fi

# Extract external links from commit messages
# Remove Korean text after URLs
EXTERNAL_LINKS=$(git log --reverse --pretty=format:"%b" $BASE_BRANCH..$BRANCH | \
    grep -o 'https\?://[^[:space:]]*' | \
    perl -CSD -pe 's/[\x{AC00}-\x{D7A3}].*$//g' | \
    grep -v '^$' | \
    sort -u)

# Write the body of the PR
# 1. Body based on commit history
#    - The latest commit is at the bottom.
#    - The format contains the commit title and description.
#    - Skip empty commit messages
COMMIT_BODY=$(git log --reverse --pretty=format:"TITLE:%s%nBODY:%b%nEND" $BASE_BRANCH..$BRANCH | \
    awk '
    BEGIN { title = ""; body = ""; in_body = 0; first_line = 1 }
    /^TITLE:/ { 
        if (title != "") {
            print "- " title
            if (body != "") {
                print "    - " body
                body = ""
            }
        }
        title = substr($0, 7)
        in_body = 0
        first_line = 1
        next
    }
    /^BODY:/ { 
        in_body = 1
        if ($0 != "BODY:") {
            body = substr($0, 6)
        }
        next
    }
    /^END/ {
        if (title != "") {
            print "- " title
            if (body != "") {
                print "    - " body
                body = ""
            }
        }
        title = ""
        in_body = 0
        first_line = 1
        next
    }
    in_body == 1 && NF > 0 {
        if (body == "") {
            body = $0
        } else {
            body = body "\n      " $0
        }
    }')

BODY=$(cat <<-END
## What changed on this pull request
$COMMIT_BODY

### Reference

#$ISSUE_NUMBER
END
)

# Add external links if any
if [ ! -z "$EXTERNAL_LINKS" ]; then
    BODY="$BODY"$'\n'"$EXTERNAL_LINKS"
fi

echo "Body: "
echo "$BODY"
