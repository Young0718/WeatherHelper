import requests as rq
import tkinter as tk 
win=tk.Tk()
win.geometry("480x240+400+300")
win.title("未来4天天气")
texts=tk.Text(win,width=480,height=240,font=("黑体",15))
texts.grid(row=0,column=0,sticky=tk.W) 
with open("city.txt","r",encoding="utf-8") as f:
    cityCode=f.read()
if len(str(cityCode))==9:
    url="http://wthrcdn.etouch.cn/weather_mini?citykey="+str(cityCode)
    response=rq.get(url)
    futureDict=response.json()
    print(futureDict)
    day=futureDict['data']['forecast'][1:]
    weather=""
    for i in day:
        weather+=(i['date']+"，")+(i['high']+'，'+i['low'])+("，天气"+i['type']+'\n')
else:
    weather="非中国地区，暂无数据！" 
texts.delete("0.0","end")
texts.insert("0.0",weather)
win.mainloop()
