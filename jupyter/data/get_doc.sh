#!/bin/bash

for ((i=1 ; i<1131 ; i++))
do
	num=${i}
	file=./html/anzen_${num}.html

	echo ${num}
        wget https://anzeninfo.mhlw.go.jp/anzen_pg/SAI_DET.aspx?joho_no=${num} -O ${file}
done

for ((i=100003 ; i<101583 ; i++))
do
	num=${i}
	file=./html/anzen_${num}.html

	echo ${num}
        wget https://anzeninfo.mhlw.go.jp/anzen_pg/SAI_DET.aspx?joho_no=${num} -O ${file}
done

for ((i=3 ; i<30 ; i++))
do
        num=${i}
        if [ ${i} -lt 10 ]; then
                num=0${i}
        fi

        file=sibou_db_h${num}.xlsx

        if [ ${i} -lt 27 ]; then
          file=sibou_db_h${num}.xls
        fi

        echo ${file}
        wget https://anzeninfo.mhlw.go.jp/anzen/sib_xls/${file} -P ./excel/
done

wget https://anzeninfo.mhlw.go.jp/anzen/sai/kikaisaigai_db28.xlsx -P ./excel/
