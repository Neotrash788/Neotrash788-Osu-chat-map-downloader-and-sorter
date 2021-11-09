# import nessecary modules
import os,time,math,shutil,getpass,selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

cwd = os.getcwd().replace('\\','/')
user = getpass.getuser()
# read chat.txt
with open('chat.txt', 'r') as f:
    arr = f.readlines()
    # remove linebreaks
    for i in range(0, len(arr)):
        arr[i] = arr[i].rstrip('\n')
    # remove timestamps
    for i in range(len(arr)-1, 0, -1):
        if arr[i][2] == ':' or arr[i][1] == ':' and arr[i][-2:].isnumeric():
            arr.pop(i)
    # isolate map nums
    for i in range(0, len(arr)):
        pos = arr[i].find('osu.ppy.sh/beatmapsets/')
        if pos != -1:
            arr[i] = arr[i][pos+23:]
            pos = arr[i].find('/')
            arr[i] = arr[i][pos+1:]
            while True:
                if not arr[i][-1:].isnumeric():
                    arr[i] = arr[i][:-1]
                else:
                    break
    # remove doubble headings
    for i in range(len(arr)-1, 0, -1):
        if not arr[i].isnumeric() and not arr[i-1].isnumeric():
            arr.pop(i-1)
    maps = arr
    arr.append('END')

# removes evreything in folder 'OsuFiles'
folder = f'{cwd}/OsuFiles'
for File in os.listdir(folder):
    filePath = os.path.join(folder, File)
    if os.path.isfile(filePath) or os.path.islink(filePath):
        os.unlink(filePath)
        print('removed', filePath)
    elif os.path.isdir(filePath):
        shutil.rmtree(filePath)
        print('removed', filePath)


def drawProgressBar(mapNo, outOf):
    precent = math.floor((mapNo/outOf)*100)
    bar = '+'*(precent)
    bar = f'[{bar}{"_"*(100-precent)}]'
    print(f'''
    Currently on map {mapNo}/{outOf}
    {bar}({precent}%)
    ''')


def waitForElement(element):
    run = True
    while run:
        try:
            driver.find_element_by_xpath(element)
            run = False
        except Exception:
            print('Notloaded yet, trying again in 1 sec')
            time.sleep(0.25)


def createDir(Dir):
    try:
        childDir = Dir
        parentDir = f"{cwd}/OsuFiles"
        path = os.path.join(parentDir, childDir)
        os.mkdir(path)
        print(f'{parentDir} Crated {childDir}')
    except FileExistsError:
        print('File {Dir} alredy created')


# save all osu maps in downloads folder to a seprate folder
createDir('PreExistingOsuMapsInDownloadsFolder')
source = f'C:/Users/{user}/Downloads'
destination = f'{cwd}/OsuFiles/PreExistingOsuMapsInDownloadsFolder'
allfiles = os.listdir(source)
for f in allfiles:
    if f.endswith(".osz"):
        shutil.move(f'{source}/{f}', destination)


# declare were to get and put files
USERNAME = input('Osu Username ->')
PASSWORD = input('Osu Password ->')

username = getpass.getuser()

#initilise chrome + driver
try:
    driver = webdriver.Chrome(
        f'{cwd}/chromedriver.exe')
    url = 'https://osu.ppy.sh/home'
except selenium.common.exceptions.SessionNotCreatedException:
    print('Webdriver Out of date Check readme.pdf')
    input('Press enter to end')
    exit()
print('Connnecting to osu')
driver.get(url)

#login to account
print('Logging in')
driver.find_element_by_xpath(
    '/html/body/div[3]/nav/div[2]/div[2]/a').click()
driver.find_element_by_xpath(
    '/html/body/div[3]/div[2]/div/form/div[1]/input[1]').send_keys(USERNAME)
driver.find_element_by_xpath(
    '/html/body/div[3]/div[2]/div/form/div[1]/input[2]').send_keys(PASSWORD)
driver.find_element_by_xpath(
    '/html/body/div[3]/div[2]/div/form/div[5]/div/button/div').click()
print(f'Loged in as {USERNAME}')

# click beatmaps menu
waitForElement('/html/body/div[4]/div[1]/div[4]/div/div[1]/div[3]/a')
driver.find_element_by_xpath(
    '/html/body/div[4]/div[1]/div[4]/div/div[1]/div[3]/a').click()

# wait untill search bar loads
waitForElement('/html/body/div[7]/div/div[2]/div/div/div[2]/input')


def resetSearch(Map):
    #replace search with an invalid one
    driver.find_element_by_xpath(
        '/html/body/div[7]/div/div[2]/div/div/div[2]/input').clear()
    driver.find_element_by_xpath(
        '/html/body/div[7]/div/div[2]/div/div/div[2]/input').send_keys('()()()')
    #if there are no results we know its cleared
    while True:
        rows = 0
        for i in driver.find_elements_by_class_name('beatmapsets__items-row'):
            rows += 1
        if rows != 0:
            print('Search bar not cleard yet')
            time.sleep(0.25)
        else:
            break
    
    #search new map
    driver.find_element_by_xpath(
        '/html/body/div[7]/div/div[2]/div/div/div[2]/input').clear()
    driver.find_element_by_xpath(
        '/html/body/div[7]/div/div[2]/div/div/div[2]/input').send_keys(Map)

    #wait for new search results
    for i in range(0, 12):
        rows = 0
        for i in driver.find_elements_by_class_name('beatmapsets__items-row'):
            rows += 1
        if rows == 0:
            print(f'Search ({Map}) - not complete')
            time.sleep(0.25)
        else:
            break
    else:
        print(f'Search ({Map}) - Timeout')


def search(Map):
    #lookup map
    resetSearch(Map)
    time.sleep(0.25)

    #download map
    for i in range(0, 120):
        try:
            driver.find_element_by_xpath(
                '/html/body/div[7]/div/div[4]/div/div[2]/div/div/div/div/div/div/div[3]/div/a').click()
            time.sleep(0.25)
            break
        except NoSuchElementException:
            print(f'{Map} Not loaded yet')
            time.sleep(0.25)
        except Exception:
            break
    else:
        print(f'timeout Map No ({Map})')

#setup for moveing files
createDir('processing')
downloads = f'C:/Users/{username}/Downloads'
time.sleep(1)

def move(name):
    while True:
        try:
            #look for any undownloaded files
            for f in os.listdir(f'C:/Users/{user}/Downloads'):
                fn,fe = os.path.splitext(f)
                if fe == '.osz': shutil.move(f'C:/Users/{user}/Downloads/{fn+fe}',f'{cwd}/OsuFiles/processing')
                if fe == '.crdownload': raise ValueError('There is an undownloaded file')
            break
        except Exception:
            time.sleep(1)
    #make new dir and move files
    createDir(name)
    [shutil.move(f'{cwd}/OsuFiles/processing/{i}',f'{cwd}/OsuFiles/{name}') for i in os.listdir(f'{cwd}/OsuFiles/processing')]
    return None

#main loop
length = len(maps)
mapNo = 0
prevTitle = 'No Title'
for i in maps:
    drawProgressBar(mapNo, length)
    if i.isnumeric():
        search(i)
    else:
        move(prevTitle)
        prevTitle = i
    mapNo += 1
move(prevTitle)

#reset conditionsb
[shutil.move(f,f'C:/Users/{user}/Downloads') for f in os.listdir(f'{cwd}/OsuFiles/processing')]
for f in os.listdir(f'{cwd}/OsuFiles'):
    if len(os.listdir(f'{cwd}/OsuFiles/{f}')) == 0: shutil.rmtree(f'{cwd}/OsuFiles/{f}')
drawProgressBar(10,10)
driver.quit()
print('Process compleated with no errors')
input('Press enter to exit ->')

