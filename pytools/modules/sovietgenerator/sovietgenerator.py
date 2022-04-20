'''
Function:
    苏联笑话生成器
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import random
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui


'''苏联笑话生成器'''
class SovietGenerator(QWidget):
    tool_name = '苏联笑话生成器'
    def __init__(self, parent=None, title='苏联笑话生成器 —— Charles的皮卡丘', **kwargs):
        super(SovietGenerator, self).__init__(parent)
        rootdir = os.path.split(os.path.abspath(__file__))[0]
        self.setFixedSize(800, 500)
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(os.path.join(rootdir, 'resources/icon.jpg')))
        # 定义一些必要的组件
        grid = QGridLayout()
        # --标签
        label_1 = QLabel('要讽刺的事情:')
        label_2 = QLabel('事情的提出人:')
        label_3 = QLabel('提出者声称这件事有助于:')
        label_4 = QLabel('事件的受害者:')
        label_5 = QLabel('事件发生的组织:')
        # --输入框
        self.edit_1 = QLineEdit()
        self.edit_1.setText('连花清瘟配送优先级高于生活必需品')
        self.edit_2 = QLineEdit()
        self.edit_2.setText('内容违规无法显示')
        self.edit_3 = QLineEdit()
        self.edit_3.setText('代替其他生活必需品')
        self.edit_4 = QLineEdit()
        self.edit_4.setText('你猜是哪个倒霉鬼')
        self.edit_5 = QLineEdit()
        self.edit_5.setText('以岭药业')
        # --生成按钮
        button = QPushButton('生成苏联笑话')
        # --结果显示框
        self.text_edit = QTextEdit()
        # 组件布局
        grid.addWidget(label_1, 0, 0, 1, 1)
        grid.addWidget(self.edit_1, 0, 1, 1, 1)
        grid.addWidget(label_2, 1, 0, 1, 1)
        grid.addWidget(self.edit_2, 1, 1, 1, 1)
        grid.addWidget(label_3, 2, 0, 1, 1)
        grid.addWidget(self.edit_3, 2, 1, 1, 1)
        grid.addWidget(label_4, 3, 0, 1, 1)
        grid.addWidget(self.edit_4, 3, 1, 1, 1)
        grid.addWidget(label_5, 4, 0, 1, 1)
        grid.addWidget(self.edit_5, 4, 1, 1, 1)
        grid.addWidget(button, 5, 0, 1, 2)
        grid.addWidget(self.text_edit, 6, 0, 5, 2)
        self.setLayout(grid)
        # 事件绑定
        button.clicked.connect(self.generate)
    '''生成苏联笑话'''
    def generate(self):
        templates = [
            "“数学和{event}有什么区别？”\r\n“在数学上，如果给出什么东西，都需要证明，而{event}什么能证明，就是什么也不能提供。”\r\n",
            "“能光屁股坐在刺猬身上吗？”\r\n“可以，但只是在三种情况下：刺猬的刺被剃掉，是别人的屁股，或者是{boss}命令那样做。”\r\n",
            "请问，这就是{target}，还是会更差劲。\r\n",
            "{boss}对大家说：“我们的一只脚已经踏上{event}，另一只脚则迈向{target}”。一个{victim}说：要是时间太长，人就会变成拐子。\r\n",
            "“{org}的童话和经典童话有什么不同？”\r\n“经典童话的开头通常是：‘很久很久以前……’而我们的则是：‘不远了，不远了……’\r\n",
            "“什么在{org}是最常见的？”\r\n“暂时的困难。”\r\n",
            "“{event}的优越性体现在哪里？”\r\n“成功地克服了在{org}之外不会存在的困难。”\r\n",
            "在{org}的调查表上有这样一个问题：在执行{event}时你动摇过吗？\r\n{victim}的回答是：“我和{event}一起动摇。”\r\n",
            "在{org}。\r\n“{victim}您好。”\r\n“您好。”\r\n“请问您是{boss}吗？”\r\n“不是。”\r\n“您以前是{boss}吗？”\r\n“不是。”\r\n“您的直系亲属中有{boss}吗？”\r\n“没有。”\r\n“那么请您把脚挪开，你踩着我了。”\r\n",
            "“为什么{org}不能接受圣经？”\r\n“根据圣经，先有混乱，然后根据上帝的计划引入秩序。{event}的经验告诉我们，先有秩序，然后混乱就会到来。”\r\n",
            "在{org}庆典的聚会上，一位35岁的{victim}高举着牌子，上面写着“感谢{event}赐予我的快乐的童年”。\r\n{boss}呵斥道，“你是在嘲讽{event}吗？{event}才实行了20年。”\r\n“确切地说，这正是我感谢它的原因。”\r\n",
            "{boss}发言道：“从下个礼拜开始我们要做两件事，一，全面在{org}实行{event}；二，周六所有{victim}都要去酒吧里拿一条蜥蜴。大家有什么意见可以提出来。”\r\n过了一会儿，台下有个声音怯生生地提问：“为什么要拿蜥蜴？”\r\n“很好，我就知道大家对{event}没有异议。”\r\n",
            "“{event}真**的智障！”\r\n“你涉嫌恶意攻击{boss},跟我走一趟。”\r\n“我又没说是哪里的{event}！”\r\n“废话！哪里的{event}智障我会不知道吗！”\r\n",
            "{boss}在向{victim}们讲话：\r\n“很快我们就能{target}！”\r\n台下传来一个声音：“那我们怎么办？”\r\n",
            "一个{victim}的鹦鹉丢了。这是只会说话的鹦鹉，要是落到{boss}的手里可糟了。\r\n这人便发表了一篇声明：“本人遗失鹦鹉一只，另外，本人不同意它关于{event}的观点。”\r\n",
            "“{event}是艺术还是科学?”\r\n“我说不好，但肯定不是科学。”\r\n“何以见得?”\r\n“如果{event}是科学的话，他们至少应该先用小白鼠做实验。”\r\n",
            "大会主持人:”请支持{event}的人坐在左边，反对{event}的坐在右边。”\r\n大多数人坐在了右边，少数人坐在了左边，只有一个人坐在中间纹丝不动。\r\n主持人很不解，询问情况。\r\n“我对{victim}们的情况表示十分理解，但我支持{event}。”\r\n”那您赶快坐到主席台来。”主持人急忙说道。\r\n",
            "{boss}关于“关爱{victim} 支持{event}”的会议纪要正在以超光速增长，但这并没有违背相对论，因为会议纪要里不含有任何信息。\r\n",
            "{boss}:“我们要不惜一切代价，为了我们的主人翁{target}！”\r\n一个{victim}对另一个{victim}说:“看哪 ，{boss}把咱们当主人翁。”\r\n另一个{victim}说:“不，我们是‘代价’。”\r\n",
            "“如果你在{org}，旁边一个陌生人突然开始唉声叹气，正确的做法是什么?”\r\n“立即阻止这种反对{event}的行为。”\r\n",
            "{boss}:“由于{event}的实行，各位{victim}的美好未来前景已经出现在了地平线上。”\r\n一个{victim}问另一个{victim}:”什么是地平线?”\r\n另一个{victim}回答道:“就是那个能看到但是永远都到不了的线。”\r\n",
            "{boss}在{org}随机采访了一位{victim}:“请问你对{event}有什么意见吗?”\r\n{victim}答道:“我有一些意见，但我不同意我的意见!”\r\n",
            "两个骷髅相遇，一骷髅问另一个骷髅:“我是被{boss}的{event}逼死的，你是怎么死的？”\r\n另一个骷髅回答说:“我还活着。”\r\n",
            "{boss}的汽车被一头牛挡住了，怎么也赶不走。{boss}便下车对牛说：“你再不走，我就把你送到{org}去{event}。”牛听了便一溜烟的跑开了。\r\n",
            "问：“{event}在哪些时候会遇到抵制？”\r\n答：“主要有四个时间段：春天、夏天、秋天和冬天。”\r\n",
            "{boss}问一名{victim}:“你的爸爸是谁？”\r\n他回答说：“是{boss}!”\r\n{boss}很满意，又问：“你的母亲是谁？”\r\n他回答：“是{event}！”\r\n{boss}又问：“你将来想当什么？”\r\n“孤儿！”\r\n",
            "问：“什么是最短的笑话？”\r\n答：“{event}。”\r\n",
            "问：“那些别有用心的人是怎样黑{event}的？”\r\n答：“他们把{boss}说的内容原文复述了。”\r\n",
            "问：“为什么{boss}把{victim}放在中心考虑？”\r\n答：“这样从各个方向都能方便地欺压他们。”\r\n",
            "问：“什么叫交换意见？”\r\n答：“带着你的意见去找{boss}理论，然后带着他的回来。”\r\n",
            "问：“{event}实行的结果如何？”\r\n答：“还是有人活下来了。”\r\n",
            "问：“{event}的前景是什么？”\r\n答：“有两种可能的情况。现实的可能是火星人会降临地球帮我们打理一切，科幻的可能是我们成功地{target}。”\r\n"
        ]
        template = random.choice(templates)
        template = template.replace('{event}', self.edit_1.text()).replace('{boss}', self.edit_2.text()).replace('{target}', self.edit_3.text()).replace('{victim}', self.edit_4.text()).replace('{org}', self.edit_5.text())
        self.text_edit.setText(template)