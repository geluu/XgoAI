# XgoAI

## XGO AI模组升级

### 准备

- 一只XGO狗狗

- 一台pc电脑

- 一根连接电脑和狗狗的数据线

- 一个sd卡读卡器

  

### 步骤

##### pc电脑下载安装软件CocoBlockly X

​	电脑浏览器打开网址 [可可乐博（CocoRobo）官网-全球 STEAM 教育解决方案服务提供商](https://www.cocorobo.cn/download)

(https://www.cocorobo.cn/download)

​	下载“CocoBlockly X 二代模块上传插件”（橙色图标）

![DownloadCoco](readmeImages\DownloadCoco.png)



##### 连接狗狗模组，更新AI固件

​	打开软件，在电脑右下角右击软件图标，选择“AI模块固件更新”

![AIBlocklyUpdate](readmeImages\AIBlocklyUpdate.png)

​	会弹出如下窗口（如未弹出，请重启软件再尝试）

<img src="readmeImages\KflashGui.png" alt="KflashGui" style="zoom:80%;" />

​	上方框选择.kfpkg文件（cocorobo-ai-module_firmware_2021-5-20_(中文)_STABLE.kfpkg）

​	连接电脑和狗狗，下方框自动填入。完成后如下图。

![ChooseKfpkg](readmeImages\ChooseKfpkg.png)

​	开始下载并等待下载成功（保持电脑和狗狗连接稳定）

​	完成后，模组的版本日期变更为20210520



##### 修改sd卡内容

​	关闭拿出sd卡，通过sd卡读卡器在pc上读取sd卡文件，大致目录如下，将原来内容全部清除后，将新的内容填入，目录结构不变（新的内容在sd文件中）

![SdCodes](readmeImages\SdCodes.png)



##### 完成

​	sd卡内容修改完成后，启动XGO狗狗后，版本日期为20210520，选择demo后目录如下，说明升级完成

<img src="readmeimages\DemoCodes.png" alt="DemoCodes" style="zoom: 33%;" />