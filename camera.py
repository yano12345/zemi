import cv2
import os
import datetime
import csv
import json
import glob
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def save_frame_camera_cycle(device_num, dir_path,delay=1, window_name='frame'):

    INITIAL_FILE= "/Users/yanokoutarou/workspace/ゼミ/code/cert/initial.json"

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with open(INITIAL_FILE) as f: # 初期設定ファイルの読み込み
        jsn = json.load(f)
        folder_id = jsn["folder_id"] # folder_idの読み込み
    
    drive = auth_gd()

    os.makedirs(dir_path, exist_ok=True)
    
    for i in range(1,13):
        if (i==4 or i==6 or i==9 or i==11):
            for j in range(1,31):
                os.makedirs(dir_path + "/" + str(i).zfill(2) + "/" + str(j).zfill(2),exist_ok=True)
        elif (i==2):
            for j in range(1,29):
                os.makedirs(dir_path + "/" + str(i).zfill(2) + "/" + str(j).zfill(2),exist_ok=True)
        else:
            for j in range(1,32):
                os.makedirs(dir_path + "/" + str(i).zfill(2) + "/" + str(j).zfill(2),exist_ok=True)

    

    with open('dataset.csv','x') as f:
        writer = csv.writer(f)
        writer.writerow(["image_path","image_start_time","image_stop_time"])
    f.close()

    base_time = datetime.datetime.now()
    now_time = datetime.datetime.now()

    timeFlag = 0
    dayFlag = 0

    
    while True:

        if cv2.waitKey(delay) & 0xFF == ord('q'):
                break

        now_time = datetime.datetime.now()
        hour_time = now_time.hour
        if (hour_time >= 0 and hour_time < 6) or (hour_time >= 17 and hour_time < 24):
            if (hour_time == 20 and dayFlag == 0):
                print('アップロード開始') 
                first_path = dir_path + str(now_time.month).zfill(2)
                second_path = first_path + '/' + str(now_time.day).zfill(2)
                base_path = create_dir(folder_id,'Image',drive)
                first_folder = create_dir(base_path,os.path.basename(first_path),drive)
                second_folder = create_dir(first_folder,os.path.basename(second_path),drive)
                dir_list = dirList(second_path)
                for i in dir_list:
                    third_folder = create_dir(second_folder,os.path.basename(i),drive)
                    file_list = fileList(i)
                    upload_file(third_folder,file_list,drive)
                dayFlag = 1
                print('finish')
            continue
        else:
            now_min = str(now_time.minute).zfill(2)
            now_min = now_min[-2]
            min = int(now_min)*10
            next_time = datetime.datetime(now_time.year,now_time.month,now_time.day,now_time.hour,min,0)
            next_time = next_time + datetime.timedelta(seconds = 600)
            shooting_time = next_time - now_time

            path = dir_path+"/"+str(next_time.month).zfill(2)+"/"+str(next_time.day).zfill(2)+"/"+str(next_time.hour).zfill(2)+"_"+str(next_time.minute).zfill(2)

            if (timeFlag == 0):
                if (now_time.minute % 10 == 0):
                    timeFlag = 1
                    base_time = datetime.datetime.now()
                    os.makedirs(path,exist_ok=True)
                    Recording(shooting_time.seconds+1,path+"/"+str(next_time))
                    with open('dataset.csv','a') as f:
                        writer = csv.writer(f)
                        writer.writerow([path+"/"+str(next_time),now_time,next_time])
                    f.close()
            else:
                pass_time = now_time - base_time
                if(pass_time.seconds > 10):
                    base_time = datetime.datetime.now()
                    os.makedirs(path,exist_ok=True)
                    Recording(shooting_time.seconds+1,path+"/"+str(next_time))
                    with open('dataset.csv','a') as f:
                        writer = csv.writer(f)
                        writer.writerow([path+"/"+str(next_time),now_time,next_time])
                    f.close()
                dayFlag = 0


        

    cv2.destroyWindow(window_name)

def Recording(time,path,delay=1):
    cap = cv2.VideoCapture(0)
    
    #fpsを20.0にして撮影したい場合はfps=20.0にします
    fps = 30.0
    
    #カメラの幅を取得
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    #カメラの高さを取得
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    #動画保存時の形式を設定
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    name = path + ".mov"
    
    #(保存名前、fourcc,fps,サイズ)
    video = cv2.VideoWriter(name, fourcc, fps, (w,h))
 
    #fps×指定した撮影時間の値繰り返す
    print("start")
    roop = int(fps * time)
    for i in range(roop):
        ret, frame = cap.read()#1フレーム読み込み
        video.write(frame)#1フレーム保存する
        if cv2.waitKey(delay) & 0xFF == ord('q'):
                break
    
    print("stop")
    video.release()
    cap.release()
    cv2.destroyAllWindows()
    
    return video

def auth_gd():
    gauth = GoogleAuth() # GoogleDrive認証
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    print('認証完了')
    return drive

def create_dir(pid,fname,drive=None):
    if drive == None:
        drive = auth_gd()

    ret = check_file(pid,fname,drive)
    if ret==False:
        folder = drive.CreateFile({'title':fname,
                                   'mimeType': 'application/vnd.google-apps.folder'})
        folder['parents'] = [{'id':pid}]
        folder.Upload()
    else:
        folder = ret

    return folder['id']

def upload_file(pid,path,drive=None):
    if drive == None:
        drive = auth_gd()

    name = os.path.basename(path)

    ret = check_file(pid,path,drive)
    if ret == False:
        gf = drive.CreateFile({'title':name,
                               'mimeType': 'video/H264',
                               'parents': [{'kind': 'drive#fileLink', 'id':pid}]})
        gf.SetContentFile(path)
        gf.Upload()
    else:
        gf = ret
        print(gf['title']+" exists")

    return gf


def check_file(pid,fname,drive=None):
    if drive==None:
        drive = auth_gd()

    query = '"{}" in parents'.format(pid)
    query += ' and title = "' + os.path.basename(fname) + '"'

    list =  drive.ListFile({'q': query}).GetList()
    if len(list)> 0:
        return list[0]
    return False    

def dirList(path):
    dirList = glob.glob(path+'/*')

    return dirList

def fileList(path):
    fileList = glob.glob(path+'/*.mov')
    fileList = "".join(fileList)

    return fileList

if __name__ == "__main__":
    path = 'image'
    save_frame_camera_cycle(0, path)