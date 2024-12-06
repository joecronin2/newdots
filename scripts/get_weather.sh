curl "https://api.open-meteo.com/v1/forecast?latitude=52.3569&longitude=4.8008&current=temperature_2m,precipitation,cloud_cover" \
	| jq -r '.current | [.temperature_2m, .precipitation, .cloud_cover] | @tsv' \
	| awk '{printf " %s󰔄   %s  %s\n", $1, $2, $3}' \

# @tsv to use \t instead of \n
