import os
import time
import math
import shutil
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# Print progress


def drawProgressBar(mapNo, outOf):
    precent = math.floor((mapNo/outOf)*100)
    bar = '+'*(precent)
    bar = f'[{bar}{"_"*(100-precent)}]'
    print(f'''
    Currently on map {mapNo}/{outOf}
    {bar}({precent}%)
    ''')


# declare were to get and put files
USERNAME = input('Osu Username ->')
PASSWORD = input('Osu Password ->')
username = input('Windows Username ->')

# create diretoryes to store files


def createDir(Dir):
    try:
        childDir = Dir
        parentDir = f"C:/Users/{username}/Desktop/OsuThingey/OsuFiles"
        path = os.path.join(parentDir, childDir)
        os.mkdir(path)
        print(f'{parentDir} Crated {childDir}')
    except FileExistsError:
        pass


# read the chat.txt fike
with open('Chat.txt', 'r') as f:
    maps = f.readlines()

# remove timestamps made by osu
for i in range(0, len(maps)):
    try:
        if maps[i][-3] == ':':
            maps.pop(i)
    except Exception:
        pass

# login to the users osu account with chrome
driver = webdriver.Chrome(
    f'C:/Users/{username}/Desktop/OsuThingey/chromedriver')
url = 'https://osu.ppy.sh/home'

print('Connnecting to osu')
driver.get(url)

print('Logging in')
driver.find_element_by_xpath(
    '/html/body/div[3]/nav/div[2]/div[2]/a').click()
driver.find_element_by_xpath(
    '/html/body/div[3]/div[2]/div/form/div[1]/input[1]').send_keys(USERNAME)
driver.find_element_by_xpath(
    '/html/body/div[3]/div[2]/div/form/div[1]/input[2]').send_keys(PASSWORD)
driver.find_element_by_xpath(
    '/html/body/div[3]/div[2]/div/form/div[5]/div/button/div').click()
print(f'Loged in as {username}')

# navagate to the beatmaps search menu on the osu site
webdriverCompletedCurrentTask = False
while not webdriverCompletedCurrentTask:
    try:
        time.sleep(1)
        driver.find_element_by_xpath(
            '/html/body/div[4]/div[1]/div[4]/div/div[1]/div[3]/a').click()
        webdriverCompletedCurrentTask = True
    except Exception:
        print('site not loded yet, trying again in 1 second')

# Remove linebreaks in maps from chat.txt
mapNums = []
for Map in maps:
    if Map.find(':') == -1:
        lastSlash = int(Map.rfind('/')+1)
        mapNums.append(Map[lastSlash:].strip('\n'))

# Remove text before and after Osu Link
for i in range(1, len(maps)):
    if maps[i][len(maps[i])-1].isnumeric() == False and maps[i].find('osu.ppy.sh') != -1:
        lastSlash = maps[i].rfind('/')
        for ii in range(lastSlash+1, len(maps[i])-1):
            if maps[i][ii].isnumeric() != True:
                lastNumeric = ii
                maps[i] = maps[i][:lastNumeric]
                break
if maps[i].find('osu.ppy.sh') != 0 and maps[i].find('osu.ppy.sh') != -1:
    osuBegins = maps[i].find('osu.ppy.sh')
    maps[i] = maps[i][osuBegins:]

# Removes evreything in folder 'OsuFiles'
folder = f'C:/Users/{username}/Desktop/OsuThingey/OsuFiles'
for File in os.listdir(folder):
    filePath = os.path.join(folder, File)
    if os.path.isfile(filePath) or os.path.islink(filePath):
        os.unlink(filePath)
        print('removed', filePath)
    elif os.path.isdir(filePath):
        shutil.rmtree(filePath)
        print('removed', filePath)

# save all osu maps in downloads folder to a seprate folder
createDir('PreExistingOsuMapsInDownloadsFolder')
folder = 'PreExistingOsuMapsInDownloadsFolder'
source = f'C:/Users/{username}/Downloads/'
destination = f'C:/Users/{username}/Desktop/OsuThingey/OsuFiles/{folder}/'
allfiles = os.listdir(source)
for f in allfiles:
    if f.endswith(".osz"):
        shutil.move(source + f, destination + f)

# declare which folder we dump undifind maps into
folder = 'No Grouping'

# Downloading and sorting files
numberOfMaps = len(mapNums)
onMap = 1
for num in mapNums:
    drawProgressBar(onMap, numberOfMaps)
    onMap += 1
    try:
        test = int(num)  # throws err if text is not an osu map
        webdriverCompletedCurrentTask = False
        print(num)
        time.sleep(0.75)

        # searches in beatmaps searchbar for current map id
        driver.find_element_by_xpath(
            '/html/body/div[7]/div/div[2]/div/div/div[2]/input').clear()
        driver.find_element_by_xpath(
            '/html/body/div[7]/div/div[2]/div/div/div[2]/input').send_keys(num)

        # difine timeout
        timeout = 5

        # account for wifispeed
        while not webdriverCompletedCurrentTask:
            try:
                # click download on the beatmap div
                time.sleep(0.75)
                driver.find_element_by_xpath(
                    '/html/body/div[7]/div/div[4]/div/div[2]/div/div/div/div/div/div/div[3]/div/a').click()
                webdriverCompletedCurrentTask = True
            except Exception:
                # if map download times out
                if timeout > 0:
                    print('Map not loaded')
                    timeout -= 1
                else:
                    print(
                        f'{num} Could not be downloaded as it is no longer on osu servers or dident appear in any surch results')
                    webdriverCompletedCurrentTask = True
    except ValueError:
        # Error occurs when text input is not a map (is a headder)
        movedFiles = False
        while movedFiles == False:
            try:
                time.sleep(0.6)
                createDir(folder)  # Creates new folder with header

                # declaring were to dump osu map files
                source = f'C:/Users/{username}/Downloads/'
                destination = f'C:/Users/{username}/Desktop/OsuThingey/OsuFiles/{folder}/'
                allfiles = os.listdir(source)

                # attempts to move files from downloads to 'OsuFiles'
                for f in allfiles:
                    shutil.move(source + f, destination + f)
                dir_name = f'C:/Users/{username}/Desktop/OsuThingey/OsuFiles/{folder}/'
                test = os.listdir(dir_name)

                # removes all crdownload files
                for item in test:
                    if item.endswith(".crdownload"):
                        os.remove(os.path.join(dir_name, item))
                folder = num
                movedFiles = True
                break
            except Exception as exeption:
                # error ^^^^^ appears when windows cant move a file as it is not finnished downloading
                print(
                    f'Map ({num}) is still downloding, trying in 1.6 seconds')
                time.sleep(1)
        print(num)

print('Finnished with no errors')
input('Press enter to exit ->')
