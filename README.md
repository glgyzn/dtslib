# dtslib 分布式光纤拉曼测温DTS解调库

```c
char* getUUID();  
描述：获取设备的ID，获取该ID后请登录www.dxslib.com获取试用的License。

char* authorize(char* licensePath, char* publicKeyPath);  
描述：授权操作，授权操作成功后才能进行解调操作。
参数：licensePath为license的路径，publicKeyPath为publicKey的路径。 
返回值：  
成功：{"ret":"ok",  data:""}  
失败：{"ret":"err",  msg: "error msg"}  

void update(double* ListA, double* ListB, int lengthA, int lengthB);  
描述：更新需要解调的数据  
参数：ListA为反斯托克数组，ListB为斯托克数组，LengthA为ListA数组元素的个数，LengthB为ListB数组元素的个数。  

void demodulate(int start, int end);  
描述：解调操作，由于DTS 接头反射导致前端跟后端一些点位的数据我们无法使用，所以我们需要设置合理的解调范围，以便把盲区排除在外。  
参数：start 为解调开始位置，默认为0，end为解调结束位置；当end为-1时这对所有点进行解调，但是这往往会导致解调出错，
所以实际应用过程中可以先设置为-1获取原始比值曲线，然后观察曲线，再设置合理的解调范围。

char* getDecayCurve();  
描述：获取原始比值曲线，返回json格式的字符串数据。  
返回值：  
成功：{"ret":"ok",  data:"xxx,xxx,xxx,xxx...."}，其中xxx为每个点的原始比值  
失败：{"ret":"err",  msg: "error msg"}  

char* getCompensationCurve();  
描述：获取补偿后的比值曲线  
返回值：  
成功：{"ret":"ok",  data:"xxx,xxx,xxx,xxx...."}，其中xxx为每个点的补偿后比值  
失败：{"ret":"err",  msg: "error msg"}    

char* getTemperature(char* calibrationData);  
描述：获取温度曲线  
参数：calibrationData 为标定数据的字符串指针，格式：”补偿后曲线点位的数值:实际标定的温度值”，
多个标定值用逗号分隔；例如: “0.54:25,0.7:100”。
返回值：  
成功：{"ret":"ok",  data:"xxx,xxx,xxx,xxx...."}，其中xxx为每个点的温度  
失败：{"ret":"err",  msg: "error msg"}   
