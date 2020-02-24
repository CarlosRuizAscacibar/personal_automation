#copy the password
export TARGET_SERVER=192.168.0.49
export TARGET_PORT=22

scp -P $TARGET_PORT pass.txt pi@$TARGET_SERVER:~/personal_automation/

scp pi@$TARGET_SERVER:~/personal_automation/personal_automation.db personal_automation.db