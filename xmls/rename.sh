#!/bin/bash

counter=1

for file in *.xml; do
    # Check if the file is a regular file
    if [ -f "$file" ]; then
        mv -- "$file" "abgabe_${counter}.xml"
        let counter++
    fi
done

let counter--
echo "$counter file(s) renamed"
