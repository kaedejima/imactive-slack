# RUN FROM TERMINAL
# cd Documents/Waseda3rdYear/ProjectResearchB/slack_api
# python3 workspace_status.py


from datetime import datetime
import dlib

import os
from dotenv import load_dotenv
from datetime import date
import json
import time
import datetime
import pandas as pd

import slack_funcs

SF = slack_funcs.SlackDriver()
(id_list, name_list) = SF.users_list()

def track_presence():
  start_time = datetime.datetime.now()
  print(start_time)
  check_interval = 5
  long_work_time = 10
  col = ['Time']+id_list
  df = pd.DataFrame(columns=col)
  curr_dict = {s: {'status':'away', 'last_modified': start_time} for s in id_list}
  print(col)
  tmp_flag = False

  while True:
    current_time = datetime.datetime.now()
    elapsed_time = current_time - start_time
    print(elapsed_time)

    start_time = datetime.datetime.now()
    res_list = [current_time]
    for member_id, member_name in zip(id_list, range(0, len(name_list))):
        user_presence_data = SF.read_presence(member_id)
        current_status = user_presence_data['presence']
        res_list.append(current_status)
        # print(user_presence_data)
        if (current_status == 'active') and ((start_time - curr_dict[member_id]['last_modified']).seconds > long_work_time):
          print('active for long time...')
          SF.send_message(str(name_list[member_name])+ ' : ' + 'Let\' take a break!', member_id)
          curr_dict[member_id]['last_modified'] = start_time
          pass
        if(curr_dict[member_id]['status'] != current_status):
            print('changed!')
            curr_dict[member_id]['status'] = current_status
            curr_dict[member_id]['last_modified'] = start_time
    # print('reslist',res_list)
    df.loc[len(df)] = res_list
    # print(res_list)
    # print(curr_dict)
    # print(df)
    if len(df) > 11:
        df = df.drop(df.index[[0]])
        df.reset_index(drop=True,inplace=True)
    time.sleep(check_interval)
  return df

track_presence()