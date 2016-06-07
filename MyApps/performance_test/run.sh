#URL="http://139.129.47.180:8002/Errand/"
URL="http://127.0.0.1:8000/Errand/"
COOKIE="csrftoken=VbHLGMwqYA9O6qNQnzCeRdgg9Yi5auwW; sessionid=5z2svhzx84dn8vjip4af2tvstx1xakna"
#GREP="grep -E 'Document Path|Complete requests|Failed requests|Requests per second|Time per request'"
NUMBER="100"
CONCURRENCY="10"

echo "$(ab -n 10 -c 10 -C "${COOKIE}" ${URL} | grep -E 'Document Path|Complete requests|Failed requests|Requests per second|Time per request'>> "res")"

OPT="register"
echo "$(ab -n 10000 -c 10 -p "${OPT}.post" -C "${COOKIE}" -T "application/x-www-form-urlencoded" ${URL}${OPT} | grep -E 'Document Path|Complete requests|Failed requests|Requests per second|Time per request'>> "res")"
#echo "$(ab -n 10 -c 10 http://139.129.47.180:8002/Errand/orderbyscores)"