if [ $# != 6 ]; then
  echo "引数の数が間違っています！"
  echo "(例) ./distributor.sh v_type v_num distance speed pj pe"
  exit 1
fi

v_type=$1
v_num=$2
distance=$3
speed=$4
pj=$5
pe=$6

echo "========================================"

if [ ${v_type} = "C" ]; then
  if [ ${v_num} -eq 1 ]; then
    ./putJson.sh ${distance} ${speed} ${pj} ${pe} "2077"
  elif [ ${v_num} -eq 2 ]; then
    ./putJson.sh ${distance} ${speed} ${pj} ${pe} "2078"
  fi
elif [ ${v_type} = "B" ]; then
  if [ ${v_num} -eq 4 ]; then
    ./putJson.sh ${distance} ${speed} ${pj} ${pe} "2079"
  #elif [ ${v_num} -eq 2 ]; then
    #./putJson.sh ${distance} ${speed} ${pj} ${pe} "2084"
  fi
fi

echo "\n========================================"
