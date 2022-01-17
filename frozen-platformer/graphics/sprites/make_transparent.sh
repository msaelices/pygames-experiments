# Example: convert colors close to "#ec5c64" to transparent
# ./make_transparent.sh player/idle_0.png "#ec5c64"

convert "$1" -fuzz 10% -transparent "$2" "$1"
