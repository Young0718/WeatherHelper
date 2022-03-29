#encoding=utf-8
#导入
import requests as rq
import pygame
from pygame import *
from sys import exit
from subprocess import Popen,PIPE
import easygui

#pygame初始化
pygame.init()
global canvas
canvas = pygame.display.set_mode((1050, 660))
pygame.display.set_caption('天气助手')

#预加载图片
bg=pygame.image.load("image/bg.png")
bg2=pygame.image.load("image/bg2.png")
sunny=pygame.image.load("image/sunny.png")
rainy=pygame.image.load("image/rainy.png")
cloudy=pygame.image.load("image/cloudy.png")
snowy=pygame.image.load("image/snowy.png")
button=pygame.image.load("image/button.png")

#预加载音频
track=pygame.mixer.music.load("radio/bgm.mp3")

#绘制文字
def fillText(content, size, pos):
    fontColor ='black'
    fontObj = pygame.font.Font("font/simhei.ttf", size)
    font = fontObj.render(content, True, fontColor)
    canvas.blit(font, pos)

#打印信息
def showDetail(cityName,temp,weather,tips):
    fillText(cityName, 45, (350, 185))
    fillText(temp, 18, (300, 285))
    fillText(weather, 35, (540, 280))
    if len(tips)>20:
        fillText(tips[0:20], 18, (200, 460))
        fillText(tips[20:], 18, (200, 490))
    else:
        fillText(tips,18,(200,460))
    pygame.display.update()
#获取城市码
def getCityCode(cityName):
    url="https://geoapi.qweather.com/v2/city/lookup?location="+cityName+"&key=22e5754064734fb490ed11f4b1ef10e1"
    response=rq.get(url)
    cityDict=response.json()
    cityID=cityDict['location'][0]['id']
    return str(cityID)

#获取基本信息
def getBasic(cityCode):
    url="https://devapi.qweather.com/v7/weather/now?location="+cityCode+"&key=22e5754064734fb490ed11f4b1ef10e1"
    response=rq.get(url)
    weatherDict=response.json()
    return weatherDict

#获取小贴士
def getTips(cityCode):
    url="http://wthrcdn.etouch.cn/weather_mini?citykey="+str(cityCode)
    response=rq.get(url)
    tipsDict=response.json()
    return tipsDict

#整理信息
def Weather(cityName):
    #城市码
    cityCode=getCityCode(cityName)
    
    #基础信息
    Dict1=getBasic(cityCode)
    temp="温度"+Dict1['now']['temp']+"℃，体感温度"+Dict1['now']['feelsLike']+'℃'
    weather=Dict1['now']['text']
    url="https://geoapi.qweather.com/v2/city/lookup?location="+cityName+"&key=22e5754064734fb490ed11f4b1ef10e1"
    response=rq.get(url)
    cityDict=response.json()
    country=cityDict['location'][0]['country']
    city=cityDict['location'][0]['name']
    #小贴士
    if country=="中国":
        Dict2=getTips(cityCode)
        tips=Dict2['data']['ganmao']
    else:
        tips="非中国地区，暂无数据"
    
    #切换背景
    if "雪" in weather:
            canvas.blit(snowy,(0,0))
    elif "雨" in weather or "雷" in weather:
            canvas.blit(rainy,(0,0))
    elif "雾" in weather or "霾" in weather or "云" in weather or "阴" in weather:
            canvas.blit(cloudy,(0,0))
    elif "晴" in weather:
            canvas.blit(sunny,(0,0))
    else:
            canvas.blit(bg2,(0,0))
    
    #打印
    showDetail(city,temp,weather,tips)
    pygame.display.update()
    
#主界面
canvas.blit(bg,(0,0))
pygame.display.update()

#等待进入二级界面
flag=True
while flag:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            exit()
        elif event.type==MOUSEBUTTONDOWN:
            x=event.pos[0]
            y=event.pos[1]
            if 396<=x<=650 and 442<=y<=511:
                canvas.blit(bg2,(0,0))
                flag=False
    pygame.display.update()

#预写入
Weather("北京")
with open("city.txt","w",encoding="utf-8") as f:
    f.write(getCityCode("北京"))

#播放背景音乐
pygame.mixer.music.play(-1)

#二级界面
while True:
    canvas.blit(button,(266,544))
    for event in pygame.event.get():
        pygame.display.update()
        if event.type==QUIT:
            pygame.quit()
            exit()
        elif event.type==MOUSEBUTTONDOWN:
            x=event.pos[0]
            y=event.pos[1]
            if 680 <=x<=934 and 63<=y<= 134:
                print("更换城市")
                city = easygui.enterbox('请输入要查询的城市',title='city')
                if city=='':
                    continue
                try:
                    code=getCityCode(city)
                except:
                    print("ERROR!")
                    continue
                with open("city.txt","w",encoding="utf-8") as f:
                    f.write(code)
                Weather(city)
                pygame.display.update()
            if 266<=x<=266+388 and 544<=y<=544+124:
                print("未来天气")
                Popen('python future.py',shell=True,stdout=PIPE)
    pygame.display.update()
                
