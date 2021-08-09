import lcd
import image
import machine, time
from machine import Timer
from fpioa_manager import fm

try:from cocorobo import display_cjk_string
except:pass

_gp_side_buttons = [9, 10, 11]

FPIOA().set_function(_gp_side_buttons[0],FPIOA.GPIO0)
FPIOA().set_function(_gp_side_buttons[1],FPIOA.GPIO1)
FPIOA().set_function(_gp_side_buttons[2],FPIOA.GPIO2)

_gp_side_a = GPIO(GPIO.GPIO0,GPIO.IN,GPIO.PULL_UP)
_gp_side_b = GPIO(GPIO.GPIO1,GPIO.IN,GPIO.PULL_UP)
_gp_side_c = GPIO(GPIO.GPIO2,GPIO.IN,GPIO.PULL_UP)

def _timer_on_timer(timer):
    global _timer_current_time_elapsed
    _timer_current_time_elapsed =  _timer_current_time_elapsed + 1

_timer_current_time_elapsed = 0
_timer_tim = Timer(Timer.TIMER1, Timer.CHANNEL1, mode=Timer.MODE_PERIODIC, period=1, callback=_timer_on_timer)

def lcd_draw_string(canvas, x, y, text, color=(255,255,255), font_size=1, scale=1, mono_space=False, auto_wrap=True):
    try:
        if font_size == 1 and scale != 1: font_size = scale
        else: font_size = font_size
        display_cjk_string(canvas, x, y, text, font_size=font_size, color=color)
        return canvas
    except: return canvas.draw_string(x, y, text, color=color, scale=scale, mono_space=mono_space)

fm.register(13,fm.fpioa.UART2_TX)
fm.register(14,fm.fpioa.UART2_RX)
robot_dog_setup_uart = machine.UART(machine.UART.UART2,115200,bits=8,parity=None,stop=1)

def add(a,b):
    num1 = a ^ b
    num2 = (a & b) << 1
    while num2 != 0:
        temp  = num1 ^ num2
        num2 = (num1 & num2) << 1
        num1 = temp
    return num1

def calculate_sum(a,b):
    bytearr = [9, 1, a, b]
    sum = 0
    for i in bytearr:
        sum = add(sum,i)
    calculated_cksum = bin(sum).replace("0b","")
    while len(calculated_cksum) < 8:
        calculated_cksum = "0" + calculated_cksum
    ReturningChecksum = ""
    for index in range(len(calculated_cksum)):
        if calculated_cksum[index] == "1":
            ReturningChecksum += "0"
        elif calculated_cksum[index] == "0":
            ReturningChecksum += "1"
    return bytes([int(hex(int(ReturningChecksum,2)),16)])

def mapping(input_value,i_min,i_max,o_min,o_max):
    if input_value < i_min:
        input_value = i_min
    if input_value > i_max:
        input_value = i_max
    dat=(input_value-i_min)/(i_max-i_min)*(o_max-o_min)+o_min
    return int(dat)

try:
	from cocorobo import firmware_info
except BaseException as e:
	print(str(e))
	pass

asr = None

if str(firmware_info.ai()) == "2020-12-26" or str(firmware_info.ai()) == "2021-04-16":
	from Maix import GPIO, I2S
	from fpioa_manager import fm
	fm.register(20,fm.fpioa.I2S0_IN_D0, force=True)
	fm.register(18,fm.fpioa.I2S0_SCLK, force=True) # dock 32
	fm.register(19,fm.fpioa.I2S0_WS, force=True)   # dock 30

	rx = I2S(I2S.DEVICE_0)
	rx.channel_config(rx.CHANNEL_0, rx.RECEIVER, align_mode=I2S.STANDARD_MODE)
	rx.set_sample_rate(16000)

	from speech_recognizer import asr

	class maix_asr(asr):

		asr_vocab = ['lv', 'shi', 'yang', 'chun', 'yan', 'jing', 'da', 'kuai', 'wen', 'zhang', 'de', 'di', 'se', 'si', 'yue', 'lin', 'luan', 'geng', 'xian', 'huo', 'xiu', 'mei', 'yi', 'ang', 'ran', 'ta', 'jin', 'ping', 'yao', 'bu', 'li', 'liang', 'zai', 'yong', 'dao', 'shang', 'xia', 'fan', 'teng', 'dong', 'she', 'xing', 'zhuang', 'ru', 'hai', 'tun', 'zhi', 'tou', 'you', 'ling', 'pao', 'hao', 'le', 'zha', 'zen', 'me', 'zheng', 'cai', 'ya', 'shu', 'tuo', 'qu', 'fu', 'guang', 'bang', 'zi', 'chong', 'shui', 'cuan', 'ke', 'shei', 'wan', 'hou', 'zhao', 'jian', 'zuo', 'cu', 'hei', 'yu', 'ce', 'ming', 'dui', 'cheng', 'men', 'wo', 'bei', 'dai', 'zhe', 'hu', 'jiao', 'pang', 'ji', 'lao', 'nong', 'kang', 'yuan', 'chao', 'hui', 'xiang', 'bing', 'qi', 'chang', 'nian', 'jia', 'tu', 'bi', 'pin', 'xi', 'zou', 'chu', 'cun', 'wang', 'na', 'ge', 'an', 'ning', 'tian', 'xiao', 'zhong', 'shen', 'nan', 'er', 'ri', 'zhu', 'xin', 'wai', 'luo', 'gang', 'qing', 'xun', 'te', 'cong', 'gan', 'lai', 'he', 'dan', 'wei', 'die', 'kai', 'ci', 'gu', 'neng', 'ba', 'bao', 'xue', 'shuai', 'dou', 'cao', 'mao', 'bo', 'zhou', 'lie', 'qie', 'ju', 'chuan', 'guo', 'lan', 'ni', 'tang', 'ban', 'su', 'quan', 'huan', 'ying', 'a', 'min', 'meng', 'wu', 'tai', 'hua', 'xie', 'pai', 'huang', 'gua', 'jiang', 'pian', 'ma', 'jie', 'wa', 'san', 'ka', 'zong', 'nv', 'gao', 'ye', 'biao', 'bie', 'zui', 'ren', 'jun', 'duo', 'ze', 'tan', 'mu', 'gui', 'qiu', 'bai', 'sang', 'jiu', 'yin', 'huai', 'rang', 'zan', 'shuo', 'sha', 'ben', 'yun', 'la', 'cuo', 'hang', 'ha', 'tuan', 'gong', 'shan', 'ai', 'kou', 'zhen', 'qiong', 'ding', 'dang', 'que', 'weng', 'qian', 'feng', 'jue', 'zhuan', 'ceng', 'zu', 'bian', 'nei', 'sheng', 'chan', 'zao', 'fang', 'qin', 'e', 'lian', 'fa', 'lu', 'sun', 'xu', 'deng', 'guan', 'shou', 'mo', 'zhan', 'po', 'pi', 'gun', 'shuang', 'qiang', 'kao', 'hong', 'kan', 'dian', 'kong', 'pei', 'tong', 'ting', 'zang', 'kuang', 'reng', 'ti', 'pan', 'heng', 'chi', 'lun', 'kun', 'han', 'lei', 'zuan', 'man', 'sen', 'duan', 'leng', 'sui', 'gai', 'ga', 'fou', 'kuo', 'ou', 'suo', 'sou', 'nu', 'du', 'mian', 'chou', 'hen', 'kua', 'shao', 'rou', 'xuan', 'can', 'sai', 'dun', 'niao', 'chui', 'chen', 'hun', 'peng', 'fen', 'cang', 'gen', 'shua', 'chuo', 'shun', 'cha', 'gou', 'mai', 'liu', 'diao', 'tao', 'niu', 'mi', 'chai', 'long', 'guai', 'xiong', 'mou', 'rong', 'ku', 'song', 'che', 'sao', 'piao', 'pu', 'tui', 'lang', 'chuang', 'keng', 'liao', 'miao', 'zhui', 'nai', 'lou', 'bin', 'juan', 'zhua', 'run', 'zeng', 'ao', 're', 'pa', 'qun', 'lia', 'cou', 'tie', 'zhai', 'kuan', 'kui', 'cui', 'mie', 'fei', 'tiao', 'nuo', 'gei', 'ca', 'zhun', 'nie', 'mang', 'zhuo', 'pen', 'zun', 'niang', 'suan', 'nao', 'ruan', 'qiao', 'fo', 'rui', 'rao', 'ruo', 'zei', 'en', 'za', 'diu', 'nve', 'sa', 'nin', 'shai', 'nen', 'ken', 'chuai', 'shuan', 'beng', 'ne', 'lve', 'qia', 'jiong', 'pie', 'seng', 'nuan', 'nang', 'miu', 'pou', 'cen', 'dia', 'o', 'zhuai', 'yo', 'dei', 'n', 'ei', 'nou', 'bia', 'eng', 'den', '_']

		def get_asr_list(string='xiao-ai-fas-tong-xue'):
			return [__class__.asr_vocab.index(t) for t in string.split('-') if t in __class__.asr_vocab]

		def get_asr_string(listobj=[117, 214, 257, 144]):
			return '-'.join([__class__.asr_vocab[t] for t in listobj if t < len(__class__.asr_vocab)])

		def unit_test():
			print(__class__.get_asr_list('xiao-ai'))
			print(__class__.get_asr_string(__class__.get_asr_list('xiao-ai-fas-tong-xue')))

		def config(self, sets):
			self.set([(sets[key], __class__.get_asr_list(key)) for key in sets])

		def recognize(self):
			res = self.result()
			# print(tmp)
			if res != None:
				#print(res)
				sets = {}
				for tmp in res:
					#print(tmp)
					sets[__class__.get_asr_string(tmp[1])] = tmp[0]
					#print(tmp[0], get_asr_string(tmp[1]))
				return sets
			return None

	from machine import Timer

	def on_timer(timer):
		#print('time up:',timer)
		#print('param:',timer.callback_arg())
		timer.callback_arg().state()

	def getRecognizeResult():
		try:
			t = maix_asr(0x500000, I2S.DEVICE_0, 3, shift=0)
			tim = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PERIODIC, period=64, callback=on_timer, arg=t)
			tim.start()
			t.config({"mi-shi":0.1, "wo-shou":0.1, "zhuan-quan":0.1, "pa-xing":0.1, "yao-bai":0.1, "chi-fan":0.1, "zhao-shou":0.1, "sa-niao":0.1, "zuo-xia":0.1, "zhan-li":0.1, "pa-xia":0.1, "dun-qi":0.1, "shen-lan-yao":0.1, "bo-lang":0.1})
			print(t.get())
			while True:
				tmp = t.recognize()
				if tmp != None:
					print(tmp)
					for key in tmp.keys():
						return key
		except Exception as e:
			print(e)
		finally:
			tim.stop()
			t.__del__()
			del t

else:
	from cocorobo import mandarin_asr
	asr = mandarin_asr(
       config = {"mi-shi":0.1, "wo-shou":0.1, "zhuan-quan":0.1, "pa-xing":0.1, "yao-bai":0.1, "chi-fan":0.1, "zhao-shou":0.1, "sa-niao":0.1, "zuo-xia":0.1, "zhan-li":0.1, "pa-xia":0.1, "dun-qi":0.1, "shen-lan-yao":0.1, "bo-lang":0.1}
	)

def getRecoResult():
	global asr
	if str(firmware_info.ai()) == "2020-12-26" or str(firmware_info.ai()) == "2021-04-16":
	    return getRecognizeResult()
	else:
	    return asr.getRecognizeResult()

_canvas_x, _canvas_y = 0, 0



lcd.init(type=2,freq=15000000,width=240,height=240,color=(0,0,0))
lcd.rotation(1)
lcd.clear(lcd.BLACK)
canvas = image.Image(size=(240, 240))
vocabulary_list = {
    "mi-shi": "觅食",
    "wo-shou": "握手",
    "zhuan-quan": "转圈",
    "pa-xing": "爬行",
    "yao-bai": "摇摆",
    "chi-fan": "吃饭",
    "zhao-shou": "招手",
    "sa-niao": "撒尿",
    "zuo-xia": "坐下",
    "zhan-li": "站立",
    "pa-xia": "趴下",
    "dun-qi": "蹲起",
    "shen-lan-yao": "伸懒腰",
    "bo-lang": "波浪"
}
while True:
    lcd_draw_string(canvas,22, 5, "Mandarin to Text Demo", color=(255,255,255), scale=1, mono_space=False)

    canvas.draw_rectangle(40, 50-10, 160, 60, color=(100,100,100), thickness=1, fill=False)

    canvas.draw_line(5,120, 235,120, color=(100,100,100), thickness=1)
    lcd_draw_string(canvas,5, 128, "Please say the following:", color=(255,255,255), scale=1, mono_space=False)
    lcd_draw_string(canvas,5, 130+22*1, "觅食、握手、转圈、爬行", color=(0,255,255), scale=1, mono_space=False)
    lcd_draw_string(canvas,5, 130+22*2, "摇摆、吃饭、招手、撒尿", color=(0,255,255), scale=1, mono_space=False)
    lcd_draw_string(canvas,5, 130+22*3, "坐下、站立、趴下、蹲起", color=(0,255,255), scale=1, mono_space=False)
    lcd_draw_string(canvas,5, 130+22*4, "伸懒腰、波浪", color=(0,255,255), scale=1, mono_space=False)
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    
    lis = getRecoResult()
    
    canvas.draw_rectangle(40, 50-10, 160, 60, color=(0,0,0), thickness=1, fill=True)
    canvas.draw_rectangle(40, 50-10, 160, 60, color=(100,100,100), thickness=1, fill=False)
    lcd_draw_string(canvas, 50, 60-10, vocabulary_list[lis], color=(0,255,255), scale=2, mono_space=False)
    lcd.display(canvas, oft=(_canvas_x,_canvas_y))
    if lis == "mi-shi":
        robot_dog_setup_uart.write(bytes([68]))
        time.sleep_ms(20)
    elif lis == "wo-shou":
        robot_dog_setup_uart.write(bytes([69]))
        time.sleep_ms(20)
    elif lis == "zhuan-quan":
        robot_dog_setup_uart.write(bytes([54]))
        time.sleep_ms(20)
    elif lis == "pa-xing":
        robot_dog_setup_uart.write(bytes([53]))
        time.sleep_ms(20)
    elif lis == "yao-bai":
        robot_dog_setup_uart.write(bytes([66]))
        time.sleep_ms(20)
    elif lis == "chi-fan":
        robot_dog_setup_uart.write(bytes([67]))
        time.sleep_ms(20)
    elif lis == "zhao-shou":
        robot_dog_setup_uart.write(bytes([63]))
        time.sleep_ms(20)
    elif lis == "sa-niao":
        robot_dog_setup_uart.write(bytes([61]))
        time.sleep_ms(20)
    elif lis == "zuo-xia":
        robot_dog_setup_uart.write(bytes([62]))
        time.sleep_ms(20)
    elif lis == "zhan-li":
        robot_dog_setup_uart.write(bytes([52]))
        time.sleep_ms(20)
    elif lis == "pa-xia":
        robot_dog_setup_uart.write(bytes([51]))
        time.sleep_ms(20)
    elif lis == "dun-qi":
        robot_dog_setup_uart.write(bytes([56]))
        time.sleep_ms(20)
    elif lis == "shen-lan-yao":
        robot_dog_setup_uart.write(bytes([64]))
        time.sleep_ms(20)
    elif lis == "bo-lang":
        robot_dog_setup_uart.write(bytes([65]))
        time.sleep_ms(20)
    if _gp_side_c.value() == 1:
        C_time = _timer_current_time_elapsed
        while _gp_side_c.value() == 1:
            time.sleep_ms(1)
            if (_timer_current_time_elapsed) - C_time >= 1000:
                machine.reset()
