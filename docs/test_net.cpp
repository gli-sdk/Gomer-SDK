#ifndef WIN32
#include <unistd.h>
#include <cstdlib>
#include <cstring>
#else
#include <winsock2.h>
#include <ws2tcpip.h>
#include <wspiapi.h>
#include <windows.h>
#endif

#include <iostream>
#include "glproto.h"

using namespace glproto;

int printf_receive_message(char* buf, int len){
	//LogDbg("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  %s\n",buf);
	return 0;
}

int GetFileResult(int result)
{
	LogDbg("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  file unblock transmit result is %d\n",result);
	return 0;
}
int main()
{
	std::cout << " @@@@@ Hello Gproto! @@@@@" << std::endl;
	int number =0;
	char * device[10];
	int xxx =ProtocolSearchDevice(number,device);
	if(xxx <1){
		LogDbg("*****************  No device find  *****************");
		return 0;
	}

	//if name == nullptr,then name set auto to be the first device
	char* name = device[0];
	//char* name;
	int yyy = ProtocolConnectDevice(name,printf_receive_message);
	if(yyy<0) {
		LogDbg("*****************  connect fail  *****************");
		return 0;
	}
    char wxy[1024] = {0};
    strcpy(wxy, "{\"seq\" : 14, \"msgtype\" : 1, \"control\" : {\"mode\" : 102}}");
    ProtocolSendMessage(wxy);

	char* test_message = const_cast<char*> ("{\"seq\" : 15, \"msgtype\" : 1,\"control\" : {\"video\" : 101}}");
	char* filePath = const_cast<char*> ("C:\\Users\\Administrator\\Desktop\\song1\\aizhongguo.wav");
	int fileType = mEnumSaveVoiceFile;
	char x;
	LogWarn("please input a letter to continue \n");
	LogWarn("e:exit      b:file transmite block        f:file transmite unblock      v:open video and display \n");
	std::cin>>x;
	while(x !='e'){
		switch (x){
			case 'b':
				ProtocolSendFileBlock(fileType,filePath);
				break;
			case 'f':
				ProtocolSendFileUnblock(fileType,filePath,GetFileResult);
				break;
			case 'v':
				ProtocolOpenVideoAndDisplay();
				break;
		}
		LogWarn("please input a letter to continue \n");
		LogWarn("e:exit      b:file transmite block        f:file transmite unblock     v:open video and display \n");
		std::cin>>x;
	}
    ProtocolDestroyConnect();
	return 0;
}
