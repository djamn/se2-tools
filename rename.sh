#!/bin/bash

counter=1

for file in *.xml; do
    # Skip files that already start with "abgabe_"
    if [[ "$file" =~ ^abgabe_.*\.xml$ ]]; then
        continue
    fi

    if [ -f "$file" ]; then
        mv -- "$file" "abgabe_${counter}.xml"
        let counter++
    fi
done

let counter--
echo "$counter file(s) renamed"
