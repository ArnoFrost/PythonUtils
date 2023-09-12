# 书签处理工具
import json
import time

from bs4 import BeautifulSoup

from scripts.common.bookmark.book_data import Bookmark


def preprocess_data(file_path: str):
    """
        预处理数据
    :return:
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        html_doc = f.read()

    soup = BeautifulSoup(html_doc, 'html.parser')
    for dt in soup.find_all('dt'):
        a = dt.find('a')
        if a:
            # 对于 <A> 标签
            url = a.get('href')
            title = a.text
            add_date = a.get('add_date')
            # 转换时间戳为可读的时间
            add_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(add_date)))
            print(f"Title: {title}, URL: {url}, Added Date: {add_date}")
        else:
            # 对于 <H3> 标签
            h3 = dt.find('h3')
            if h3:
                dir_name = h3.text
                add_date = h3.get('add_date')
                last_modified = h3.get('last_modified')
                # 转换时间戳为可读的时间
                add_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(add_date)))
                last_modified = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(last_modified)))
                print(f"Directory: {dir_name}, Added Date: {add_date}, Last Modified: {last_modified}")


def preprocess_bookmark(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        html_doc = f.read()

    soup = BeautifulSoup(html_doc, 'html.parser')

    bookmarks = []
    tags = []

    for dt in soup.find_all('dt'):
        a = dt.find('a')
        if a:
            # 对于 <A> 标签
            url = a.get('href')
            title = a.text
            add_date = a.get('add_date')
            # 转换时间戳为可读的时间
            add_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(add_date)))

            bookmark = Bookmark(title, url, add_date, tags.copy())
            bookmarks.append(bookmark)
        else:
            # 对于 <H3> 标签
            h3 = dt.find('h3')
            if h3:
                dir_name = h3.text
                tags.append(dir_name)

    for bookmark in bookmarks:
        print(bookmark)


def extract_bookmarks(file_path):
    with open(file_path, 'r') as f:
        contents = f.read()

    soup = BeautifulSoup(contents, 'lxml')
    dt_tags = soup.find_all('dt')

    # Build a dict for storing id-path pairs
    path_dict = {}

    def traverse(node, path):
        if node.h3:  # this is a directory
            new_path = path + [node.h3.string] if node.h3.string != "Bookmarks" else list(path)  # create a new instance
            path_dict[id(node)] = new_path
            for child in node.find_all('dt', recursive=False):
                traverse(child, new_path)
        else:  # this is a bookmark
            path_dict[id(node)] = list(path)  # create a new instance for bookmark as well

    for dt in dt_tags:
        if dt.parent.name == 'dl':  # top level nodes
            traverse(dt, [])

    # Use path_dict to process each bookmark
    bookmarks = {}
    for dt in dt_tags:
        if dt.a:  # this is a bookmark
            title = dt.a.string
            add_date = dt.a.get('add_date')
            # 转换时间戳为可读的时间
            add_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(add_date)))
            url = dt.a['href']
            try:
                path = path_dict[id(dt)]
            except KeyError:
                print(f"Could not find path for bookmark: {title}")
                continue
            tags = ['#' + tag for tag in path]
            bookmark = Bookmark(title, url, add_date, tags)
            bookmarks[title] = bookmark
            print(f'Added bookmark: {title} - {url} - {tags}')

    return bookmarks


def print_bookmarks(file_path):
    with open(file_path, 'r') as f:
        contents = f.read()

    soup = BeautifulSoup(contents, 'lxml')
    dt_tags = soup.find_all('dt')

    # Build a dict for storing id-path pairs
    path_dict = {}

    def traverse(node, path):
        if node.h3:  # this is a directory
            new_path = path + [node.h3.string] if node.h3.string != "Bookmarks" else path  # ignore "Bookmarks"
            path_dict[id(node)] = new_path
            for child in node.find_all('dt', recursive=False):
                traverse(child, new_path)
        else:  # this is a bookmark
            path_dict[id(node)] = path
            # print the path for debugging
            print(' -> '.join(path + [node.a.string if node.a else "None"]))

    for dt in dt_tags:
        if dt.parent.name == 'dl':  # top level nodes
            traverse(dt, [])


def save_bookmarks_to_json(bookmarks, file_path):
    # 将 Bookmark 对象转换为可以序列化为 JSON 的字典
    bookmarks_dict = {title: bookmark.__dict__ for title, bookmark in bookmarks.items()}

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(bookmarks_dict, f, ensure_ascii=False, indent=4)


from bs4 import BeautifulSoup
import csv
import time


def bookmarks_html_to_csv(html_file_path, csv_file_path):
    with open(html_file_path, 'r') as f:
        contents = f.read()

    soup = BeautifulSoup(contents, 'lxml')
    dt_tags = soup.find_all('dt')

    # 创建一个字典存储每个节点及其对应的路径（标签）
    path_dict = {}

    def traverse(node, path):
        if node.h3:  # 这是一个目录
            new_path = path.copy()  # 创建path的副本
            new_path.append(node.h3.string)  # 向新路径中添加当前目录
            path_dict[id(node)] = new_path
            for child in node.find_all('dt', recursive=False):
                traverse(child, new_path)  # 使用new_path，它包含了当前目录的名称
        else:  # 这是一个书签
            path_dict[id(node)] = path  # 在处理书签时，我们只需要记录它所在的路径，不需要再添加当前目录的名称

    for dt in dt_tags:
        if dt.parent.name == 'dl':  # 顶级节点
            traverse(dt, [])

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'URL', 'Add_Date', 'Modify_Date', 'Tags']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for dt in dt_tags:
            if dt.a:  # 这是一个书签
                title = dt.a.string
                url = dt.a['href']
                add_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(dt.a.get('add_date'))))
                modify_date = dt.a.get('last_modified')
                if modify_date:
                    modify_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(modify_date)))
                try:
                    tags = ','.join(path_dict[id(dt.parent)])
                except:
                    print(f"Could not find path for bookmark: {title}")
                    continue
                writer.writerow(
                    {'Title': title, 'URL': url, 'Add_Date': add_date, 'Modify_Date': modify_date, 'Tags': tags})


if __name__ == '__main__':
    html_file_path = '/Users/xuxin14/Desktop/favorites_2023_6_21.html'
    csv_file_path = '/Users/xuxin14/Desktop/favorites_2023_6_21.csv'
    bookmarks_html_to_csv(html_file_path, csv_file_path)

# if __name__ == '__main__':
#     bookmark_file_path = "/Users/xuxin14/Desktop/favorites_2023_6_19.html"
#     # bookmarks = extract_bookmarks(bookmark_file_path)
#     # output_file_path = "/Users/xuxin14/Desktop/bookmarks.json"
#     # save_bookmarks_to_json(bookmarks, output_file_path)
#     # print("=======================")
#     # print(f"Total bookmarks: {len(bookmarks)}")
#
#     print_bookmarks(bookmark_file_path)

"""
<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
    <DT><H3 ADD_DATE="1678687154" LAST_MODIFIED="1678687154">往日纪念</H3>
    <DL><p>
        <DT><A HREF="https://www.douban.com/note/707952128/" ADD_DATE="1559203016" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABQElEQVQ4jWO0mOh64tkZBuKAhZQJI0O5IJGqYaBc0GNW8H8igMesYIZyQRYGBoZbr+7Ub28naPKtV3cYGBigThL4z0mMaz4wfmeBsLSldI/k7/j//z8jI+N/VEWMDAwMDAw2Ez2OPj/FwMDAgix3792Dok1lv39+ZWBhZ/jPwPD/N8O/f5NDpyoLK0IUCPznRNHAzsZ58NoxNGd8/fMTmYui4eev7woSSmgauFnYcWpQFla8UHwYm28xNFx9dtljVsiOtDV///8z6rLlYOVkYGD48fv7xfKj337/CJofc/XZZYj3ETacvHv8/ruHcgIyD988QDby5eeXO+/tE2DghAQ9E0T0A+P3D4zf117azMzEHGkaARGEMNZe2gxRADOhXHDy4VnEJI3Jh2dBk8aRByeEOYXw+xWijIGBgZHU5A0Arsa8Mw6SBsUAAAAASUVORK5CYII=">那时候买了不少《软件指南》《软件应用指南》等</A>
        <DT><A HREF="http://localhost/wordpress/wp-login.php" ADD_DATE="1558938830" ICON="">Log In ‹ FoxHound — WordPress</A>
        <DT><H3 ADD_DATE="1678687154" LAST_MODIFIED="1678687154">往日技术-起步</H3>
        <DL><p>
            <DT><H3 ADD_DATE="1678687154" LAST_MODIFIED="1678687154">三方库</H3>
            <DL><p>
                <DT><H3 ADD_DATE="1678687154" LAST_MODIFIED="1678687154">图片加载</H3>
                <DL><p>
                    <DT><H3 ADD_DATE="1678687154" LAST_MODIFIED="1678687154">fresco</H3>
                    <DL><p>
                        <DT><A HREF="http://www.jianshu.com/p/8ff81be83101" ADD_DATE="1510726759" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAACY0lEQVQ4jSXRTW9UVRzH8d/vf865dwZuZ5gZGBgeijwVF/IQgwqJhsSVOxISjLwAo++Bl0DcsXNj3LgxvgCNGGOMuCERIjGB2lYy5aGk7XQ67dy595yfi+4/q++Xw7t3QEgkoViDRjOQSEmxhjmaAQQkiaSBlEBISa7VtUauGNOsFM33j1meCVJVKiWSkgwSSCkiFN1Pv5h79yJ8Fo4MWBzs3f68eeZUnOyEE6ddM1eMJLwAkrGsivc/zLqtePCtA5+cC925elKbRzb/drtzct/FK7PHv238eh8uN9LSdBJOvlNcWFj79h5ax7C5tPXgoW+kN999k529jPHq2tdfjR/9RZ9BMsXK2oPW1Q+2fvrBHV3gbKNcH2fzg/HvP9ejcbmyKJeHXi+ONgEQMEgMbvuPH3f+eRInZeh0qrXXKqe+P19culwNF/Pz13o3P/NFAymJ9PQhbbyMaHRufVkvPxr9+bBxZqH675nMZ4Pj5b9/o9G3Wag3t5E1KJkkugCj7w4sx/TZUnHlI9/r2Fx3/3vXm6dPKUYJUiIJ0giIQB3TZDtOthm86ormSEu7W7MXzwUjsTcBgIEkIAAkzSSoLmerK7PhimpYcz+xJ/cgPABJdJ4hKCbm3op2Nn8u1c4196mqUddALogSAA+JAswsy2hmwVWry+XSU8mXR09Y+5A/3KftUAQJyIOUkkhA9KFaebL+ajFNd6E0+mW39fGN4vzZrfvfyxwJJHB4944g0If+IK6/SLMKMBpBpnLX2oezQ91y+SnoCAD0AEiDYjVcggs0h70GKVne1GR9OnrNLCcACcT/hPIvAZ0pDQQAAAAASUVORK5CYII=">你所不知道的fresco使用集锦 - 简书</A>
                        <DT><A HREF="https://www.cnblogs.com/peiandsky/p/4394779.html" ADD_DATE="1510727131" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACh0lEQVQ4jX2TT2hUVxTGf+fe95LMmLwBI7UxKqWKtmkXSR6TPKOjiBtX1q2CqKhUcZ3SRXddS8GVi7ZQiigtzbr1H4jBSRhHAkEXMhv1hU7EJtFJHJ3Mu8eFbyTa6Le899zv/r5zOMJHVIiGTovYY4BR1Uu3JiZ+er/GrvLOAFqIou/Emu/V6XngjjFmdFNv77pHcXwDkFaxrGJAX19fZ3cu94Bm89CtUukmQD7f35+xHVeXa7XtxXv35lb+9j/lcrkcAv8tLZVTSlsqTU2r8IIg+OJ9XBuGob/ysFgsVkW1ujYIfgASINk9PDwKqHXuxPDWrUGr1gvDsLPD9/cBYytiJc7pKWvNX4WRaKcgTp1uEHWXjeedle7uc1Qq9wEx5XL5mYU9I/l8/0qK8cnJ8lxtcQDhN9T98WR+ftCJ2eZ5XqdC2ErgATh4YjzvDPBtSqCATE9PzwM/AxSGhg6KyDfOuUSMjAC/A2oAXJJcEfRAGIbr3vhBauIBRNHgl8azF6wxRlWtqubT/jkDcLtUuouoZn3/SHrRlpo0C2E02Gbar3u+t345af7qXFKy1n5VGBjobk3BAAlO/gZOpwSNfD7/6a4o+tG2mxsiMld/2Tg0Xpw8kaj7xYjpcG1tW2ghpn340/fs8cKOoVEV0y7wtaosJXCytvTi2tTU1AIgSb3xT5K1iRj9HJiwaVY2wox0de0VMUdRdgLtItRwurbD97f0bt6gjx/PxHG1urB5U+9+g1QfxjPjbwmKcVwnjveEYbimq15PapmMzTQaRoOgOTs726hUKq/SuKrKReCzdyK0mlYul5/xYTmA+sLzsUwQHAZktW0UPrBkLf379OniJz09c9lstvYaxI/3vPRLsl0AAAAASUVORK5CYII=">OkHttp+Stetho+Chrome调试android网络部分（原创） - peiandsky - 博客园</A>
                        <DT><A HREF="http://www.fresco-cn.org/" ADD_DATE="1510726759" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABlElEQVQ4jaWTPYhTURCFv5l732bj3yqCcYt0NiJsE0SsFmwsZHsLsdNWaysLW0EEESyEbewURVjZThC1MYKIlYLixkJEFIJZdt+bGQsJvMQkKp7q3uHOx5zDXBhTgATI8Fyr6/jbmYoORR06DSLjhR8nWWzuSDfdbdWFj1nS1cE3Oz2/L60gsXzlnp+9DD4RsHGcZqul1zQowxjkhFWBAqIqTfNoFJ/8onQZDHtGRlposFMqNj14G0qrrHivyteAvVbxSkF7c0S9ZwTwuUefQg4npS3hq6ngvIb0gDc5x4UQv91+zuZUwKF3lGZ2XVSWRFI7xG8EnBPzl7LlJ4oHPBvPbDTVJZoZPWVVPHHiqLgeMI8XsU1fHvElIM0GLNKoggSoBuJGKcquosACRMBmArrr9LPKwZyYD/xuypzBfE3WeC2MhjdUrl86UG2F3SLSpYAPsuHHcpdyUuNkCx32qOhKtR33QZN0Kesb+WfAbgQnFXMcUfz7L1+/+54OeExfs+wPkaf5IXcApLa2f6V//nX/C/kJvfydIq7KEiIAAAAASUVORK5CYII=">www.fresco-cn.org</A>
                    </DL><p>
                </DL><p>
                <DT><H3 ADD_DATE="1678687154" LAST_MODIFIED="1678687154">优化</H3>
                <DL><p>
                    <DT><A HREF="https://github.com/badoo/android-weak-handler" ADD_DATE="1626960867" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABeklEQVQ4jY3Tv2qVQRAF8PPdP7k3itoE7SOIKFZiDAZsfBJFfBDRQjBFGkFiJ/gKerGwsRAsvaKFFhYWgo3GxEA0P4vMhTUk4sDy7c6cMztzZr9kn2EFD/Eem7Xele/yfnxLnMP9Isxst9bMfhRmriX2MMLE/9ukOL1ZktUKvMANvMIGpnhT+9e4jmeFvTcjL2ELv7BevjFOYYgBFjBfsbXCbuLiIMnNJPPV0Tb6XddtJ9luJPqKDv0kO0n6SY4kuZVSeBc/cabRpWt06mZnLJaYu5im+oPPGB06pr9Fn1aCjV6SYcWOJhm3Nx9A7pKMkywk6ZIMe0k+JJHkRJLlruugf0ALg67rJFlJcrI4H4NHVc53fMLZf1RwDm/xu9peD5brcBuPa/8cSw3xAp7gW8V3apSXZoC1quI87uApTjcJFptXuFXf1VbVPl7WSK+1txdmjC9Nkom9f6fXggZ40ICON7Fj1feOvWc/zGGGK9XGqPGNcBdX9+P/AO1cPr7g2LjWAAAAAElFTkSuQmCC">badoo/android-weak-handler：android.os.Handler 的内存安全实现</A>
                </DL><p>
            </DL><p>
            <DT><H3 ADD_DATE="1678687154" LAST_MODIFIED="1678687154">基础知识</H3>
            <DL><p>
                <DT><H3 ADD_DATE="1678687154" LAST_MODIFIED="1678687154">动态权限</H3>
                <DL><p>
                    <DT><A HREF="http://www.jianshu.com/p/b5c494dba0bc" ADD_DATE="1511923514" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAACY0lEQVQ4jSXRTW9UVRzH8d/vf865dwZuZ5gZGBgeijwVF/IQgwqJhsSVOxISjLwAo++Bl0DcsXNj3LgxvgCNGGOMuCERIjGB2lYy5aGk7XQ67dy595yfi+4/q++Xw7t3QEgkoViDRjOQSEmxhjmaAQQkiaSBlEBISa7VtUauGNOsFM33j1meCVJVKiWSkgwSSCkiFN1Pv5h79yJ8Fo4MWBzs3f68eeZUnOyEE6ddM1eMJLwAkrGsivc/zLqtePCtA5+cC925elKbRzb/drtzct/FK7PHv238eh8uN9LSdBJOvlNcWFj79h5ax7C5tPXgoW+kN999k529jPHq2tdfjR/9RZ9BMsXK2oPW1Q+2fvrBHV3gbKNcH2fzg/HvP9ejcbmyKJeHXi+ONgEQMEgMbvuPH3f+eRInZeh0qrXXKqe+P19culwNF/Pz13o3P/NFAymJ9PQhbbyMaHRufVkvPxr9+bBxZqH675nMZ4Pj5b9/o9G3Wag3t5E1KJkkugCj7w4sx/TZUnHlI9/r2Fx3/3vXm6dPKUYJUiIJ0giIQB3TZDtOthm86ormSEu7W7MXzwUjsTcBgIEkIAAkzSSoLmerK7PhimpYcz+xJ/cgPABJdJ4hKCbm3op2Nn8u1c4196mqUddALogSAA+JAswsy2hmwVWry+XSU8mXR09Y+5A/3KftUAQJyIOUkkhA9KFaebL+ajFNd6E0+mW39fGN4vzZrfvfyxwJJHB4944g0If+IK6/SLMKMBpBpnLX2oezQ91y+SnoCAD0AEiDYjVcggs0h70GKVne1GR9OnrNLCcACcT/hPIvAZ0pDQQAAAAASUVORK5CYII=">Android各大手机品牌手机跳转到权限管理界面 - 简书</A>
                </DL><p>
                <DT><H3 ADD_DATE="1678687154" LAST_MODIFIED="1678687154">状态栏</H3>
                <DL><p>
                    <DT><A HREF="http://blog.csdn.net/guolin_blog/article/details/51763825" ADD_DATE="1510725685">Android状态栏微技巧，带你真正理解沉浸式模式 - 郭霖的专栏 - 博客频道 - CSDN.NET</A>
                </DL><p>
                <DT><H3 ADD_DATE="1678687154" LAST_MODIFIED="1678687154">View</H3>
                <DL><p>
                    <DT><A HREF="http://blog.csdn.net/harvic880925/article/details/69787359" ADD_DATE="1498638025">自定义控件三部曲视图篇（三）——瀑布流容器WaterFallLayout实现 - 启舰 - 博客频道 - CSDN.NET</A>
                    <DT><A HREF="https://www.cnblogs.com/fuck1/p/5456337.html" ADD_DATE="1512003674" ICON="">Android的startActivityForResult()与onActivityResult()与setResult()参数分析，activity带参数的返回 - 我所向往的美好 - 博客园</A>
                    <DT><A HREF="http://www.jianshu.com/p/3c471953e36d" ADD_DATE="1499074403" ICON="">Android可伸缩布局－FlexboxLayout(支持RecyclerView集成) - 简书</A>
                    <DT><A HREF="http://blog.csdn.net/wangrain1/article/details/72764086" ADD_DATE="1498627863">Android自定义view基础详解及开发流程 - WangRain1的博客 - 博客频道 - CSDN.NET</A>
                </DL><p>
            </DL><p>
        </DL><p>
        </DL><p>
    <DT><A HREF="https://www.baidu.com/" ADD_DATE="1525225997" ICON="">百度一下，你就知道</A>
</DL><p>

"""
