"""Chinese (Simplified) for the texts the launcher shows outside the base table.

`bbport_lang.KEYS` covers the labels that existed when the Windows launcher was
written; the pages added later (controls, the frame-generation and camera
options, co-op accounts, the trophy counts) build their labels from tables and
formats, so their English never reached `KEYS`. This module holds those
translations instead of growing the parallel arrays, and `bbport_lang` merges
them into the Chinese table.
"""

ZH2 = {
    # Play page and trophy counts (formatted with {} placeholders).
    '{} of {} trophies earned': '已获得 {} / {} 个奖杯',
    'All': '全部',
    'Earned': '已获得',
    'Locked': '未获得',
    'Bronze': '铜',
    'Silver': '银',
    'Gold': '金',
    'Platinum': '白金',
    'Trophies the game unlocks while you play; updated live, kept with your saves.':
        '游戏在你游玩时解锁的奖杯；实时更新，随存档保存。',

    # Graphics and display options.
    '1280 × 720 (Steam Deck)': '1280 × 720（Steam Deck）',
    '3840 × 2160 (4K)': '3840 × 2160（4K）',
    'AMD FSR 3.1 Frame Generation (any GPU)': 'AMD FSR 3.1 帧生成（任意显卡）',
    'NVIDIA DLSS Frame Generation (GeForce RTX 40/50)': 'NVIDIA DLSS 帧生成（GeForce RTX 40/50）',
    'DLSS (NVIDIA GeForce RTX)': 'DLSS（NVIDIA GeForce RTX）',
    '2× (one generated frame)': '2×（生成一帧）',
    '3× (DLSS on GeForce RTX 50)': '3×（GeForce RTX 50 上的 DLSS）',
    '4× (DLSS on GeForce RTX 50)': '4×（GeForce RTX 50 上的 DLSS）',
    'Native AA (×1.0)': '原生抗锯齿（×1.0）',
    'Quality (×1.5)': '画质（×1.5）',
    'Balanced (×1.7)': '均衡（×1.7）',
    'Performance (×2)': '性能（×2）',
    'Ultra Performance (×3)': '极致性能（×3）',
    'Frame generation': '帧生成',
    'Fit to display refresh': '跟随显示器刷新率',
    'Follow the device in use': '跟随当前使用的设备',
    'Frames made between two of the game\'s: 60 FPS on screen becomes 120. Needs a display with '
    'that refresh rate (120 Hz or more at 60 FPS); it pauses when the display cannot show the extra '
    'frames. Adds a little input latency. Menus and movies are not generated. DLSS needs a GeForce '
    'RTX 40 or newer, otherwise FSR 3.1 is used.':
        '在游戏的两帧之间插入生成的帧：屏幕上 60 帧会变成 120 帧。需要显示器达到对应刷新率'
        '（60 帧时需 120 Hz 以上）；显示器无法显示额外帧时会自动暂停。会略微增加输入延迟。'
        '菜单与过场不生成。DLSS 需 GeForce RTX 40 或更新，否则使用 FSR 3.1。',
    'FSR 3.1 makes one frame (2×); DLSS on a GeForce RTX 50 up to three (4×).':
        'FSR 3.1 生成一帧（2×）；GeForce RTX 50 上的 DLSS 最多生成三帧（4×）。',
    'On: no more frames than the display shows (an uncapped game gets fewer generated frames, and '
    'the GPU does less). Off: the multiplier as chosen.':
        '开启：不生成超过显示器能显示的帧数（不限帧时生成的帧更少，显卡负载更低）。'
        '关闭：按选定的倍数生成。',
    'Centred (16:9)': '居中（16:9）',
    'Halfway': '中间',
    'Screen edges': '屏幕边缘',
    'HUD position (ultrawide)': 'HUD 位置（超宽屏）',
    '21:9 outputs: health, items and Blood Echoes at the screen edges, or in the centred 16:9 area '
    'as on a 16:9 screen.':
        '21:9 输出：生命、道具与血之回响显示在屏幕边缘，或像 16:9 屏幕那样居中在 16:9 区域内。',
    'FIFO (VSync)': 'FIFO（垂直同步）',
    'FIFO Relaxed': 'FIFO 宽松',
    'Direct (1:1, like a PC game)': '直接（1:1，如同 PC 游戏）',
    'Field of view': '视场角',
    'Vertical, in degrees. Every camera of the game is widened by the same amount.':
        '垂直方向，单位为度。游戏内所有视角都按同一数值加宽。',
    'Mute when the game is in the background': '游戏切到后台时静音',

    # Controls.
    'Button prompts': '按键提示',
    'The game\'s button icons: your keyboard and mouse keys while you play with them, the '
    'controller\'s (PlayStation, Xbox or Switch) while you use it.':
        '游戏内的按键图标：使用键盘鼠标时显示你的按键，使用手柄时显示手柄按键'
        '（PlayStation、Xbox 或 Switch）。',
    'Layout': '布局',
    'Use the Dark Souls III layout': '使用《黑暗之魂 III》布局',
    'WASD, Space to dodge, left click / Shift + left click to attack, right click / Shift + right '
    'click (or Ctrl) for the off hand, E interact, R item, F vial, Q lock on, Tab or Esc menu, and '
    'the 1:1 mouse camera. Replaces the keyboard and mouse bindings; the controller keeps its own.':
        'WASD 移动，空格翻滚，左键 / Shift + 左键攻击，右键 / Shift + 右键（或 Ctrl）使用左手，'
        'E 交互，R 道具，F 血瓶，Q 锁定，Tab 或 Esc 菜单，以及 1:1 鼠标视角。'
        '会替换键盘鼠标绑定；手柄保持自己的绑定。',
    'Click a slot, then press a key, click a mouse button or turn the wheel; Esc cancels. '
    'Right-click a slot to clear it. Movement and camera directions take keys only.':
        '点选一个槽位，然后按键、点鼠标键或滚动滚轮；Esc 取消。右键点击槽位清除绑定。'
        '移动与视角方向只能绑定键盘。',
    'Combinations: hold Shift, Ctrl or Alt while pressing the key or mouse button (up to three '
    'inputs, such as Shift + left click). A held combination wins over the bindings on its parts, '
    'so left click and Shift + left click can be two actions. ⚠ marks an input another action uses '
    'too. A key that is both an action of its own and part of a combination is pressed on the way '
    'into it: with Shift on Circle, Shift + left click starts a sprint that ends as a dodge.':
        '组合键：按住 Shift、Ctrl 或 Alt 再按该键或鼠标键（最多三个输入，例如 Shift + 左键）。'
        '按住的组合优先于各分键自身的绑定，因此左键与 Shift + 左键可以是两个不同动作。'
        '⚠ 表示该输入也被其他动作使用。某个键既是独立动作又属于组合时，会按进入组合的方式触发：'
        '若 Shift 绑在圈上，则 Shift + 左键会先起跑、随后转为翻滚。',
    'Combinations are cancelled by any other key': '按其他任何键都会取消组合',
    'Mouse controls': '鼠标控制',
    'Mouse buttons and the scroll wheel are bound in the slots above: click a slot, then click or '
    'turn the wheel. They work while the mouse is captured (mouse look on).':
        '鼠标键与滚轮绑定在上面的槽位：先点槽位，再点击或滚动滚轮。'
        '它们在鼠标被捕获时（鼠标视角开启）生效。',
    'Enable mouse look': '启用鼠标视角',
    'Mouse look': '鼠标视角',
    'Sensitivity (stick)': '灵敏度（摇杆）',
    'Sensitivity (direct)': '灵敏度（直接）',
    'How fast the camera turns for a given mouse movement in stick emulation.':
        '摇杆模拟下，鼠标移动量对应的视角转速。',
    'How far the direct camera turns per mouse movement (1.00 = 900 counts per radian).':
        '直接模式下鼠标每移动一格转动多少（1.00 = 每弧度 900 计数）。',
    'A constant added on top of sensitivity; raises the floor for slow movements without affecting '
    'fast ones as much.':
        '在灵敏度之上叠加的常量；抬高慢速移动的下限，对快速移动影响较小。',
    'Vertical sensitivity': '垂直灵敏度',
    'Up and down as a multiple of left and right (1.00 = the same).':
        '上下灵敏度为左右的倍数（1.00 = 相同）。',
    'Invert horizontal': '反转水平',
    'Invert vertical': '反转垂直',
    'Vertical sensitivity and inverting apply to both camera modes.':
        '垂直灵敏度与反转对两种视角模式都生效。',
    'Minimum turn speed (stick)': '最低转速（摇杆）',
    'Stick emulation': '摇杆模拟',
    'Direct turns the game\'s camera by exact angles: no stick acceleration or turn-speed cap. It '
    'falls back to the stick while locked on.':
        '直接模式按精确角度转动视角：没有摇杆加速，也没有转速上限。锁定目标时回退为摇杆。',
    'Multiplier': '倍数',
    'Changes apply the next time the game starts, or press F8 in-game to reload input.ini without '
    'restarting.':
        '改动会在下次启动游戏时生效；也可在游戏内按 F8 重新载入 input.ini，无需重启。',
    'F7 also toggles this in-game, instantly; F8 reloads these settings without restarting.':
        '游戏内按 F7 也可即时切换；F8 重载这些设置，无需重启。',
    'Reserved: Insert/Escape (the port\'s menu), F9 (route recording), and whichever key toggles '
    'mouse look or reloads input.ini (F7/F8 by default).':
        '已占用：Insert/Escape（移植版菜单）、F9（路线录制），以及切换鼠标视角或重载 input.ini 的键'
        '（默认 F7/F8）。',
    'Keyboard and mouse': '键盘与鼠标',
    'Keyboard and mouse bindings, up to three per action. The controller keeps working side by '
    'side; edit its lines in input.ini directly — see docs/INPUT.md.':
        '键盘与鼠标绑定，每个动作最多三个。手柄可同时使用；手柄的绑定请直接编辑 input.ini'
        '——见 docs/INPUT.md。',
    'Movement and camera': '移动与视角',
    'Movement (left stick)': '移动（左摇杆）',
    'Move forward': '前进',
    'Move back': '后退',
    'Move left': '左移',
    'Move right': '右移',
    'Camera': '视角',
    'Camera (right stick)': '视角（右摇杆）',
    'Camera up': '视角上',
    'Camera down': '视角下',
    'Camera left': '视角左',
    'Camera right': '视角右',
    'Combat': '战斗',
    'Attack (R1)': '攻击（R1）',
    'Strong attack (R2)': '重攻击（R2）',
    'Transform weapon (L1)': '变形武器（L1）',
    'Firearm (L2)': '枪械（L2）',
    'Items and menus': '道具与菜单',
    'Use quick item (Square)': '使用快捷道具（□）',
    'Blood vial (Triangle)': '血瓶（△）',
    'Interact; confirm in menus (Cross)': '交互；菜单中确认（×）',
    'Dodge / dash (hold); back in menus (Circle)': '翻滚 / 冲刺（长按）；菜单中返回（○）',
    'Jump while dashing (L3)': '冲刺中跳跃（L3）',
    'Lock on / reset camera (R3)': '锁定 / 视角归位（R3）',
    'Game menu (Options)': '游戏菜单（Options）',
    'Gestures (touchpad)': '手势（触摸板）',
    'Right half of the touchpad (debug menu)': '触摸板右半（调试菜单）',
    'Switch right hand weapon (d-pad right)': '切换右手武器（十字键右）',
    'Switch left hand weapon (d-pad left)': '切换左手武器（十字键左）',
    'Switch quick item (d-pad down)': '切换快捷道具（十字键下）',
    'D-pad up': '十字键上',
    'Game (43°)': '游戏（43°）',
    'Precise': '精确',
    'Quit to Desktop in the title menu and in the System menu': '在标题菜单与系统菜单中加入「退到桌面」',

    # Online co-op.
    'Co-op pool': '联机池',
    'shadNet server': 'shadNet 服务器',
    'shadNet: a shadNet server and its account. SuperMedo Server uses an account from supermedo.com.':
        'shadNet：shadNet 服务器及其账号。SuperMedo Server 使用 supermedo.com 的账号。',
    'SuperMedo Server': 'SuperMedo Server',
    'SuperMedo Server account': 'SuperMedo Server 账号',
    'The account you made at supermedo.com.': '你在 supermedo.com 注册的账号。',
    'Sign up for SuperMedo Server': '注册 SuperMedo Server',
    "The Hunter's Dream (with bbhost players)": "The Hunter's Dream（与 bbhost 玩家联机）",
    "The Hunter's Dream account": "The Hunter's Dream 账号",
    "The connection to The Hunter's Dream is Awaken's port of bbhost's network code; bbhost and "
    "The Hunter's Dream are by droogie.":
        "The Hunter's Dream 连接是 Awaken 对 bbhost 网络代码的移植；"
        "bbhost 与 The Hunter's Dream 由 droogie 开发。",
    'Sign in with Discord': '使用 Discord 登录',
    'Not signed in': '未登录',
    'Username': '用户名',
    'Show me on the live map': '在实时地图上显示我',
    'thehuntersdream.com/map shows where players are and which bells ring: the game sends your '
    'position more often while you play.':
        'thehuntersdream.com/map 显示玩家位置与摇铃情况：游戏会在你游玩时更频繁地上传位置。',

    # Patches page.
    'Download community patches': '下载社区补丁',
    '{} community patches, updated {}': '社区补丁 {} 条，更新于 {}',
    'This fork:': '本分支：',

    # Keys and mouse buttons, and the few remaining labels.
    'Left click': '鼠标左键',
    'Right click': '鼠标右键',
    'Mouse back': '鼠标侧键（后）',
    'Mouse forward': '鼠标侧键（前）',
    'Walk (hold)': '行走（长按）',
    'Other versions…': '其他版本…',
    'Play with': '游玩方式',
}
