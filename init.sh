cd ./elasticsearch
mkdir es-data

wget https://object-storage.tyo2.conoha.io/v1/nc_2520839e1f9641b08211a5c85243124a/sudachi/sudachi-dictionary-20200127-full.zip

unzip sudachi-dictionary-20200127-full.zip

mv sudachi-dictionary-20200127/system_full.dic .

wget https://github.com/WorksApplications/elasticsearch-sudachi/releases/download/v7.5.0-1.3.2/analysis-sudachi-elasticsearch7.5-1.3.2.zip

