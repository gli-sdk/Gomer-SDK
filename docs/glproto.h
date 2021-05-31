#ifndef _GLPROTO_H_
#define _GLPROTO_H_

#include "os_type.h"
#include <thread>

#ifdef WIN32
//#include<winsock2.h>
    #ifndef __MINGW__
		#include <winsock2.h>
        typedef SOCKET OS_SOCKET;
    #else
        typedef int OS_SOCKET;
    #endif
#else
    typedef int OS_SOCKET;
#endif

namespace glproto
{
// function: ProtocolSearchDevice
// description: when we want to connect to device,first of all, we should search device by this function
// parameter: respond_device_number: output,the number of devices who respond; name_List: output,the name of devices
// return:  //<0: error  //-9:no device respond   //1: some devices respond
OS_API int ProtocolSearchDevice(int& respond_device_number,char* name_List[]);

// function: ProtocolConnectDevice
// description: if some device has been found,it can be connected by this function,only one device can be connect at the same time
// parameter: name: input,the name of device we want to connect,default(name=null) will connect the first one;
//            msg_callback: input,when received some message,the function call back
// return:  //<0: error   //1: connect success
typedef int (*FuncMsgCB)(char* buf, int len);
OS_API int ProtocolConnectDevice(char* name,FuncMsgCB msg_callback);

// function: ProtocolDestroyConnect
// description: close connection by this function
// parameter:
// return:  //0: success
OS_API int ProtocolDestroyConnect(void);

// function: ProtocolSendMessage
// description: send message to device by this function
// parameter: buf: input,the data of the message,the length of the message should less than 1440 bytes
// return:  //<0:fail      //0: success
OS_API int ProtocolSendMessage(char* buf);

// function: ProtocolSendFileBlock
// description: send file to device by this function,when sent over or some error occurred,it return
// parameter: file_type:input,file type (EmFileTypeItem);  file_path: input,the path of the file
// return:  the result of file transmit(EmTransmitFileResult)
enum EmFileTypeItem {
	mEnumSaveVoiceFile = 101,
	mEnumSaveImageFile = 102,
	mEnumNotSaveVoiceButPlayImmediately = 201,
	mEnumNotSavePicture = 202,
	mEnumNotSaveVoiceAndNotPlay = 204,
};
enum EmTransmitFileResult {
	kInputFileTypeWrong = -1,
	kInputFilePathWrong = -2,
	kInputFileNull = -3,
	kFileTransmitStatusBusy = -4,
	kFileTransmitError = -5,
	kFileTransmitOk =1,
};
OS_API int ProtocolSendFileBlock(int file_type, char* file_path);

// function: ProtocolSendFileUnblock
// description: send file to device by this function,it return immediately
// parameter: file_type:input,file type (EmFileTypeItem);  file_path: input,the path of the file;
//            cb: output,when sent over or some error occurred,it call back function cb with result (EmTransmitFileResult)
// return:  0
typedef int (*FuncFileCB)(int result);
OS_API int ProtocolSendFileUnblock(int file_type,char* file_path ,FuncFileCB cb);


// function: ProtocolOpenVideo
// description: open robot video by this function,it return immediately
// parameter: play_video:output,call back function,return yuv data, width of image ,height of image;
// return:  //<0:fail      //0: success
OS_API int ProtocolOpenVideo(int (*play_video)(unsigned char *yuv_data, int width, int height));

// function: ProtocolCloseVideo
// description: close robot video by this function,it return immediately
// parameter: 
// return:  //<0:fail      //0: success
OS_API int ProtocolCloseVideo(void);

// function: ProtocolOpenVideoAndDisplay
// description: open robot video and display it in screen,it return immediately
// parameter: 
// return:  //<0:fail      //0: success
OS_API int ProtocolOpenVideoAndDisplay(void);

// function: ProtocolCloseVideoAndDisplay
// description: close robot video by this function,it return immediately
// parameter: 
// return:  //<0:fail      //0: success
OS_API int ProtocolCloseVideoAndDisplay(void);
// function: DelayMs
// description: time delay with the unit of milisecond
// parameter: ms: input,milisecond
// return:
OS_API void DelayMs(int ms);

// function: MiscCreateThread
// description: start a new thread
// parameter: func: input,the function of new thread;  param: the parameter of the function of new thread
// return:  id of this thread
typedef void(*ThreadFunc)(void*);
OS_API int MiscCreateThread(ThreadFunc func, void * param);


//  ---------------------------------- Deprecated  bellow  this line, No longer maintained ------------------------------------------  //
//  ---------------------------------- Deprecated  bellow  this line, No longer maintained ------------------------------------------  //
//  ---------------------------------- Deprecated  bellow  this line, No longer maintained ------------------------------------------  //


enum EmTransmitFileStat {
	kTrFileStatIdle = 0,
	kTrFileStatBusy,
	kTrFileStatOK,
	kTrFileStatErr
};
OS_API OS_SOCKET ProtUdpCreate(void);
OS_API int ProtUdpDestroy(OS_SOCKET socket_id);
OS_API int ProtUdpSend(OS_SOCKET socket_id, char* buf, int buf_size);
//try to receive data, this is a blocking call
OS_API int ProtUdpRecv(OS_SOCKET socket_id, char* buf, int buf_size);
//create a thread to receive data, please give a callback function
OS_API int ProtCreateUdpRecvMonitor(OS_SOCKET socket_id, FuncMsgCB msg_callback);

OS_API int ProtSearchDevice(OS_SOCKET socket_id);
OS_API int ProtSelectDevice(char *dev_name, int sid);

OS_API int ProtClearConnectStat(void);
//OS_API int ProtClearDeviceList(void);

//message
OS_API OS_SOCKET ProtMsgSocketCreate(void);
OS_API int ProtMsgSocketDestroy(OS_SOCKET socket_id);
OS_API int ProtMsgSend(OS_SOCKET socket_id, char* buf, int buf_size);
//try to receive data, this is a blocking call
OS_API int ProtMsgRecv(OS_SOCKET socket_id, char* buf, int buf_size);
//create a thread to receive data, please give a callback function
OS_API int ProtCreateMsgRecvMonitor(OS_SOCKET socket_id, FuncMsgCB msg_callback);

//file transmit
OS_API int ProtFileSend(char* file);
//create a thread to send file, please give a callback function
OS_API int ProtFileAsyncSend(char* file, FuncFileCB cb);



}//namespace glproto


#endif	//_GLPROTO_H_
