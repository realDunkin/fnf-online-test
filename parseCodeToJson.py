import json

assetName = input("Enter Asset Name: ")
print("")
animsToSplit = input("Enter Animation Data to Parse: ")
print("")
offsetsToSplit = input("Enter Offset Data to Parse: ")
print("")
animType = input("Enter Dance Type [0 = Default, 1 = GF Type]: ")
print("")
startingAnim = input("Enter Starting Animation: ")
print("")
singDuration = input("Enter Sing Duration: ")

print("\n")
				
splitAnims = animsToSplit.replace('\t', '').replace('\n', '').split(';')
del splitAnims[-1]

daDictionary = {"asset": assetName, "barColor": "#FFFFFF", "noAntialiasing": False, "flip_x": False, "scale": 1, "animType": int(animType), "startingAnim": startingAnim, "singDuration": float(singDuration), "animations": []}

for item in splitAnims:
    animDictionary = {}
    tempAnim = item.replace("'", "").replace('"', '')
    animData = tempAnim.replace("animation.addByIndices", "").replace('animation.addByPrefix', '').replace('(', '').replace(')', '').split(',')
    if "animation.addByPrefix" in tempAnim:
        animDictionary['name'] = animData[0].lstrip()
        animDictionary['prefix'] = animData[1].lstrip()
        animDictionary['offsets'] = {'X': 0, 'Y': 0}
        animDictionary['waitUntilFinished'] = False
        animDictionary['frameIndices'] = []
        try:
            animDictionary['fps'] = int(animData[len(animData) - 2])
        except:
            animDictionary['fps'] = int(animData[len(animData) - 1])
        try:
            if animData[len(animData) - 1] == True:
                animDictionary['looping'] = True
            else:
                animDictionary['looping'] = False
        except:
            animDictionary['looping'] = False
    elif "animation.addByIndices" in tempAnim:
        indicesArray = []
        for i in range(2, len(animData) - 3):
            indicesArray.append(int(animData[i].replace('[', '').replace(']', '').replace(' ', '')))
        animDictionary['name'] = animData[0].lstrip()
        animDictionary['prefix'] = animData[1].lstrip()
        animDictionary['offsets'] = {'X': 0, 'Y': 0}
        animDictionary['waitUntilFinished'] = False
        animDictionary['frameIndices'] = indicesArray
        try:
            animDictionary['fps'] = int(animData[len(animData) - 2])
        except:
            animDictionary['fps'] = int(animData[len(animData) - 1])
        try:
            if animData[len(animData) - 1] == True:
                animDictionary['looping'] = True
            else:
                animDictionary['looping'] = False
        except:
            animDictionary['looping'] = False
    daDictionary['animations'].append(animDictionary)

splitOffsets = offsetsToSplit.replace('\t', '').replace('\n', '').split(';')
del splitOffsets[-1]

for item in splitOffsets:
    tempOffset = item.replace("'", "").replace('"', '')
    offsetData = tempOffset.replace("addOffset", "").replace('(', '').replace(')', '').split(',')
    offsetData[0] = offsetData[0].lstrip()
    for anim in daDictionary['animations']:
        if anim['name'] == offsetData[0]:
            try:
                anim['offsets']['X'] = int(offsetData[1])
            except:
                pass
            try:
                anim['offsets']['Y'] = int(offsetData[2])
            except:
                pass

filename = input("Enter Character Name: ")

with open(f'data/characters/{filename}.json', 'w') as json_file:
    json.dump(daDictionary, json_file, indent=4)