import time
import random
import android

droid = android.Android()
messages = []
with open("/sdcard/txt_list.txt") as file:
	for line in file:
		messages.append(line.strip())

def checkNumbers(filename):
	returnList = []
	with open(filename) as file:
		for line in file:
			returnList.append(line.strip())
	return tuple(returnList)


messageCount = droid.smsGetMessageCount(True)[1]

targetNumbers = checkNumbers("/sdcard/target_respond_list.txt")

print "Starting with " + str(messageCount) + " unread messages"
print "Message list:"
print messages
print "Target numbers:"
print targetNumbers

loopCount = -1

while True:
	loopCount += 1
	if droid.smsGetMessageCount(True)[1] > messageCount:
		number = droid.smsGetMessages(True)[1].pop()['address'].replace('+', '')
		print "Got a message from: " + number 
		if number in targetNumbers:
			print "Sending crap to it..."
			droid.smsSend(number, messages[random.randrange(0, len(messages))])

	messageCount = droid.smsGetMessageCount(True)[1]

	if loopCount is 30:	# Check for number change every minute
		tmpList = checkNumbers("/sdcard/target_respond_list.txt")
		if tmpList != targetNumbers:
			print "Target numbers changed"
			targetNumbers = tmpList
		loopCount = 0

	time.sleep(2)