from bs4 import BeautifulSoup
import requests
import database

link = "http://www.epiman.cn/forum-51-{}.html"
keywords = ["北大","北京大学","北医"]
session = database.Session()

def view_page(page):
    print(link.format(page))
    s = requests.session()
    bs = BeautifulSoup(s.get(link.format(page), headers="").content, "html.parser")

    tbodys = bs.find_all("tbody")

    for tbody in tbodys:
        try:
            data = tbody.find("a", {"class": "s xst"})
            for key in keywords:
                if key in data.getText():
                    print(data.getText())
                    print (data.get("href"))
                    if database.single(data.get("href")):
                        session.add(database.Doc(title=data.getText(),link=data.get("href")))
                        session.commit()
        except Exception:
            pass


if __name__ == "__main__":
    for i in range(327):
        view_page(i)