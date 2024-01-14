import requests
import json
from structure import Tree, TreeEncoder, Type
from requests.adapters import HTTPAdapter


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0 ",
    "referer": "https://browser.ihtsdotools.org/?perspective=full&conceptId1=404684003&edition=MAIN/2024-01-01&release=&languages=en",
}

proxies = {"http": "socks5://127.0.0.1:7890", "https": "socks5://127.0.0.1:7890"}


def get_request(url, params):
    s = requests.Session()
    s.mount("http://", HTTPAdapter(max_retries=3))
    s.mount("https://", HTTPAdapter(max_retries=3))

    try:
        response = s.get(
            url, params=params, headers=headers, timeout=15, proxies=proxies
        )  # 超时设置为15秒
        resptime_a = response.elapsed.total_seconds()  # 获取请求响应时间
        print("响应时间" + str(resptime_a) + "秒")
        if response.status_code == 200:
            content = json.loads(response.text)
            return content
    except requests.exceptions.RequestException as e:
        print(e)


def get_request_old(url, params):
    try:
        response = requests.get(
            url, params=params, headers=headers, timeout=15, proxies=proxies
        )  # 超时设置为15秒
        resptime_a = response.elapsed.total_seconds()  # 获取请求响应时间
        print("响应时间" + str(resptime_a) + "秒")
        if response.status_code == 200:
            content = json.loads(response.text)
            return content
    except Exception as e:
        for i in range(100):  # 循环2次去请求网站
            response = requests.get(
                url, params=params, headers=headers, proxies=proxies
            )
            print("循环第" + str(i) + "次")
            resptime_b = response.elapsed.total_seconds()
            print("响应时间" + str(resptime_b) + "秒")
            if response.status_code == 200:
                content = json.loads(response.text)
                return content
            if resptime_b < 10:  # 如果响应时间小于10秒，结束循环
                break


# 获取所有stroke相关的数据
def express(term: str, limit: int, pass_num: int):
    url = "https://browser.ihtsdotools.org/snowstorm/snomed-ct/browser/MAIN/2024-01-01/descriptions"
    params = {
        "limit": limit,
        "term": term,
        "active": True,
        "conceptActive": True,
        "lang": "english",
        "groupByConcept": True,
    }

    # response = requests.get(url, params=params, headers=headers, proxies=proxies)
    # if response.status_code == 200:
    if 1:
        content = get_request(url, params)
        # content = json.loads(response.text)
        for i, item in enumerate(content.get("items")):
            term = item.get("term")
            print(i, term)
            if i < pass_num:
                continue
            id = item.get("concept").get("id")
            result = Tree(term)
            getPro(id, result)
            getChildren(id, result)
            save_file(result)


def getChildren(id, tree):
    url = "https://browser.ihtsdotools.org/snowstorm/snomed-ct/browser/MAIN/2024-01-01/concepts/{}/children".format(
        id
    )
    params = {"form": "inferred"}
    if 1:
        content = get_request(url, params)
        # response = requests.get(url, params=params, headers=headers, proxies=proxies)
        # if response.status_code == 200:
        #     content = json.loads(response.text)
        if content:
            for c in content:
                a = Tree(c.get("pt").get("term"))
                tree.children.append(a)
                getPro(id, a)
                getChildren(c.get("id"), a)


def getPro(id, tree):
    url = "https://browser.ihtsdotools.org/snowstorm/snomed-ct/browser/MAIN/2024-01-01/concepts/{}".format(
        id
    )
    params = {"descendantCountForm": "inferred"}
    # response = requests.get(url, params=params, headers=headers, proxies=proxies)
    # if response.status_code == 200:
    #     content = json.loads(response.text)
    if 1:
        content = get_request(url, params)
        if content:
            for a in content.get("classAxioms"):
                for re in a.get("relationships"):
                    tree.relationships.append(
                        Type(
                            re.get("type").get("pt").get("term"),
                            re.get("target").get("pt").get("term"),
                        )
                    )


def save_file(tree: Tree):
    content = []
    with open("stroke.json", "r") as file:
        content = json.load(file)
    json_str = json.dumps(tree, cls=TreeEncoder)
    json_object = json.loads(json_str)
    content.append(json_object)
    with open("stroke.json", "w+") as file:
        json.dump(content, file)


def read_file():
    content = []
    with open("stroke.json", "r") as file:
        content = json.load(file)
    return len(content)


if __name__ == "__main__":
    # result = express("stroke", 1, read_file())
    print(read_file())
