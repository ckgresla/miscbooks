# Rename all *.txt to *.text
for f in *.webp; do 
    mv -- "$f" "${f%.webp}.jpg"
done
