#!/usr/bin/env python3

import os, sys, re
from datetime import datetime

log_file = list()

# find all config files
def conf_files(path):
    config_files = list()
    for pd, directories, files in os.walk(path):
        for file in files:
            if file.endswith('.conf'):
            	fname = os.path.join(pd, file)
            	config_files.append(fname)
    return config_files

# check config file for a setting
def check_file(file, content):
	re_content = r'\b' + content + r'\b'
	with open(file, 'r') as x:
		for lines in x:
			if re.match(re_content, lines):
				return True

# function to find and replace lines in config files
def find_replace(file, item, new_line):
	rewritten_file = []
	re_item = r'\b' + re.escape(item) + r'\b'
	with open(file, 'r') as open_file:
		for lines in open_file:
			if re.match(re_item, lines):
				rewritten_file.append(new_line + '\n')
			else:
				rewritten_file.append(lines)
	with open(file, 'w+') as new_config:
                for lines in rewritten_file:
                        new_config.write(lines)

# generate a list of config files with the setting to change
def get_working_list(f_list, setting):
	working_list = list()
	for names in f_list:
		if check_file(names, setting):
			working_list.append(names)
	return working_list

# change the setting with proper function
def change_setting(w_list, setting, new_setting):
	for items in w_list:
		print(items)
		find_replace(items, setting, new_setting)
		add_to_log(items, new_setting)
	w_list.clear()

# add setting change to the log file
def add_to_log(file, new_setting):
	global log_file
	dnow = datetime.now()
	dtnow = str(dnow)
	log_line = dtnow + ': ' + file + ': ' + 'Changed setting to: ' + new_setting
	return log_file.append(log_line)

# prompt user to make change to settings
def user_prompt_settings(setting, url, new_setting):
	print(f'{setting}: Do you want to change setting to: {new_setting}' + '\n' + url)
	yes_no = input('Would you like to change this setting?[Y/n]: ')
	while yes_no != 'Y' and yes_no != 'y' and yes_no != 'N' and yes_no != 'n':
		yes_no = input('Would you like to change this setting?[Y/n]: ')
	if yes_no == 'Y' or yes_no == 'y':
		return True
	elif yes_no == 'N' or yes_no == 'n':
		return False


def main():
	# directroy of apache config files
	directory = sys.argv[1]
	# find all config files
	file_list = conf_files(directory)

	# Server Tokens setting
	setting = 'ServerTokens'
	bp_setting = 'ServerTokens Prod'
	url = 'https://apache-patchy.gitbook.io/guide/info-leakage'
	user_change = user_prompt_settings(setting, url, bp_setting)
	if user_change:
		working_list = get_working_list(file_list, setting)
		change_setting(working_list, setting, bp_setting)
		working_list.clear()

	# Server signature setting
	setting = 'ServerSignature'
	bp_setting = 'ServerSignature Off'
	url = 'https://apache-patchy.gitbook.io/guide/info-leakage'
	user_change = user_prompt_settings(setting, url, bp_setting)
	if user_change:
		working_list = get_working_list(file_list, setting)
		change_setting(working_list, setting, bp_setting)
		working_list.clear()

	# Keep Alive setting
	setting = 'KeepAlive'
	bp_setting = 'KeepAlive On'
	url = 'https://apache-patchy.gitbook.io/guide/info-leakage'
	user_change = user_prompt_settings(setting, url, bp_setting)
	if user_change:
		working_list = get_working_list(file_list, setting)
		change_setting(working_list, setting, bp_setting)
		working_list.clear()

	# ETag settings
	setting = 'FileETag'
	bp_setting = 'FileETag None'
	url = 'PLACEHOLDER'
	user_change = user_prompt_settings(setting, url, bp_setting)
	if user_change:
		working_list = get_working_list(file_list, setting)
		change_setting(working_list, setting, bp_setting)
		working_list.clear()

	# Timeout settings
	setting = 'Timeout'
	bp_setting = 'Timeout <TIME IN SECONDS>'
	url = 'PLACEHOLDER'
	user_change = user_prompt_settings(setting, url, bp_setting)
	if user_change:
		working_list = get_working_list(file_list, setting)
		user_def = input('Enter an amount of Timeout setting in seconds: ')
		bp_setting = 'Timeout ' + user_def
		change_setting(working_list, setting, bp_setting)
		working_list.clear()

	# Max Keep Alive Requests
	setting = 'MaxKeepAliveRequests'
	bp_setting = 'MaxKeepAliveRequests 0'
	url = 'PLACEHOLDER'
	user_change = user_prompt_settings(setting, url, bp_setting)
	if user_change:
		working_list = get_working_list(file_list, 'MaxKeepAliveRequests')
		change_setting(working_list, 'MaxKeepAliveRequests', 'MaxKeepAliveRequests 0')
		working_list.clear()

	# Keep Alive Timeout
	setting = 'KeepAliveTimeout'
	bp_setting = 'KeepAliveTimeout <TIME IN SECONDS>'
	url = 'PLACEHOLDER'
	user_change = user_prompt_settings(setting, url, bp_setting)
	if user_change:
		working_list = get_working_list(file_list, setting)
		user_def = input('Enter Keep ALive Timeout setting: ')
		bp_setting = 'KeepAliveTimeout ' + user_def
		change_setting(working_list, setting, bp_setting)
		working_list.clear()

	# write the log file
	with open('log_file.log', 'w+') as final_log:
		for events in log_file:
			final_log.write(events + '\n')


if __name__ == "__main__":
	main()