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
id_and_name = dict(zip(id_list, name_list))

SF.send_message('YEL: active for 10mins\n Kenta: active for 30mins', '#imactive-response')

def track_presence():
  start_time = datetime.datetime.now()
  print(start_time)
  check_interval = 30
  long_work_time = 1500
  df_size = 11
  all_status_view_time = 1800
  col = ['Time']+id_list
  df = pd.DataFrame(columns=col)
  curr_dict = {s: {'status':'away', 'continuous_active': False, 'last_continuous': start_time, 'last_modified': start_time} for s in id_list}
  print(col)
  tmp_flag = False

  while True:
    current_time = datetime.datetime.now()
    elapsed_time = current_time - start_time
    print(elapsed_time)

    # start_time = datetime.datetime.now()
    res_list = [current_time]
    for member_id, member_name in zip(id_list, range(0, len(name_list))):
        user_presence_data = SF.read_presence(member_id)
        current_status = user_presence_data['presence']
        res_list.append(current_status)
        # print(user_presence_data)
        if (current_status == 'active') and ((start_time - curr_dict[member_id]['last_continuous']).seconds > long_work_time):
          if (curr_dict[member_id]['countinuous_active']):
            curr_dict[member_id]['last_continuous'] = start_time
            # if (curr_dict[member_id]['last_continuous'].seconds > ):
          curr_dict[member_id]['countinuous_active'] = True
          print('active for long time...')
          SF.send_message(str(name_list[member_name])+ ' : ' + 'Let\' take a break!', member_id)

        if(curr_dict[member_id]['status'] != current_status):
            print('changed!')
            curr_dict[member_id]['status'] = current_status
            curr_dict[member_id]['last_continuous'] = start_time

    # if (elapsed_time.seconds > all_status_view_time):
    active_members = [k for k, v in curr_dict.items() if v['status'] == 'active']
    mes = ''
    for (name, id, v) in zip(id_and_name.items(),id_and_name.keys(),active_members):
        if (v == id):
          duration = current_time - curr_dict[id]['last_modified']
          mes += '{0}: active for {0}min\n'.format(name, duration)
    SF.send_message(mes, '#imactive-response')
    elapsed_time = current_time
    # # print('reslist',res_list)
    df.loc[len(df)] = res_list
    # print(res_list)
    print(curr_dict)
    # print(df)
    if len(df) > df_size:
        df = df.drop(df.index[[0]])
        df.reset_index(drop=True,inplace=True)
    time.sleep(check_interval)
  return df

# track_presence()