import pygame
import numpy as np
import copy

pygame.init()

pygame.font.init()
fontBig = pygame.font.SysFont("Arial", 50)
fontSmall = pygame.font.SysFont("Arial", 20)


# zoomFactor = 1
clock = pygame.time.Clock()
camCoords = np.array([0, 0])


screen = pygame.display.set_mode((1800,1000))



image = pygame.image.load("lf_scaled.jpg")

groundSurface = pygame.Surface(image.get_size())


# def addTuple(a, b):
#     return tuple([a[i] + b[i] for i in range(len(a))])
#
# def subTuple(a, b):
#     return tuple([a[i] - b[i] for i in range(len(a))])
#
# def scaleTuple(a, b):
#     return tuple([a[i] * b for i in range(len(a))])
#
# def roundTuple(a):
#     return tuple([round(i) for i in a])

status = True
clicking = False
offset = np.array([0,0])
mouseDownPos = np.array([0,0])
mouseUpPos = np.array([0,0])

dots = {'0': {'position': [1433, 1679.3333333333333], 'connections': ['8', '9'], 'labels': []}, '1': {'position': [1228.5, 1679.3333333333333], 'connections': ['2', '8'], 'labels': []}, '2': {'position': [1136.0, 1679.3333333333333], 'connections': ['1', '3', '5'], 'labels': []}, '3': {'position': [1136.0, 1726.3333333333333], 'connections': ['2', '4', '5'], 'labels': []}, '4': {'position': [1200, 1726.3333333333333], 'connections': ['3'], 'labels': ['Toilet', 'Men']}, '5': {'position': [1048.0, 1726.3333333333333], 'connections': ['3', '6', '2'], 'labels': []}, '6': {'position': [1048.0, 1761.0], 'connections': ['5', '7'], 'labels': []}, '7': {'position': [1117, 1761.0], 'connections': ['6'], 'labels': ['Toilet', 'Women']}, '8': {'position': [1301, 1679.3333333333333], 'connections': ['1', '0'], 'labels': []}, '9': {'position': [1577.6666666666667, 1679.3333333333333], 'connections': ['0', '10', '11'], 'labels': []}, '10': {'position': [1577.6666666666667, 1854], 'connections': ['9', '85'], 'labels': ['LF8']}, '11': {'position': [1670.7, 1679.3333333333333], 'connections': ['9', '12'], 'labels': []}, '12': {'position': [1670.7, 1660.5], 'connections': ['11', '13', '14'], 'labels': []}, '13': {'position': [1704, 1660.5], 'connections': ['12'], 'labels': []}, '14': {'position': [1670.7, 1602.0], 'connections': ['12', '15', '21'], 'labels': []}, '15': {'position': [1739, 1602.0], 'connections': ['14', '16'], 'labels': []}, '16': {'position': [1938.0, 1602.0], 'connections': ['15', '17', '81'], 'labels': []}, '17': {'position': [2003.0, 1602.0], 'connections': ['16', '18'], 'labels': []}, '18': {'position': [2003.0, 1662], 'connections': ['17'], 'labels': ['Lecture Theatre', '1.1']}, '19': {'position': [1938.0, 1264.75], 'connections': ['20', '22', '81'], 'labels': ['LF9', 'Tooltill 0', 'Computer Lab']}, '20': {'position': [1695, 1264.75], 'connections': ['19', '21'], 'labels': []}, '21': {'position': [1670.7, 1264.75], 'connections': ['20', '14', '27'], 'labels': []}, '22': {'position': [2015.0, 1264.75], 'connections': ['19', '23'], 'labels': []}, '23': {'position': [2015.0, 1087.5], 'connections': ['22', '24'], 'labels': []}, '24': {'position': [1796.0, 1087.5], 'connections': ['23', '25'], 'labels': ['LF16', 'Tooltill 1', 'Computer Lab']}, '25': {'position': [1796.0, 915.5], 'connections': ['24', '26'], 'labels': []}, '26': {'position': [1670.7, 915.5], 'connections': ['25', '27', '34'], 'labels': []}, '27': {'position': [1670.7, 1116.3333333333333], 'connections': ['21', '26', '28'], 'labels': []}, '28': {'position': [1501, 1116.3333333333333], 'connections': ['27', '29'], 'labels': []}, '29': {'position': [1395.3333333333333, 1116.3333333333333], 'connections': ['28', '30', '31'], 'labels': ['LF39', 'Collab 1']}, '30': {'position': [1304, 1429], 'connections': ['29'], 'labels': []}, '31': {'position': [1395.3333333333333, 984], 'connections': ['29', '32'], 'labels': []}, '32': {'position': [1395.3333333333333, 861.6666666666666], 'connections': ['31', '33'], 'labels': ['LF34', 'Collab 2']}, '33': {'position': [1517, 861.6666666666666], 'connections': ['32', '34'], 'labels': []}, '34': {'position': [1670.7, 861.6666666666666], 'connections': ['33', '26', '35'], 'labels': []}, '35': {'position': [1670.7, 734.6666666666666], 'connections': ['34', '36', '37'], 'labels': []}, '36': {'position': [1517, 734.6666666666666], 'connections': ['35', '46'], 'labels': []}, '37': {'position': [1670.7, 651.25], 'connections': ['35', '38', '43', '47'], 'labels': []}, '38': {'position': [1717.4, 651.25], 'connections': ['37', '39', '40', '41'], 'labels': []}, '39': {'position': [1717.4, 705.5], 'connections': ['38'], 'labels': ['LF17', 'PGR Home']}, '40': {'position': [1717.4, 583], 'connections': ['38', '48'], 'labels': []}, '41': {'position': [1926.5, 651.25], 'connections': ['38', '42'], 'labels': []}, '42': {'position': [1926.5, 705.5], 'connections': ['41'], 'labels': ['LF15', 'PGR Lab']}, '43': {'position': [1609.0, 651.25], 'connections': ['37', '44'], 'labels': []}, '44': {'position': [1609.0, 576.5], 'connections': ['43', '45'], 'labels': []}, '45': {'position': [1471.5, 576.5], 'connections': ['44', '46'], 'labels': ['LF31', 'Computer Lab']}, '46': {'position': [1471.5, 734.6666666666666], 'connections': ['45', '36'], 'labels': []}, '47': {'position': [1670.7, 290.5833333333333], 'connections': ['37', '67', '69'], 'labels': []}, '48': {'position': [1717.4, 498.75], 'connections': ['40', '49', '50'], 'labels': []}, '49': {'position': [1717.4, 365.75], 'connections': ['48', '52'], 'labels': []}, '50': {'position': [1872.0, 498.75], 'connections': ['48', '51', '53'], 'labels': ['LF21']}, '51': {'position': [1872.0, 365.75], 'connections': ['50', '52', '55'], 'labels': []}, '52': {'position': [1796, 365.75], 'connections': ['51', '49'], 'labels': ['LF22']}, '53': {'position': [1911.5, 498.75], 'connections': ['50', '54', '60'], 'labels': []}, '54': {'position': [1911.5, 425.3333333333333], 'connections': ['53', '56'], 'labels': []}, '55': {'position': [1922.5, 365.75], 'connections': ['51', '56'], 'labels': []}, '56': {'position': [1922.5, 425.3333333333333], 'connections': ['55', '54', '57'], 'labels': []}, '57': {'position': [2013.3333333333333, 425.3333333333333], 'connections': ['56', '58'], 'labels': []}, '58': {'position': [2013.3333333333333, 366], 'connections': ['57', '59'], 'labels': []}, '59': {'position': [2013.3333333333333, 290.5833333333333], 'connections': ['58', '62', '63'], 'labels': []}, '60': {'position': [2055.0, 498.75], 'connections': ['53', '61'], 'labels': []}, '61': {'position': [2055.0, 419], 'connections': ['60'], 'labels': []}, '62': {'position': [2050, 290.5833333333333], 'connections': ['59'], 'labels': ['LF23']}, '63': {'position': [1969.0, 290.5833333333333], 'connections': ['59', '64', '65'], 'labels': []}, '64': {'position': [1969.0, 246.5], 'connections': ['63'], 'labels': ['LF24']}, '65': {'position': [1841.5, 290.5833333333333], 'connections': ['63', '66', '67'], 'labels': []}, '66': {'position': [1841.5, 246.5], 'connections': ['65'], 'labels': ['LF25']}, '67': {'position': [1718.5, 290.5833333333333], 'connections': ['65', '68', '47'], 'labels': []}, '68': {'position': [1718.5, 246.5], 'connections': ['67'], 'labels': ['LF26']}, '69': {'position': [1593.0, 290.5833333333333], 'connections': ['47', '70', '71'], 'labels': []}, '70': {'position': [1593.0, 246.5], 'connections': ['69'], 'labels': ['LF27']}, '71': {'position': [1467.5, 290.5833333333333], 'connections': ['69', '72', '73'], 'labels': []}, '72': {'position': [1467.5, 246.5], 'connections': ['71'], 'labels': ['LF28']}, '73': {'position': [1344.0, 290.5833333333333], 'connections': ['71', '74', '75'], 'labels': []}, '74': {'position': [1344.0, 246.5], 'connections': ['73'], 'labels': ['LF29']}, '75': {'position': [1215, 290.5833333333333], 'connections': ['73', '78'], 'labels': []}, '76': {'position': [1128.0, 290.5833333333333], 'connections': ['77', '78'], 'labels': []}, '77': {'position': [1128.0, 339], 'connections': ['76'], 'labels': []}, '78': {'position': [1178.0, 290.5833333333333], 'connections': ['75', '76', '79'], 'labels': []}, '79': {'position': [1178.0, 461.0], 'connections': ['78'], 'labels': []}, '81': {'position': [1938.0, 1437.3333333333333], 'connections': ['16', '19', '82'], 'labels': []}, '82': {'position': [1993, 1437.3333333333333], 'connections': ['81', '83'], 'labels': []}, '83': {'position': [2013.0, 1437.3333333333333], 'connections': ['82'], 'labels': ['LF12']}, '85': {'position': [1577.6666666666667, 1983.5], 'connections': ['10', '86'], 'labels': []}, '86': {'position': [1373, 1983.5], 'connections': ['85'], 'labels': ['LF7', 'Research Lab']}}

dotNum = 0
for d in dots:
    if int(d) > int(dotNum):
        dotNum = int(d)

workingNum = "-1"
isTyping = False
dHeld = False
selected = []
undoStack = []
typedText = ""

def screenToWorld(coords):
    return coords + camCoords + offset

while (status):
    mousePos = np.array(pygame.mouse.get_pos())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicking = True
            mouseDownPos = mousePos
        elif event.type == pygame.MOUSEBUTTONUP:
            clicking = False
            mouseUpPos = mousePos
            camCoords = camCoords - offset
            offset = (0, 0)
        elif event.type == pygame.KEYDOWN:
            # w to create dot
            # a to create dot that connects to working dot
            # s to set working dot to dot being moused over
            # d to move working dot to mouse position
            # e to delete working dot
            # q to connect working dot to moused over dot
            # r to add label to working dot (typed)
            # f to remove label from working dot
            # l to load from file ----- eh no need
            # t to select multiple dots
            # x to align dots horizontally
            # y to align dots vertically
            # u to undo
            # z to delete connection between 2 selected dots
            # arrow keys to nudge selection
            if not isTyping:
                undoStack.append(copy.deepcopy(dots))
                if event.key == pygame.K_w:
                    dots[str(dotNum)] = {"position":screenToWorld(mousePos).tolist(), "connections": [], "labels": []}
                    workingNum = str(dotNum)
                    dotNum += 1
                elif event.key == pygame.K_a:
                    if workingNum != "-1":
                        dots[str(dotNum)] = {"position":screenToWorld(mousePos).tolist(), "connections": [workingNum], "labels": []}
                        dots[workingNum]["connections"].append(str(dotNum))
                        workingNum = str(dotNum)
                        dotNum += 1
                elif event.key == pygame.K_s:
                    selected = []
                    coords = screenToWorld(mousePos)
                    lowest = 999999
                    lowestDot = -1
                    for dot in dots:
                        dist = np.linalg.norm(coords - dots[dot]["position"])
                        if dist < lowest:
                            lowest = dist
                            lowestDot = dot
                    if lowestDot != -1 and lowest <= 20:
                        workingNum = lowestDot
                elif event.key == pygame.K_d:
                    if workingNum != "-1":
                        dHeld = True
                elif event.key == pygame.K_e:
                    if workingNum in dots:
                        dots.pop(workingNum)
                        for dot in dots:
                            if workingNum in dots[dot]["connections"]:
                                dots[dot]["connections"].remove(workingNum)
                        workingNum = "-1"
                elif event.key == pygame.K_q:
                    coords = screenToWorld(mousePos)
                    lowest = 999999
                    mousedDot = -1
                    for dot in dots:
                        dist = np.linalg.norm(coords - dots[dot]["position"])
                        if dist < lowest:
                            lowest = dist
                            mousedDot = dot
                    if mousedDot != -1 and lowest <= 20:
                        dots[mousedDot]["connections"].append(workingNum)
                        dots[workingNum]["connections"].append(mousedDot)
                        workingNum = mousedDot
                elif event.key == pygame.K_r:
                    if workingNum in dots:
                        isTyping = True
                        typedText = ""
                elif event.key == pygame.K_f:
                    if len(dots[workingNum]["labels"]) > 0:
                        dots[workingNum]["labels"].pop()
                elif event.key == pygame.K_t:
                    workingNum = "-1"
                    coords = screenToWorld(mousePos)
                    lowest = 999999
                    mousedDot = -1
                    for dot in dots:
                        dist = np.linalg.norm(coords - dots[dot]["position"])
                        if dist < lowest:
                            lowest = dist
                            mousedDot = dot
                    if mousedDot != -1 and lowest <= 20:
                        if mousedDot in selected:
                            selected.remove(mousedDot)
                        else:
                            selected.append(mousedDot)
                elif event.key == pygame.K_x:
                    if len(selected) > 0:
                        exes = [dots[ex]["position"][0] for ex in selected]
                        avg = sum(exes)/len(exes)
                        for ex in selected:
                            dots[ex]["position"][0] = avg
                elif event.key == pygame.K_y:
                    if len(selected) > 0:
                        ys = [dots[y]["position"][1] for y in selected]
                        avg = sum(ys)/len(ys)
                        for y in selected:
                            dots[y]["position"][1] = avg
                elif event.key == pygame.K_u:
                    undoStack.pop()
                    if len(undoStack) > 1:
                        dots = undoStack.pop()
                elif event.key == pygame.K_z:
                    if len(selected) == 2:
                        if selected[1] in dots[selected[0]]["connections"]:
                            dots[selected[0]]["connections"].remove(selected[1])
                            dots[selected[1]]["connections"].remove(selected[0])
                elif event.key == pygame.K_UP:
                    for i in selected:
                        dots[i]["position"][1] -= 0.5
                elif event.key == pygame.K_DOWN:
                    for i in selected:
                        dots[i]["position"][1] += 0.5
                elif event.key == pygame.K_LEFT:
                    for i in selected:
                        dots[i]["position"][0] -= 0.5
                elif event.key == pygame.K_RIGHT:
                    for i in selected:
                        dots[i]["position"][0] += 0.5


            elif event.key == pygame.K_RETURN:
                isTyping = False
                dots[workingNum]["labels"].append(typedText)
            else:
                typedText += event.unicode





            # print(undoStack)
            print(dots)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                dHeld = False



        if dHeld:
            dots[workingNum]["position"] = screenToWorld(mousePos).tolist()



        # elif event.type == pygame.MOUSEWHEEL:
        #     factor = 1.1**event.y
        #     oldZoom = zoomFactor
        #     zoomFactor *= factor
        #
        #     mouseWorldOld = addTuple(camCoords, scaleTuple(mousePos, 1 / oldZoom))
        #     mouseWorldNew = addTuple(camCoords, scaleTuple(mousePos, 1 / zoomFactor))
        #     diff = subTuple(mouseWorldNew,mouseWorldOld)
        #     print(roundTuple(diff))
        #     camCoords = subTuple(camCoords, diff)



    if clicking:
        offset = mousePos - mouseDownPos




    screen.fill((0,0,0))
    groundSurface.blit(image, (0, 0))

    for dot in dots:
        for conn in dots[dot]["connections"]:
            pygame.draw.line(groundSurface, (255,0,255), dots[dot]["position"], dots[conn]["position"], 2)


    for dot in dots:
        if dot in selected:
            pygame.draw.circle(groundSurface, (255, 165, 0), dots[dot]["position"], 8)
        elif dot == str(workingNum):
            pygame.draw.circle(groundSurface, (0, 0, 255), dots[dot]["position"], 8)
        else:
            pygame.draw.circle(groundSurface, (255, 0, 0), dots[dot]["position"], 6)
        if len(dots[dot]["labels"]) > 0:
            textSurface = fontSmall.render(dots[dot]["labels"][-1], True, (0,0,255))
            groundSurface.blit(textSurface, dots[dot]["position"] + np.array([-textSurface.get_width()/2, textSurface.get_height()/2]))
        textSurface = fontSmall.render(str(dot), True, (0, 255, 0))
        groundSurface.blit(textSurface, dots[dot]["position"]+np.array([-textSurface.get_width()/2, -textSurface.get_height()]))



    # transformed = pygame.transform.scale_by(groundSurface, zoomFactor)


    screen.blit(groundSurface, -camCoords + offset)
    if isTyping:
        textSurface = fontBig.render(f'Label: "{typedText}"', True, (0, 0, 255))
        screen.blit(textSurface, (900 - textSurface.get_width()/2, 600))
    pygame.display.flip()

    clock.tick(60)





pygame.quit()