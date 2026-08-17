import datetime
import json
import os
from pathlib import Path

class Attendance:
    def __init__(self):
        # 保存到桌面
        desktop = Path.home() / "Desktop"
        self.file = str(desktop / "attendance.json")
        self.today = datetime.datetime.now().strftime("%Y-%m-%d")
        self.data = json.load(open(self.file)) if os.path.exists(self.file) else {}
        
    def save(self):
        json.dump(self.data, open(self.file, 'w'), ensure_ascii=False, indent=2)
    
    def check_in(self):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.data.setdefault(self.today, {})['check_in'] = now
        self.save()
        print(f"✅ 上班打卡：{now}")
    
    def check_out(self):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        d = self.data.setdefault(self.today, {})
        d.setdefault('check_in', now)
        d['check_out'] = now
        
        t1 = datetime.datetime.strptime(d['check_in'], "%H:%M:%S")
        t2 = datetime.datetime.strptime(now, "%H:%M:%S")
        hours = (t2 - t1).seconds / 3600
        d['work_hours'] = round(hours, 2)
        self.save()
        print(f"✅ 下班打卡：{now} | 工时：{hours:.2f}h")
    
    def show(self):
        if not self.data:
            print("暂无记录")
            return
        print("-"*55)
        for date, r in sorted(self.data.items(), reverse=True):
            print(f"{date}  上班：{r.get('check_in','-')}  下班：{r.get('check_out','-')}  {r.get('work_hours',0)}h")
        print("-"*55)

def main():
    app = Attendance()
    while True:
        print("\n1.上班打卡  2.下班打卡  3.查看记录  4.退出")
        c = input("选择：").strip()
        if c == '1': app.check_in()
        elif c == '2': app.check_out()
        elif c == '3': app.show()
        elif c == '4': break
        else: print("无效")
        input("按回车继续...")

if __name__ == "__main__":
    main()
