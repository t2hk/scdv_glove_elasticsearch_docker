import re, json, glob, os.path, sys
from bs4 import BeautifulSoup

args = sys.argv
html_dir = args[1]
csv_file = args[2]

html_files = glob.glob(html_dir + "*")
csv_header = '"doc_id","category","text_id","text"'

with open(csv_file, 'w') as w_csv:
  w_csv.writelines(csv_header + '\n')

  for html_file in html_files:
    csv_line = {}
    file_size = os.path.getsize(html_file)
    if file_size < 10000:
        print("[ERROR] {}".format(html_file))
        continue

    print(html_file)

    id = html_file.replace(html_dir + "anzen_","").replace(".html","")
    html = BeautifulSoup(open(html_file, encoding="cp932"), 'html.parser')

    for i in html.select("br"):
      i.replace_with("\n")

    # タイトルの処理
    title = html.find('table').find('h1').text.strip()
    title_id = id + '_t_00'

    w_csv.writelines('"{}","{}","{}","{}"\n'.format(id, "title", title_id, title))

    # 原因の処理
    cause = html.find("img", alt="原因").find_parent().find_parent().find('td').text.strip().replace("\u3000", "").split("\n")

    for i, val in enumerate(cause):
        val = val.strip().replace("\t","").replace("\n","")
        if len(val) > 0:
            cause_id = id + '_c_' + str(i).zfill(2)
            w_csv.writelines('"{}","{}","{}","{}"\n'.format(id, "cause", cause_id, val))

    # 状況の処理
    situation = html.find("img", alt="発生状況").find_parent().find_parent().find('td').text.strip().replace("\u3000", "").split("\n")
    for i, val in enumerate(situation):
        val = val.strip().replace("\t","").replace("\n","")
        if len(val) > 0:
            situation_id = id + '_s_' + str(i).zfill(2)
            w_csv.writelines('"{}","{}","{}","{}"\n'.format(id, "situation", situation_id, val))

    # 対策の処理
    measures = html.find("img", alt="対策").find_parent().find_parent().find('td').text.strip().replace("\u3000", "").split("\n")
    for i, val in enumerate(measures):
        val = val.strip().replace("\t","").replace("\n","")
        if len(val) > 0:
            measures_id = id + '_m_' + str(i).zfill(2)
            w_csv.writelines('"{}","{}","{}","{}"\n'.format(id, "measures", measures_id, val))

