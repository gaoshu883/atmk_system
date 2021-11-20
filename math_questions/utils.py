from bs4 import BeautifulSoup
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
        key = 'HOLEL_%d_WLDOR_%d' % (id, inx)
        math = tag.replace_with(key)
        math_dict[key] = str(math)
    text = content.get_text()
    '''清除空格、序号、答案括号等字符'''
    text = ''.join(text.split())  # 空格去不掉的解决方法
    text = re.sub(r'(（）)|(（\d+）、)|(\(\d+\)、)|(\d+、)|([A-Z]、)', '', text)
    return text, math_dict


def remove_similar(contents: list):
    '''
    题目去重
    对相似度高的题目进行警告处理
    '''
