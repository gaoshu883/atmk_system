from bs4 import BeautifulSoup
import jieba
import re


def clean_html(raw_html: str = '', id: int = 0):
    soup = BeautifulSoup(raw_html, 'html.parser')
    content = soup.select_one('.exam-con')
    '''删除无用标签'''
    drop = []
    table_tag = soup.select('table')
    input_tag = soup.select('input')
    img_tag = soup.select('img')
    drop.extend(table_tag)
    drop.extend(input_tag)
    drop.extend(img_tag)
    for item in drop:
        item.decompose()
    '''数学表达式替换-提取'''
    math_dict = {}
    for inx, tag in enumerate(soup.select('math')):
        key = 'HEL_%d_WLDOR_%d_OL' % (id, inx)
        math = tag.replace_with(key)
        math_dict[key] = str(math)
    text = content.get_text()
    '''清除空格、序号、答案括号等字符'''
    text = ''.join(text.split())  # 空格去不掉的解决方法
    text = re.sub(r'(（）)|(（\d+）、)|(\(\d+\)、)|(\d+、)|([A-Z]、)', '', text)
    '''将模式替换成公式'''
    math_text = re.sub(r'HEL_\d+_WLDOR_\d+_OL',
                       lambda matched: replace_formula(matched, math_dict), text)
    math_text = ''.join(math_text.split())  # 去除空字符
    '''
    切字、词
    文本按公式拆分成块处理
    '''
    char_list = []
    word_list = []
    text_list = re.sub(r'HEL_\d+_WLDOR_\d+_OL',
                       lambda matched: 'HELLO_WORLD', text).split('HELLO_WORLD')
    for u in text_list:
        char_list.extend(cut_char(u))
        word_list.extend(cut_word(u))

    return text, math_dict, math_text, char_list, word_list


def replace_formula(matched, formulas) -> str:
    value = matched.group()
    if value in formulas:
        return formulas[value]
    return value


def remove_same(contents: list):
    '''
    题目去重
    对一样的题目进行警告处理
    id,text,formulas,math_text
    利用math_text进行比较
    '''
    print('开始检查重复项...')
    ret = {}
    temp = []
    for u in contents:
        f_id = u['id']
        text = u['math_text']
        if text in ret:
            print('题目 %d 和题目 %d' % (f_id, ret[text]))
        else:
            ret[text] = f_id
            temp.append(u)
    print('检查完毕^^')
    return temp


def cut_char(text: str) -> list:
    '''
    切字符
    '''
    return ''.join(text.split())


def cut_word(text: str) -> list:
    '''
    切词
    '''
    seg_list = jieba.cut(text, cut_all=False)
    return seg_list
