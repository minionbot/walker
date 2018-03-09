# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

import itertools

KEYS = [
    '原地',
    '原地封',
    't3', '户县',
    't4', '大庆',
    't5', '大寨',
    't11', '韶山',
    't74', '辽塑',
    't82', '西厢',
    't84', '黄帝陵',
    't89', '簪花仕女图',
    't89m',
    't96', '拙政园',
    't99', '牡丹亭',
    't99m',
    't100', '峨眉山',
    't103', '梅花', '梅园',
    't103m',
    't104', '花灯',
    't108', '航天',
    't110', '白鹤',
    't110m',
    't116', '壁画', '敦煌',
    't121', '名楼',
    't129', '兰花',
    't130', '泰山',
    't131', '三国',
    't132', '麋鹿',
    't137', '儿童生活',
    't138', '水浒',
    't140', '华山',
    't141', '美术作品',
    't143', '火箭',
    't144', '西湖',
    't150',
    't151', '铜马车',
    't155', '衡山',
    't156', '都江堰',
    't158', '夜宴图',
    't162', '杜鹃',
    't163', '衡山',
    't164', '避暑山庄', '承德'
    't166', '瓷器', '景德镇',
    't167',
    '2000-3', '动物',
    '2000-8', '大理',
    '2000-14', '崂山',
    '2000-22', '神舟',
    '2000-24', '君子兰',
    '2001-3', '丑角',
    '2001-7', '聊斋',
    '2001-8', '武当山',
    '2001-13', '黄果树瀑布',
    '2001-22', '昭陵六骏',
    '2001-25', '六盘山',
    '2001-26', '民间传说', '白娘子',
    '2002-2', '八大山人',
    '2002-4', '民族乐器',
    '2002-5', '步辇图',
    '2002-6', '汝窑',

    '2002-7',
    '2002-8', '千山',
    '2002-9', '丽江',
    '2002-10', '灯塔',
    '2002-12', '黄河水利',
    '2002-16', '青海湖',
    '2002-19', '雁荡山',
    '2002-20', '中秋节',
    '2002-21', '壶口',
    '2002-20', '中秋节',
    '2002-23', '董永与七仙女',
    '2002-27', '长臂猿',

    '2003-2', '杨柳青',
    '2003-3', '古代书法', '篆书',
    '2003-4', '百合',
    '2003-5', '拱桥',
    '2003-7', '乐山大佛',
    '2003-8', '鼓浪屿',
    '2003-11', '网师园',
    '2003-12', '藏羚羊',
    '2003-13', '崆峒山',
    '2003-15', '晋祠',
    '2003-18', '重阳节',
    '2003-20', '梁山伯与祝英台',
    '2003-25', '毛泽东',
    '2003-26', '晋祠',
    '2003-15', '东周青铜器',

    '2004-2', '桃花坞',
    '2004-6', '孔雀',
    '2004-7', '楠溪江',
    '2004-8', '丹霞山',
    '2004-13', '古村落', '宏村', '西递',
    '2004-14', '柳毅传书',
    '2004-15', '八仙过海',
    '2004-24', '边陲风光',
    '2004-26', '清明上河图',
    '2004-27', '中国名亭',
    '2004-28', '隶书',

    '2005-4', '杨家埠',
    '2005-5', '玉兰花',
    '2005-7', '鸡公山',
    '2005-15', '向海',
    '2005-19', '梵净山',
    '2005-25', '洛神赋',

    '2006-2', '武强',
    '2006-3', '民间灯彩',
    '2006-4', '漓江',
    '2006-7', '青城山',
    '2006-8', '云冈石窟',
    '2006-9', '天柱山',
    '2006-15', '青藏铁路',
    '2006-16', '喀纳斯',
    '2006-23', '文房四宝',
    '2006-25', '长征 七十周年',
    '2006-29', '神骏图',
    '2006-30', '和谐铁路',

    '首日',
]

SEARCHES = [' '.join(item) for item in itertools.product(KEYS, ['寄'])]

