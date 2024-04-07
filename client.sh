#! /bin/sh
user=$(jq .username config.json -r)
password=$(jq .password config.json -r)
ip=$(jq .server_ip config.json -r)
port=$(jq .port config.json -r)
file=$(jq .file config.json -r)


sleep 1

while true; do
    curl -u "${user}:${password}" -O "ftp://${ip}:${port}/${file}" 2>&1 | tr '\r' '\n'
    rm "./${file}"
done

