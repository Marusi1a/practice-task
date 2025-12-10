import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

wiki_page = input("Put first wiki link: ")
keywords = ["Hitler", "dictator", "war"]
target = "https://en.wikipedia.org/wiki/Adolf_Hitler"


# ім'я користувача щоб уникнути блокувань на вікіпедії, бо та не пускає ботів
def get_html(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.text

def get_first_relevant_link(url):
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")

    content = soup.find("div", {"id": "mw-content-text"})
    if not content:
        return None

    links = content.find_all("a", href=True)

    # Зберігаємо перший лінк та окремі ключові лінки
    first_link = None
    uni_link = None
    school_link = None
    math_link = None

    for a in links:
        href = a.get("href")
        if not href or not href.startswith("/wiki/"):
            continue

        # ігнорувати службові сторінки
        if ":" in href:
            continue
        href_lower = href.lower()
        if "disambiguation" in href_lower:
            continue

        # перший звичайний лінк
        if first_link is None:
            first_link = href

        text = a.get_text().lower()

        # Пріоритетний пошук
        if ("Hitler" in href_lower or "hitler" in text) and uni_link is None:
            uni_link = href

        elif ("Dictator" in href_lower or "dictator" in text) and school_link is None:
            school_link = href

        elif ("War" in href_lower or "war" in text) and math_link is None:
            math_link = href

    # Вибір за пріоритетами
    if uni_link:
        return uni_link
    if school_link:
        return school_link
    if math_link:
        return math_link

    return first_link




#цикл для пошуку лінків
current =  wiki_page
found = False

for step in range(6):
    print(f"Крок {step + 1}: {current}")

    if target in current:
        found = True
        break

    next_link = get_first_relevant_link(current)
    if not next_link:
        break

    current = urljoin("https://en.wikipedia.org", next_link)

# Виведення результату
if found or (target in current):
    print("Hitler found!", current)
else:
    print("Hitler not found")
