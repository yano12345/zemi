import cv2
import os
import datetime
import csv


def save_frame_camera_cycle(device_num, dir_path,delay=1, window_name='frame'):

    cap = cv2.VideoCapture(device_num)

    if not cap.isOpened():
        return
    
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

    
    while True:

        if cv2.waitKey(delay) & 0xFF == ord('q'):
                break

        now_time = datetime.datetime.now()
        hour_time = now_time.hour
        if (hour_time >= 0 and hour_time < 6) or (hour_time >= 17 and hour_time < 24):
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

if __name__ == "__main__":
    path = 'image'
    save_frame_camera_cycle(0, path)