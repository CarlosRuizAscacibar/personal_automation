#copy the password
export=:TARGET_SERVER=localhost
export=:TARGET_PORT=58888

scp -P $TARGET_PORT pass.txt pi@$TARGET_SERVER:~/personal_automation/

scp -P $TARGET_PORT pi@$TARGET_SERVE:~/personal_automation/personal_automation.db personal_automation.db