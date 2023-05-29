<div align="center">

<p align="center">
    <img src="https://github.com/Panzer-Jack/SerialHelperfor_SIX-DOF_manipulator/assets/81006731/1a68bee4-6843-4a18-b8d9-66e75861d181" alt="" width="300px">
</p>
<h4>_✨ Developped by PyQT5 and Pyserial ✨_  </h4>
一个 用于实时控制和获取六自由度机械臂-关键帧的多线程串口通信的调试软件（特化型串口工具） |  Multithreading serial debugging communications software for catch the Keyframe of 6-DOF manipulator
</div> 

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.8+-blue" alt="license">
</p>

<hr>

## 这是什么？
一个用于六自由度关节臂控制与记录的特化型串口工具（）

## 它能干什么
1. 调整数值滑条发送串口指令来实时控制关节机械臂运动
2. 在实时控制启动中可以实时记录当前帧的状态并保存进Excel表格`机械臂关键帧-录取表`
3. 可以实时接收串口返回的值并显示在左上角`接收区`
4. 通过手动修改`机械臂关键帧-确认表`（格式与录取表相同）可以测试每个录取帧的实时状态；可以单独测试，也可以整体测试。
5. 如果需要的话，你也可以把它直接当作串口工具来用（）

## 它的用法
1. 打开`qtMain.exe`
2. 输入你的串口号，点击`开关串口`
3. 实时控制功能：点击`启动`，通过滑动滑条即可
4. 实时记录关键帧功能：在`启动`后，滑动滑条到你想要的位置，然后点击`记录关键帧`；此功能是按时序连续记录的, 记录完毕后直接关闭软件. 就会自动生成`机械臂关键帧-录取表`, 过程中你可以观看左上角`接收区`来查看机械臂给你返回的串口状态。
5. 测试关键帧：首先将`机械臂关键帧-录取表`改成`机械臂关键帧-确认表`；然后进入软件。连续测试：直接点击`关键帧测试`；单独测试：在`关键帧测试`上方那个空输入表格内动作帧的的序号，然后点击`测`即可。
