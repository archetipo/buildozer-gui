#!/usr/bin/python
#-*- coding:utf-8 -*-
import string,os,sys

class Android_Build_o():
	def __init__(self):
		self.arg_list=[]
		self.prj_path=''
		self.permissions_list=["ACCESS_CHECKIN_PROPERTIES" ,
								"ACCESS_COARSE_LOCATION" ,
								"ACCESS_FINE_LOCATION" ,
								"ACCESS_LOCATION_EXTRA_COMMANDS" ,
								"ACCESS_MOCK_LOCATION" ,
								"ACCESS_NETWORK_STATE" ,
								"ACCESS_SURFACE_FLINGER" ,
								"ACCESS_WIFI_STATE" ,
								"ACCOUNT_MANAGER" ,
								"AUTHENTICATE_ACCOUNTS" ,
								"BATTERY_STATS" ,
								"BIND_APPWIDGET" ,
								"BIND_DEVICE_ADMIN" ,
								"BIND_INPUT_METHOD" ,
								"BIND_REMOTEVIEWS" ,
								"BIND_WALLPAPER" ,
								"BLUETOOTH" ,
								"BLUETOOTH_ADMIN" ,
								"BRICK" ,
								"BROADCAST_PACKAGE_REMOVED" ,
								"BROADCAST_SMS" ,
								"BROADCAST_STICKY" ,
								"BROADCAST_WAP_PUSH" ,
								"CALL_PHONE",
								"CALL_PRIVILEGED" ,
								"CAMERA",
								"CHANGE_COMPONENT_ENABLED_STATE" ,
								"CHANGE_CONFIGURATION" ,
								"CHANGE_NETWORK_STATE" ,
								"CHANGE_WIFI_MULTICAST_STATE" ,
								"CHANGE_WIFI_STATE" ,
								"CLEAR_APP_CACHE" ,
								"CLEAR_APP_USER_DATA" ,
								"CONTROL_LOCATION_UPDATES" ,
								"DELETE_CACHE_FILES" ,
								"DELETE_PACKAGES" ,
								"DEVICE_POWER" ,
								"DIAGNOSTIC" ,
								"DISABLE_KEYGUARD" ,
								"DUMP" ,
								"EXPAND_STATUS_BAR" ,
								"FACTORY_TEST" ,
								"FLASHLIGHT" ,
								"FORCE_BACK" ,
								"GET_ACCOUNTS" ,
								"GET_PACKAGE_SIZE" ,
								"GET_TASKS" ,
								"GLOBAL_SEARCH" ,
								"HARDWARE_TEST" ,
								"INJECT_EVENTS" ,
								"INSTALL_LOCATION_PROVIDER" ,
								"INSTALL_PACKAGES" ,
								"INTERNAL_SYSTEM_WINDOW" ,
								"INTERNET",
								"KILL_BACKGROUND_PROCESSES" ,
								"MANAGE_ACCOUNTS" ,
								"MANAGE_APP_TOKENS" ,
								"MASTER_CLEAR" ,
								"MODIFY_AUDIO_SETTINGS" ,
								"MODIFY_PHONE_STATE" ,
								"MOUNT_FORMAT_FILESYSTEMS" ,
								"MOUNT_UNMOUNT_FILESYSTEMS" ,
								"NFC" ,
								"PROCESS_OUTGOING_CALLS" ,
								"READ_CALENDAR" ,
								"READ_CONTACTS" ,
								"READ_FRAME_BUFFER" ,
								"READ_HISTORY_BOOKMARKS" ,
								"READ_INPUT_STATE" ,
								"READ_LOGS" ,
								"READ_PHONE_STATE" ,
								"READ_SMS" ,
								"READ_SYNC_SETTINGS" ,
								"READ_SYNC_STATS" ,
								"REBOOT" ,
								"RECEIVE_BOOT_COMPLETED" ,
								"RECEIVE_MMS" ,
								"RECEIVE_SMS" ,
								"RECEIVE_WAP_PUSH" ,
								"RECORD_AUDIO" ,
								"REORDER_TASKS" ,
								"RESTART_PACKAGES" ,
								"SEND_SMS" ,
								"SET_ACTIVITY_WATCHER" ,
								"SET_ALARM" ,
								"SET_ALWAYS_FINISH" ,
								"SET_ANIMATION_SCALE" ,
								"SET_DEBUG_APP" ,
								"SET_ORIENTATION" ,
								"SET_POINTER_SPEED" ,
								"SET_PROCESS_LIMIT" ,
								"SET_TIME" ,
								"SET_TIME_ZONE" ,
								"SET_WALLPAPER" ,
								"SET_WALLPAPER_HINTS" ,
								"SIGNAL_PERSISTENT_PROCESSES" ,
								"STATUS_BAR" ,
								"SUBSCRIBED_FEEDS_READ" ,
								"SUBSCRIBED_FEEDS_WRITE" ,
								"SYSTEM_ALERT_WINDOW" ,
								"UPDATE_DEVICE_STATS" ,
								"USE_CREDENTIALS" ,
								"USE_SIP" ,
								"VIBRATE" ,
								"WAKE_LOCK" ,
								"WRITE_APN_SETTINGS" ,
								"WRITE_CALENDAR" ,
								"WRITE_CONTACTS" ,
								"WRITE_EXTERNAL_STORAGE" ,
								"WRITE_GSERVICES" ,
								"WRITE_HISTORY_BOOKMARKS" ,
								"WRITE_SECURE_SETTINGS" ,
								"WRITE_SETTINGS" ,
								"WRITE_SMS" ,
								"WRITE_SYNC_SETTINGS"]


	def add_argument(self,name,type,help='',required=False):
		self.arg_list.append({'name':name,'help':help,'value':type,'required':required,'added':False})

	def add_argument_value(self,name,value):
		for arg in self.arg_list:
			if arg['name']==name:
				if type(value)==type(arg['value']):
					arg['value']=value
					if arg['required']:arg['added']=True
					return 1 # insert value ok
				else:
					return -1  # type mismatch
		return 0 # name mismatch

	def check_list(self):
		error_list=''
		for arg in self.arg_list:
			if arg['required'] and (not arg['added']):
				error_list+=arg['name']

	def run_project(self):
		if self.prj_path=='':
			return False,'missing Project path' # project path error
		check=self.check_list()
		if check!='':
			return False,'missing %s' % check
		filename='%s%sbuildozer.spec' % (slef.prj_path,os.sep)
		out_file = open(filename,"w")
		out_file.write('[app]\n')
		for arg in self.arg_list:
			if type(arg['value'])==type(''):
				str='%s=%s\n' % (arg['name'],arg['value'])
				out_file.write('[app]\n')
			elif type(arg['value'])==type([]):
				str='%s=%s\n' % (arg['name'],','.join(arg['value']))
				out_file.write('[app]\n')
			elif type(arg['value'])==type(True):
				str='%s=%s\n' % (arg['name'],int(arg['value']))
				out_file.write('[app]\n')
		out_file.close()
		return True,'Spec File Created' #spec file create


def get_Android_args():

	obj_builder=Android_Build_o()

	obj_builder.add_argument('title','',help='Title of your application',required=True)
	obj_builder.add_argument('package.name','',help='The name of the java package the project will be packaged under.',required=True)
	obj_builder.add_argument('version','',help='Application versionning',required=True)
	obj_builder.add_argument('source.dir','',help='Source code where the main.py live',required=True)
	obj_builder.add_argument('source.include_exts',['py','png','jpg','kv','atlas'],help='Source files to include (let empty to include all the files)')
	obj_builder.add_argument('source.exclude_exts',['spec'],help='Source files to exclude (let empty to not excluding anything)')
	obj_builder.add_argument('requirements',['kivy'],help='Application requirements')
	obj_builder.add_argument('presplash.filename','%(source.dir)s/data/presplash.png',help='Presplash of the application')
	obj_builder.add_argument('icon.filename','%(source.dir)s/data/icon.png',help='Icon of the application')
	obj_builder.add_argument('fullscreen',True,help='Indicate if the application should be fullscreen or not')
	obj_builder.add_argument('android.permissions',[],help='Permission')
	obj_builder.add_argument('android.api','14',help='Android API to use',required=True)
	obj_builder.add_argument('android.minapi','8',help='Minimum API required (8 = Android 2.2 devices',required=True)
	obj_builder.add_argument('android.sdkversion','22',help='Android SDK version to use',required=True)
	obj_builder.add_argument('android.ndkversion','8c',help='Android NDK version to use',required=True)
	obj_builder.add_argument('android.ndk_path','',help='Android NDK directory (if empty, it will be automatically downloaded.)')
	obj_builder.add_argument('android.sdk_path','',help='Android SDK directory (if empty, it will be automatically downloaded.)')
	obj_builder.add_argument('android.entrypoint','',help='Android entry point, default is ok for Kivy-based app')
	obj_builder.add_argument('android.add_jars','',help='Semicolon separated list of Java .jar files to add to the libs sothat pyjnius can access their classes. Don\'t add jars that you do not need,since extra jars can slow down the build process. Allows wildcards matching',)
	obj_builder.add_argument('android.manifest.intent_filters','',help='XML file to include as an intent filters in <activity> tag',)





	return obj_builder

