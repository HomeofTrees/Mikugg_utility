#!/usr/bin/env python3
import json
import argparse
import os.path
import copy
from pathlib import Path

def checkConsistency(jsonObj):

	#collect all ID's from the novel definition
	characterslist = []
	for char in jsonObj['novel']['characters']:
		characterslist.append({'id':char['id'], 'name':char['name']})

	sceneslist = []
	for scene in jsonObj['novel']['scenes']:
		sceneslist.append({'id':scene['id'], 'name':scene['name']})

	startslist = []
	for start in jsonObj['novel']['starts']:
		startslist.append({'id':start['id'], 'name':start['title']})

	lorebookslist = []
	for lorebook in jsonObj['novel']['lorebooks']:
		lorebookslist.append({'id':lorebook['id'], 'name':lorebook['name']})

	objectiveslist = []
	for objective in jsonObj['novel']['objectives']:
		objectiveslist.append({'id':objective['id'], 'name':objective['name']})
	#

	#collect all ID's that appear in narration
	#all scenes used
	narrationsceneIDs = []
	for _key, value in jsonObj['narration']['interactions'].items():
		narrationsceneIDs.append(value['sceneId'])
	
	#all characters used
	narrationcharacterIDs = []
	for _key, value in jsonObj['narration']['responses'].items():
		narrationcharacterIDs.append(value['selectedCharacterId'])
		for char in value['characters']:
			narrationcharacterIDs.append(char['characterId'])
	narrationcharacterIDs = list(set(narrationcharacterIDs))
	#all parentResponseIDs
	responseIDs = []
	parentresponseIDs = []
	for _key, value in jsonObj['narration']['interactions'].items():
		parentresponseIDs.append(value['parentResponseId'])
		responseIDs.append(value['id'])
		responseIDs.extend(value['responsesId'])
	#all responseIDs

	#TODO check ['narration']['responses']['suggestedScenes']
	#

	#check used sceneIDs
	for id in narrationsceneIDs:
		if id in [scene['id'] for scene in sceneslist]:
			continue
		else:
			print(f"WARN: Following scene is used in narration but not defined in novel <{id}>")
	#check used characterIDs
	for id in narrationcharacterIDs:
		if id in [char['id'] for char in characterslist]:
			continue
		else:
			print(f"WARN: Following character is used in narration but not defined in novel <{id}>")
	#check all parentresponseIDs whether they have a matching responseID or startID
	for id in parentresponseIDs:
		if id in responseIDs:
			continue
		if id in [start['id'] for start in startslist]:
			continue
		print(f"WARN: Following response is used in narration but has no parent response <{id}>")

#################
##   END FUN   ##
#################

parser = argparse.ArgumentParser()
parser.add_argument("old_narration", type=argparse.FileType('r', encoding='utf-8'), help="Old narration json file that should be update")
parser.add_argument("new_narration", type=argparse.FileType('r', encoding='utf-8'), help="New novel or narration json file used as a basis for updating")
#TODO allow to pass novel json as argument for new_narration
args = parser.parse_args()

oldjsonname = args.old_narration.name
updatedjsonname = '{}.updated.json'.format(Path(oldjsonname).stem)

oldjson = json.load(args.old_narration)
args.old_narration.close()
newjson = json.load(args.new_narration)
args.new_narration.close()


updatedjson = copy.deepcopy(oldjson)
updatedjson['novel'] = copy.deepcopy(newjson['novel'])
try:
	#updatedjson['inventory'] = copy.deepcopy(newjson['inventory'])
	#updatedjson['version'] = copy.deepcopy(newjson['version'])
	updatedjson['objectives'] = copy.deepcopy(newjson['objectives'])
except KeyError:
	pass


#write updated json to file
with open(updatedjsonname, 'w') as f:
	json.dump(updatedjson, f)
print("Updated narration file at: " + os.path.abspath(updatedjsonname))


#TODO finish consistency check and activate call
checkConsistency(updatedjson)
