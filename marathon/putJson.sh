if [ $# != 5 ]; then
  echo "引数の数が間違っています！"
  echo "(例) ./putJson.sh kyori speed pj pe destination"
  exit 1
fi

destination=$5

kyori=$1
scale_X=`echo "scale=1; (19.3*${kyori})/42.195" | bc`
place_jp=$3
place_en=$4
speed=$2
place_ot="Other"

json=$(cat << EOS
{"payload":{"scale_X":"${scale_X}","kyori":"${kyori}","place_jp":"${place_jp}","place_en":"${place_en}","place_ot":"${place_ot}","speed":"${speed}"}}
EOS
)

curl -X PUT "https://app.singular.live/apiv1/datanodes/"${destination}"/data" -H "Content-Type: application/json" --basic -u "ID:PW" -d ${json}

