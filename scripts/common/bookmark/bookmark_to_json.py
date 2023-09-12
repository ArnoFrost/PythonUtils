from bs4 import BeautifulSoup
import json


def process_bookmarks(input_filepath, output_filepath):
    with open(input_filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    result = {
        'name': 'root',
        'children': [],
        'web': []
    }
    dl = soup.find('dl')
    process_dl(dl, result)
    json_output = json.dumps(result, indent=4)

    with open(output_filepath, 'w', encoding='utf-8') as json_file:
        json_file.write(json_output)


def process_dl(dl, node):
    dts = dl.find_all('dt', recursive=False)
    for dt in dts:
        h3 = dt.find('h3')
        if h3 is not None:
            child_node = {
                'name': h3.get_text(),
                'children': [],
                'web': []
            }
            node['children'].append(child_node)
            child_dl = dt.find('dl')
            if child_dl is not None:
                process_dl(child_dl, child_node)
        else:
            a = dt.find('a')
            if a is not None:
                node['web'].append({
                    'url': a.get('href'),
                    'title': a.get_text(),
                    'desc': a.get_text(),
                    'logo': a.get('icon')
                })


if __name__ == '__main__':
    # 提供输入的HTML书签文件的路径和输出的JSON文件的路径
    bookmark_file_path = '/Users/xuxin14/Desktop/favorites_2023_6_21.csv'
    bookmark_json_path = '/Users/xuxin14/Desktop/test_bookmarks.json'
    process_bookmarks(bookmark_file_path, bookmark_json_path)
