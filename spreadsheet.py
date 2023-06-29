import gspread
import csv
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#ダウンロードしたjsonファイルをドライブにアップデートした際のパス
json = '/Users/yanokoutarou/workspace/ゼミ/code/dataset-389006-c2278299b07c.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(json, scope)

gc = gspread.authorize(credentials)

#書き込み先のスプレッドシートキーを追加
SPREADSHEET_KEY = '1eo59cpom2o9WgVw_eqNa3uohk1tF3fZewGnJ-GJdFhY'


#共有設定したスプレッドシートの1枚目のシートを開く
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

num = 0
page = 0

with open('test.csv','a') as f:
        writer = csv.writer(f)
        writer.writerow(["1","1","1"])
        writer.writerow(["1","1","1"])
        writer.writerow(["1","1","1"])
        writer.writerow(["1","1","1"])
        writer.writerow(["1","1","1"])
        writer.writerow(["3","3","3"])
f.close()

#書き込み用の文字列を作成
with open('test.csv','r') as f:
        read = csv.reader(f)
        for i in read:
            worksheet.append_row(i)
            page += 1
f.close()
# シートへ文字列を追加
with open('test.csv','a') as f:
        writer = csv.writer(f)
        writer.writerow(["\n"])
        writer.writerow(["4","4","4"])
        writer.writerow(["2","2","2"])
        writer.writerow(["2","2","2"])
        writer.writerow(["2","2","2"])
f.close()

with open('test.csv','r') as f:
        read = csv.reader(f)
        for i in read:
            if (num == page):
                worksheet.append_row(i)
                page+=1
            num += 1
f.close()

print(page)