# SPDX-License-Identifier: GPL-2.0-or-later
"""Localised trophy names and descriptions.

The interface is one table: TEXT[language][trophy id] = (name, description). Every entry that a
language does not provide falls back to the English text in bbport_trophies.TROPHIES, so a
translation may cover a single trophy, a single group or the whole list, and it never renders an
empty row. Adding a language is therefore one dict block keyed by the launcher language code used
in bbport_lang.LANGUAGE_NAMES - no other file has to change.

Simplified Chinese uses the names and descriptions of the official PS4 release (the zh-Hans trophy
list of CUSA03023's Chinese build), not a literal translation of the English text.
"""
import bbport_trophies as trophies

LANGUAGES = ('zh',)

TEXT = {
    'zh': {
        # Official Simplified Chinese trophy text, base game.
        0: ('Bloodborne', '已获得所有战利品。脱帽!'),
        1: ('亚南日出', '你在经历过猎杀后活了下来，并看到了新的一天。'),
        2: ('履行愿望', '因月亮的出现而被迷惑，你发誓要照看好猎人之梦。'),
        3: ('童年的开始', '你成为大神的转世婴儿，领导人类进入下一个幼年时期。'),
        4: ('亚南，修梅里安女王', '击败亚南，古旧迷宫的血之女王。'),
        5: ('猎人的精髓', '获得所有猎人武器。'),
        6: ('猎人的手工', '获得所有特殊的猎人工具。'),
        7: ('武器大师', '获取一把最高级别的武器。'),
        8: ('神血宝石大师', '获得一颗极端稀有的神血宝石。'),
        9: ('符文大师', '获得一枚极端稀有的卡丽尔符文。'),
        10: ('凯因赫斯特', '进入凯因赫斯特，被遗忘的废墟城堡。'),
        11: ('圣诗班', '进入圣诗班的领域，他们是治愈教会中的高层人员。'),
        12: ('梦之源', '探索废弃的旧工场，这里是猎人的梦境之源。'),
        13: ('噩梦讲堂', '进入拜伦维斯教学楼，它漂流在噩梦的领域之中。'),
        14: ('加斯科因神父', '击败曾是加斯科因神父的怪兽。'),
        15: ('代理人阿梅利亚', '击败曾是薇卡·阿梅利亚的怪兽。'),
        16: ('亚南的影子', '击败亚南的影子。'),
        17: ('罗姆，空虚的蜘蛛', '击败大神：空虚的蜘蛛罗姆。'),
        18: ('重生之神', '击败重生之神。'),
        19: ('米克拉什，噩梦之主', '击败噩梦之主米克拉什。'),
        20: ('墨戈的乳母', '击败大神：墨戈的乳母。'),
        21: ('神职人员怪兽', '击败神职人员怪兽。'),
        22: ('缺血的怪兽', '击败缺血的怪兽。'),
        23: ('亨维科的女巫', '击败亨维科女巫。'),
        24: ('黑暗怪兽帕阿尔', '击败黑暗怪兽帕阿尔。'),
        25: ('阿米戈达拉', '击败大神：阿米戈达拉。'),
        26: ('殉道者洛加留斯', '击败殉道者洛加留斯。'),
        27: ('天庭使者', '击败大神：天庭使者。'),
        28: ('埃波利耶塔，宇宙之女', '击败大神：宇宙之女埃波利耶塔。'),
        29: ('神血宝石新手', '获得可为猎人武器附加特别力量的血之宝石。'),
        30: ('符文联系人', '获得可为猎人自身附加特别力量的卡丽尔符文。'),
        31: ('修梅露圣杯', '获得封印着构成亚南地下蛛网般结构的墓穴的修梅露圣杯。'),
        32: ('贫瘠洛然圣杯', '获得封印着深藏在沙漠中、发生了惨剧的贫瘠之地洛然的圣杯。'),
        33: ('伊兹圣杯', '获得伊兹大圣杯，它封印着宇宙眷族的居所。'),
        # The Old Hunters.
        34: ('老猎人的精华', '获得所有老猎人武器。'),
        35: ('科斯孤儿', '打败大神：科斯孤儿。'),
        36: ('路德维格，神圣之剑', '打败曾经是路德维希的野兽，神圣之剑。'),
        37: ('精神钟塔的玛利亚修女', '打败精神钟塔的玛利亚修女。'),
        38: ('失败者', '击败没能成为大神的人。'),
        39: ('劳伦斯，第一个代理人', '打败曾经是劳伦斯的野兽，第一个代理人。'),
    },
}

GROUP_NAMES = {
    'zh': {
        trophies.BASE: '血源诅咒',
        trophies.DLC: '老猎人',
    },
}

# The Traditional table is generated from the Simplified one (scripts/generate_hant.py), so the two
# never drift apart; when the generated file is missing, zh-hant simply falls back to English.
try:
    import bbport_trophy_text_hant as _hant
except ImportError:  # pragma: no cover - the generated file ships with the launcher
    _hant = None
else:
    TEXT['zh-hant'] = _hant.TEXT
    GROUP_NAMES['zh-hant'] = _hant.GROUP_NAMES
    LANGUAGES = LANGUAGES + ('zh-hant',)


def _table(language):
    """The rows for one language, treating `zh-hant` as Traditional Chinese, not as unknown."""
    return TEXT.get(language) or {}


def text(trophy, language):
    """(name, description) for one trophy row, in the requested language when it has one."""
    entry = TEXT.get(language, {}).get(trophy[0])
    return entry if entry else (trophy[1], trophy[2])


def group(name, language):
    """The localised name of a trophy group (the base game or the expansion)."""
    return GROUP_NAMES.get(language, {}).get(name, name)


def coverage(language):
    """(translated, total) for one language; total is every trophy the launcher knows."""
    have = TEXT.get(language, {})
    return sum(1 for trophy in trophies.TROPHIES if trophy[0] in have), len(trophies.TROPHIES)
