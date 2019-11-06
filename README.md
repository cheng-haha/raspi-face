# raspi-face
 基于树莓派的人脸识别
 
 一：项目拉取
 
 		git clone https://github.com/cheng-haha/raspi-face.git
		
二：运行人脸识别程序

    cd raspi-face
  
  如果是sg90舵机控制门锁：
  
    python3 face_recongnition.py
    
  如果是普通舵机控制：
  
    python3 face_recongnition2.py
    
三：项目原理

  1.启动程序后无限循环检查连接按钮的GPIO引脚，如果为低电平，则进入人脸识别模块
  
  2.启动人脸识别后获取照片，返回json格式文本，如果为与百度人脸识别组内相同的人脸，则有三种功能的同时进行：
  
   （1）舵机转动，智能门禁。也可用继电器加电磁锁的组合。
      
   （2）发送mqtt信息给智能家居，例如开灯，开电风扇，开电风扇，达到开门和灯（或者其他家居，消息可自己设置开哪一个电器）同时亮起的效果。
 
   （3）发送信息给微信，告诉主人家里来人了，平且同时告知主人来的是谁以及正在进行的动作，例如DoorOpen就是开门，cheng就是代表来的是谁。
  
  3.如果为与百度人脸识别组不同的人脸，则播放中国人民共和国私闯民宅法律的语音。
  
  
  
  
 												  作者：程东洲
  
  												  2019.11.6
  
