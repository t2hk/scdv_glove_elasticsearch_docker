import re, json, glob, os.path, sys
from bs4 import BeautifulSoup

args = sys.argv
html_dir = args[1]
json_dir = args[2]

html_files = glob.glob(html_dir + "*")

for html_file in html_files:
    file_size = os.path.getsize(html_file)
    if file_size < 10000:
        print("[ERROR] {}".format(html_file))
        continue

    print(html_file)
    #json_file = html_file.replace("./html/", "./elastic_json/").replace(".html", ".json")
    json_file = html_file.replace(html_dir, json_dir).replace(".html", ".json")

    id = html_file.replace(html_dir + "anzen_","").replace(".html","")

    html = BeautifulSoup(open(html_file, encoding="cp932"), 'html.parser')

    for i in html.select("br"):
      i.replace_with("\n")

    title = html.find('table').find('h1').text.strip()
    title_id = id + '_t_0'

    _cause = html.find("img", alt="原因").find_parent().find_parent().find('td').text.strip().replace("\u3000", "").split("\n")
    cause = []

    for i, val in enumerate(_cause):
        val = val.strip().replace("\t","").replace("\n","")
        if len(val) > 0:
            cause.append('{"cause_id":"%s", "text":"%s"}' % (id + '_c_' + str(i), val))
    cause = ",".join(cause)

    situation = []
    _situation = html.find("img", alt="発生状況").find_parent().find_parent().find('td').text.strip().replace("\u3000", "").split("\n")
    for i, val in enumerate(_situation):
        val = val.strip().replace("\t","").replace("\n","")
        if len(val) > 0:
            situation.append('{"situation_id":"%s", "text":"%s"}' % (id + '_s_' + str(i), val))
    situation = ",".join(situation)

    _measures = html.find("img", alt="対策").find_parent().find_parent().find('td').text.strip().replace("\u3000", "").split("\n")
    measures = [] 
    for i, val in enumerate(_measures):
        val = val.strip().replace("\t","").replace("\n","")
        if len(val) > 0:
            measures.append('{"measures_id":"%s", "text":"%s"}' % (id + '_m_' + str(i), val))
    measures = ",".join(measures)

    json_data = '{"index":{"_index":"anzen","_id":"%s"}},\n{"title":{"title_id":"%s", "text":"%s"},"situation":[%s],"cause":[%s],"measures":[%s]}' % (id, title_id, title, situation, cause, measures)

    with open(json_file, "w") as jw:
        jw.writelines(json_data + "\n\n")
