import pyodbc
conn = pyodbc.connect("DSN=Baseball")


def pullOffStat(tableName, retroId):
    conn = pyodbc.connect("DSN=Baseball")
    cursor = conn.cursor()
    command = "select nameFirst, nameLast from People where retroID = ?"
    playerId = cursor.execute(command, retroId).fetchone()
    player = str(playerId)
    player = player.replace('(', '')
    player = player.replace(')', '')
    player = player.replace(',', '')
    player = player.replace('\'', '')
    player = player.replace('\"', '')
    command = "select OPS, wRCplus from %s where name = ?" % tableName
    offStat = cursor.execute(command, player).fetchone()
    playStat = str(offStat)
    if playStat == 'None':
        print(player + " Year: " + tableName)
    playStat = playStat.replace('(', '')
    playStat = playStat.replace(')', '')
    return str(playStat)


def pullPitchStat(year, retroId):
    tableName = "PitchingAdvanced" + str(year)
    conn = pyodbc.connect("DSN=Baseball")
    cursor = conn.cursor()
    command = "select nameFirst, nameLast from People where retroID = ?"
    playerId = cursor.execute(command, retroId).fetchone()
    player = str(playerId)
    player = player.replace('(', '')
    player = player.replace(')', '')
    player = player.replace(',', '')
    player = player.replace('\'', '')
    command = "select SIERA from %s where name = ?" % tableName
    offStat = cursor.execute(command, player).fetchone()
    playStat = str(offStat)
    playStat = playStat.replace('(', '')
    playStat = playStat.replace(')', '')
    return str(playStat)


def readGameLog(gamelogYear):
    basePath = "C:\\Users\\Andrew Swaim\\Documents\\Retrosheet Game Logs\\GL"
    filepath = basePath + str(gamelogYear) + ".txt"
    file = open(filepath, 'r')
    isHomeTeamId = 0
    tableName = "BattingAdvanced" + str(gamelogYear)
    homePitcherId = 103
    visitingPitcherId = 101
    visitorId = [105,108,111,114,117,120,123,126,129]
    homeId = [132,135,138,141,144,147,150,153,156]
    trainingStatArray = []
    gameNum = 0
    for line in file:
        isHomeTeamId = 0
        gameStatsArray = []
        stripLine = line.replace('\"', '')
        gameArray = stripLine.split(',')
        if gameArray[3] == 'HOU' or gameArray[6] == 'HOU':
            playerNF = 0
            gameNum += 1
            print("Game: " + str(gameNum))
            statString = ""
            if gameArray[6] == "HOU":
                isHomeTeamId = 1
            gameStatsArray.append(isHomeTeamId)
            if isHomeTeamId == 1:
                pitchStat = pullPitchStat(gamelogYear, gameArray[homePitcherId])
                if pitchStat == 'None':
                    continue
                siera = pitchStat.split(',')
                gameStatsArray.append(float(siera[0]))
                for id in homeId:
                    offStat = pullOffStat(tableName, gameArray[id])
                    if offStat == 'None':
                        playerNF = 1
                        break
                    offStatArray = offStat.split(',')
                    gameStatsArray.append(float(offStatArray[0].strip()))
                    gameStatsArray.append(float(offStatArray[1].strip()))
                if playerNF == 1:
                    continue
                for id in visitorId:
                    offStat = pullOffStat(tableName, gameArray[id])
                    if offStat == 'None':
                        playerNF = 1
                        break
                    offStatArray = offStat.split(',')
                    gameStatsArray.append(float(offStatArray[0].strip()))
                    gameStatsArray.append(float(offStatArray[1].strip()))
                if playerNF == 1:
                    continue
                pitchStat = pullPitchStat(gamelogYear, gameArray[visitingPitcherId])
                if pitchStat == 'None':
                    continue
                siera = pitchStat.split(',')
                gameStatsArray.append(float(siera[0]))
            else:
                visitpitchStat = pullPitchStat(gamelogYear, gameArray[visitingPitcherId])
                if visitpitchStat == 'None':
                    continue
                siera = visitpitchStat.split(',')
                gameStatsArray.append(float(siera[0]))
                for id in visitorId:
                    visitOffStat = pullOffStat(tableName, gameArray[id])
                    if visitOffStat == 'None':
                        playerNF = 1
                        break
                    visitoffStatArray = visitOffStat.split(',')
                    gameStatsArray.append(float(visitoffStatArray[0].strip()))
                    gameStatsArray.append(float(visitoffStatArray[1].strip()))
                if playerNF == 1:
                    continue
                for id in homeId:
                    homeOffStat = pullOffStat(tableName, gameArray[id])
                    if homeOffStat == 'None':
                        playerNF = 1
                        break
                    homeOffStatArray = homeOffStat.split(',')
                    gameStatsArray.append(float(homeOffStatArray[0].strip()))
                    gameStatsArray.append(float(homeOffStatArray[1].strip()))
                if playerNF == 1:
                    continue
                homepitchStat = pullPitchStat(gamelogYear, gameArray[homePitcherId])
                if homepitchStat == 'None':
                    continue
                siera = homepitchStat.split(',')
                gameStatsArray.append(float(siera[0]))
            for stat in gameStatsArray:
                statString += str(stat) + ','
            print(str(len(gameStatsArray )))
            visitScore = gameArray[9]
            homeScore = gameArray[10]
            if isHomeTeamId == 1:
                if homeScore > visitScore:
                    statString += "1"
                else:
                    statString += "0"
            else:
                if visitScore > homeScore:
                    statString += "1"
                else:
                    statString += "0"
            trainingStatArray.append(statString)
    return trainingStatArray


game = 1
trainingPath = "C:\\Users\\Andrew Swaim\\Documents\\ANNE Homework\\trainingSet2.txt"
testPath = "C:\\Users\\Andrew Swaim\\Documents\\ANNE Homework\\testSet2.txt"
file = open(trainingPath, 'w')
testFile = open(testPath, 'w')
TrainingSet = []
trainingYears = [2013, 2014, 2015, 2016, 2017]
for year in trainingYears:
    TrainingSet.append(readGameLog(year))
TestSet = readGameLog(2018)
print("Training Set:\n")
for set in TrainingSet:
    for log in set:
        file.write(log + "\n")
        print("Game: " + str(game) + ": " + log)
        game += 1
for log in TestSet:
    testFile.write(log + "\n")
    print("Game: " + str(game) + ": " + log)
    game += 1
file.close()
testFile.close()
