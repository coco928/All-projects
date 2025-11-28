>##### TEAMNAME: 对对队
>##### LEADER: 朱家怡（2023533180）
>##### MEMBERS：黄乙珂（2023533020）彭琨景（2023533186）

# **游戏操作说明**
- 切换英语输入法
- 用箭头按键来移动主角（PGUP，PGDN，HOME，END）而不是awsd按键
- 由于pygame库函数的感应问题，有时候判定按下按键会很不灵敏，可以尝试长按某个按键或迅速按
- 每天首先要做的就是去找npc对话得知要干什么以及当天操作限制

# **BunnyKillsMommy/杀马兔**
- 我是一款兼养成与解谜于一体的像素游戏，玩家通过控制主角`Bunny`探索小镇`The Great Great Town`发生的故事。
- 近日，小镇被未知的**邪恶势力**攻击，水源污染严重，不少村民因此而亡。善良的`Bunny`向村民们伸出援手，在有限的**三天时间**内找到水源污染的真相。
  - 第一天：
    - 去*井下* 杀死**幽灵**以获得金币，收集幽灵掉落的可以引出boss的**碎片（Debris）**
    - 去*商店* 用**金币**购买**种子**并在*菜地* 种下
    - 回到*家* 中接**食物**来回复**血量**
  - 第二天：
    - 去*菜地* 收获**果实**并在*商店* 合成**神秘药水（Potion）**
    - 继续去*井下* 杀死**邪恶势力**以获得金币，收集**碎片（Debris）**用来引出Boss
    - 回到*商店* 用金币来增强**人物属性**，包括Hp、攻击力和防御等等，为攻打boss做准备
    - 回到*家* 中接**食物**来回复**血量**
  - 第三天： 
    - 杀死**BOSS**获得最终结局
  - **注意**：进入*家* 意味着一天的结束，在你完成今天的任务之前，请**不要**随意的出入*家* 中，否则会收获意想不到的结局。

- **成员分工**
  - **朱家怡**：
    - 1.DialogBox
    - 2.ShoppingBox
    - 3.种花流程（如`Field.py`、`check_event_planting()`等）
    - 4.四种结局（在`Main.py`和`Scene.py`中体现，既有动画也有picture的结算页面）
    - 5.场景转换（Main里面的事件判断种包含flush_scene的部分）
    - 6.素材收集（所有的图片资料）， 动画每一帧的制作（动画用到的图片）， 剧情编写
    - 7.编写Report
    - 8.作为团队与github的桥梁
  - **黄乙珂**：
    - 1.接金币相关的（Coinbox，HomeScene，README）
    - 2.动画相关：home里的开门动画，战斗特效（Battlebox中的打斗动画的部分以及chek_event_battle中的判断怪兽种类的部分），boss和monster的动画（Boss和Monster类中的update函数），player的移动和动画
    - 3.Camera（WildScene里面的）
    - 4.WildScene（一开始是pkj全写了，然后因为她加了太多的函数，并没有用render函数，很不工整，于是我帮她又几乎全部重写了（包括WildScene里面render函数的内容，SceneManager里面的update和render函数的部分内容，Map里面gen_monster,gen_wild_map的内容））
    - 5.ShoppingBox（和朱家怡一起写的）
    - 6.统一碰撞检测（SceneManager里面的collide的update函数）
    - 7.优化DialogBox的触发（check_event_talking中除了每天文字不同的部分的其他部分），顺便优化npc（村长）的移动（一旦进入player周围的一定范围就会停下）
    - 8.剧情编写
    - 9.天数循环（和day相关的地方）
    - 10.参与结算动画制作
    - 11.编写Report中的“统一碰撞”、“camera"、“两种monster”、“接金币”、“打斗”
  - **彭琨景**：
    - 1.野外场景的构建和怪物的生成（旧版的一些相关函数，现在无法看到但是第一次check的时候上传到过github，可以正常运行但是格式不太工整）
    - 2.野外迷宫的构建，添加相应的碰撞检测
    - 3.战斗机制代码的书写（BattleBox和SceneManager中的check_event_battle函数等）
    - 4.添加游戏Bgm
    - 5.书写readme和report
    - 6.优化DialogBox（check_event_talking中每天文字不同的部分，并重写了整个对话）
    - 7.游戏可玩性优化，即合理设计参数
