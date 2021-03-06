
###以下为函数体部分###

##用户配置信息相关##
#函数体：读取配置

def get_config(config_name='inct_dir'):
    '''
    默认获取并返回指示文件目录；
    指定'uid'时获取并返回学号；
    指定'upw'时获取并返回密码.
    '''
    import sys
    import os
    if config_name == 'uid':
        uid = open('uid','r').read()
        return uid
    elif config_name == 'upw':
        upw = open('upw','r').read()
        return upw
    else:
        import sys
        inct_dir =  '.\\inct\\'
        return inct_dir

#函数体：判断配置是否存在，存在返回 True，否则创建sys.path[0] +
def chk_config():
    '''判断配置是否存在，存在返回 True ，否则创建'''
    from os import path
    if path.exists('uid') and path.exists('upw') and path.exists(get_config()):
        print("检查到存在配置文件，正在载入...")
        return True
    else:
        print("没有创建配置文件，请根据提示进行创建.")
        from os import mkdir
        uid = input('输入你的学号（11或12位）：\n')
        while len(uid) != 11 and len(uid) !=12:
            uid = input('你的输入长度有误，请再次输入：\n')
        upw = input('输入你的密码：\n')
        open('uid','w').write(uid)
        open('upw','w').write(upw)
        #mkdir(get_config() + '.\\')
        return True
       
##用户配置信息结束##

#函数体：获取当前日期，返回指示文件的文件名
def get_name(checked=False, page=False):
    '''
    默认返回原始文件名，指定 checked=True 时返回带a的文件名，指定 page=True 时返回带 s.png 的文件名；
    page 参数带有优先性，即两者同时指定 True 时，返回效果与仅指定 page=True 时相同.
    '''
    import time
    if checked == True:
        name = time.strftime('%Y{y}%m{m}%d{d}').format(y='年',m='月',d='日') + 'a'  #直接生成带有中文的名称会报错，似乎是模块自建编码的问题，故使用间接生成
    else:
        name = time.strftime('%Y{y}%m{m}%d{d}').format(y='年',m='月',d='日')  #直接生成带有中文的名称会报错，似乎是模块自建编码的问题，故使用间接生成
    if page == True:
        name = time.strftime('%Y{y}%m{m}%d{d}').format(y='年',m='月',d='日') + '.html'  #直接生成带有中文的名称会报错，似乎是模块自建编码的问题，故使用间接生成
    return name

#函数体：生成指示文件
def creat_inct(name):
    '''生成指示文件，只需指定文件名'''
    tmp = get_config() + name
    open(tmp, 'w').write('SUCCEED')


#函数体：进行上报与确认
def jksb(check=False):
    #准备webdriver（导入与简化不放在开头，以提高运行效率）
    from selenium import webdriver
    from time import sleep
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.firefox.options import Options

    options = Options()
    options.set_headless(True) # newer webdriver versions  #无头模式
    fx = webdriver.Firefox(options=options,executable_path='.\\geckodriver.exe') #默认加载本目录驱动
    fx.get('http://e-office2.nuist.edu.cn/infoplus/form/XNYQSB/start')  #开启网页
    print("开始填写")
    WebDriverWait(fx,10).until(EC.visibility_of_element_located((By.ID,'password')))
    fx.find_element_by_name("IDToken1").clear()  #清除原有学号
    fx.find_element_by_name("IDToken1").send_keys(get_config('uid'))  #填入学号
    fx.find_element_by_name("IDToken2").clear()  #清除原有密码
    fx.find_element_by_name("IDToken2").send_keys(get_config('upw'))  #填入密码
    fx.find_element_by_xpath("/html/body/div[2]/div/form/button[1]").click()  #点击登录
    if check != True:
        WebDriverWait(fx,10).until(EC.visibility_of_element_located((By.ID,'V1_CTRL82')))  #等待加载，若出现错误可增加等待时间
        fx.switch_to.default_content()  #回到原始框架
        fx.find_element_by_xpath("/html/body/div[4]/form/div/div[2]/div[3]/div/div[1]/div[1]/table/tbody/tr[2]/td/div[1]/table/tbody/tr[46]/td/div[1]/input").click()  #承诺
        fx.find_element_by_xpath("/html/body/div[4]/form/div/div[1]/div[2]/ul/li[1]").click()  #确认填报
        fx.implicitly_wait(30)  #等待加载，若出现错误可增加等待时间
        fx.find_element_by_xpath("/html/body/div[7]/div/div[2]/button[1]").click()  #上报完成，点击确认
        fx.refresh() #刷新网页获取结果
        WebDriverWait(fx,10).until(EC.visibility_of_element_located((By.ID,'title_content')))
        data = fx.find_element_by_xpath('/html/body/div[4]/form/div/div[1]/div[1]/div[2]/nobr')
        print("\n\n\n填写完成，检查inct文件夹html内容")

        open(get_config() + get_name(page=True),'wb').write(fx.page_source.encode("utf-8", "ignore"))  #保存网页，以备查询

        fx.quit()  #关闭浏览器

#函数体：判断运行情况
def run():
    '''
    检查运行情况，根据不同情况进行操作，未运行时无操作
    '''
    from os import path
    if path.exists(get_config() + get_name(checked=True)):
        print("\n今天已运行本工具，并且二次确认已上报成功！")
        input()
        sys.exit()
    elif path.exists(get_config() + get_name()):
        print("你今天已经上报，还需要再次确定吗？输入y表示确认，否则请直接退出.")
        tmp = input()
        while tmp != 'y':
            print("你输入了其他内容，如果需要再次检查请输入y，否则请直接退出.")
            tmp = input()
        #开始再次检查
        print("开始二次确认...\n\n")
        jksb(check=True)
        print("上报是否成功？若成功，请输入y，否则请自行上报，然后直接退出.\n")
        tmp = input()
        while tmp != 'y':
            print("你输入了其他内容，如果成功上报请输入y，否则自行上报，然后直接退出.")
            tmp = input()
        creat_inct(get_name(checked=True))
        sys.exit()


###以上为函数体部分###
