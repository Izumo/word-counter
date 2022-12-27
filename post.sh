#curl -X POST -H 'Content-Type: text/plain' --data-binary @post.sh http://localhost:8000/CountWords
curl -X POST -H 'Content-Type: text/plain' --data-binary @/usr/share/doc/file/README http://localhost:8000/CountWords
