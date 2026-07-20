圆玩 ~ Oceanfront
=

---

**点线Project 第二作**  

**在 26 年的三分之一时开始做的**  

**本作并不是打砖块，可能偏向于文花帖这类作品** *（？*  

**设定是有 4 面**  

---

## 前情提要
**“罗，玩的开心！记得带点海胆回来哦~”**  

**“放心吧，按璃你的厨艺三两下就能做好吃了，但是今天晚上我在圆湾吃哦。”**  

**“嗯……车快到了，拜拜~”**  

**“拜拜！”**  

---

## 按键说明书
- ### 主界面
  - 按 Z 开玩
  - 按 C 查看日志 *（有日志看日志，没日志当木鱼*
  - 按 Q 回家
- ### 游戏ing
  - 按 ↑↓←→ 移动
  - 在对话中按 Z 下一则对话
    - 也可以按 X 跳过
  - 按 Esc 休息一下
  - 主主角操控看[主主角](#主主角)吧
- ### 休息ing
  - 按 Esc 休息完了
  - 不想玩就按 Del 吧 *（返回主界面了*
- ### 存日志
  - 按 Esc 不存
  - 按 Enter 存 *（存在 用户根目录/Saved Games/DX01 里*
  - 可以存致谢人的名称 *（最多 8 个字符*
- ### 看日志
  - 按 Esc 合上
  - 按 Del 扔掉
  - 翻页则按 ←→

---

## 主主角
- ### H.罗
  - 形力
    - 最高 48 点，最低 -8 点
    - 每收集 24 点蓄力点加 1 点形力
    - 每撞一次弹幕减 4 点形力
  - 形态
    - 长按 Z 切换为特殊形态
      - 一旦松开会切换回正常形态
    - 正常形态为大胆状态 *（普速移动*
    - 特殊形态为谨慎状态 *（慢速移动*
  - 累值
    - 最高 24 点
    - 达到最高点按 SPACE 把所有在窗口内的弹幕转为蓄力点并吸过来 *（这也算是一种形分吧？*

---

## 说一下规则吧
- ### 形点
  - 绿色为蓄力点
- ### 分数
  - 每收集一个蓄力点 + 64
  - 结算
    - 形闪结算：(24 - 形闪次数) / 24 * 32768
    - 形力结算：形力 / 最大形力 * 8192
- ### 输赢
  - 如果剩余分数为 0 或者负数，则算赢
  - 否则算输
- ### 擦弹
  - 每擦一次弹加 1 点累值
  - 在无敌时间不会加累值
- ### 无敌
  - 被弹幕撞到后有 3.5 秒的无敌时间
  - 释放累值后则有 2 秒

---

## 分发包清单
- ### CHAR.md
  - 这是角色们的介绍文档
  - 分有主主角和主角 *（主角就是每面末站的 BOSS，按面数从上到下排*
- ### DX00125.pyz
  - 游戏的主程序
  - 双击就可以开玩啦 *（要有 [Python 和 Pygame-CE 环境](#本项目使用以下第三方资源)*
- ### LICENSE
  - 顾名思义就是许可证
  - 本游戏的程序代码就是以这个协议开源的 *（源神*
- ### README.md
  - 就是你正在阅读的

---

## 备注区
- ### 本项目版权声明
  - 程序代码遵循 [GNU GPLv3.0](./LICENSE) 协议
  - 所有资产文件均保留所有权利 *（字体文件除外*
- ### 本项目使用以下第三方资源
  - 编程语言：[Python](https://www.python.org) *（需要安装哦*
    - 推荐 3.11 - 3.15
  - 游戏库：[Pygame-CE](https://github.com/pygame-community/pygame-ce) *（这个也是*
    - 可以在命令提示符输入 pip install pygame-ce 回车
  - 字体：[GNU Unifont](https://www.unifoundry.com/unifont) *（子集化后的，我称它为 Uni3500*
    - 子集化用到的
      - 工具：[字体子集化](http://font.ssjjss.com/font-subset)、[Fonttools](https://github.com/fonttools/fonttools)
      - 仓库：[常用汉字集](https://gitee.com/feng_xingkai/chinese)
    - 遵循 [SIL OFL 1.1](https://www.unifoundry.com/OFL-1.1.txt) 协议
  - 音频
    - 制作：[PMD](http://www5.airnet.ne.jp/kajapon/tool.html) *（喜欢 YM2203*
    - 处理：[WaveShop](https://github.com/victimofleisure/WaveShop)
  - 图像：[Krita](https://krita.org/zh-cn)
  - 打包：[Zipapp](https://docs.python.org/3/library/zipapp.html)
- ### 本项目网址 *（感兴趣的话就点个星吧~*
  - https://github.com/An-172N/DianXian-YuanWan

---

**(C)opyright 2026 An_172N**  