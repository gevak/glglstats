# Source of lists:
# https://he.wikipedia.org/wiki/%D7%9E%D7%A6%D7%A2%D7%93_%D7%94%D7%A4%D7%96%D7%9E%D7%95%D7%A0%D7%99%D7%9D_%D7%94%D7%A2%D7%91%D7%A8%D7%99_%D7%94%D7%A9%D7%A0%D7%AA%D7%99
# https://he.wikipedia.org/wiki/%D7%9E%D7%A6%D7%A2%D7%93_%D7%94%D7%A4%D7%96%D7%9E%D7%95%D7%A0%D7%99%D7%9D_%D7%94%D7%A2%D7%91%D7%A8%D7%99_%D7%94%D7%A9%D7%A0%D7%AA%D7%99_(%D7%94%27%D7%AA%D7%A9%22%D7%A3_%D7%95%D7%90%D7%99%D7%9C%D7%9A)
from collections import OrderedDict
from common import SongId

YEARS = list(range(1969, 2021))


PIZMONET_PAGES = [
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%9B%22%D7%98",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%22%D7%9C",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%9C%22%D7%90",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%9C%22%D7%91",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%9C%22%D7%92",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%9C%22%D7%93",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%9C%22%D7%94",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%9C%22%D7%95",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%9C%22%D7%96",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%9C%22%D7%97",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%9C%22%D7%98",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%22%D7%9D",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%9E%22%D7%90",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%9E%22%D7%91",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%9E%22%D7%92",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%9E%22%D7%93",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%9E%22%D7%94",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%9E%22%D7%95",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%9E%22%D7%96",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%9E%22%D7%97",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%9E%22%D7%98",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%22%D7%9F",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%A0%22%D7%90",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%A0%22%D7%91",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%A0%22%D7%92",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%A0%22%D7%93",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%A0%22%D7%94",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%A0%22%D7%95",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%A0%22%D7%96",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%A0%22%D7%97",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%A0%22%D7%98",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%22%D7%A1",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%A1%22%D7%90",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%A1%22%D7%91",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%A1%22%D7%92",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%A1%22%D7%93",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%A1%22%D7%94",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%A1%22%D7%95",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%A1%22%D7%96",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%A1%22%D7%97",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%A1%22%D7%98",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%22%D7%A2",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%A2%22%D7%90",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%A2%22%D7%91",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%A2%22%D7%92",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%A2%22%D7%93",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%A2%22%D7%94",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%A2%22%D7%95",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%A2%22%D7%96",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%A2%22%D7%97",
    "http://pizmonet.co.il/wiki/%D7%AA%D7%A9%D7%A2%22%D7%98",
]

ARTISTS = OrderedDict()
ARTISTS["של פעם"] = ["זוהר ארגוב", "כוורת", "יהודית רביץ", "עופרה חזה", "אריק איינשטיין", "ריטה", "מתי כספי",
                     "מרגלית צנעני", "צביקה פיק", "אהוד בנאי", "חווה אלברשטיין", "שלום חנוך", "כוורת", "יהודה פוליקר",
                     "מאיר אריאל"]
ARTISTS["חדשים"] = ["נועה קירל", "אלה לי", "רביד פלוטניק", "טונה", "עדן חסון", "עדן בן זקן", "חנן בן-ארי", "איתי לוי",
                    "עדי ביטי", "סטטיק", "עומר אדם", "אליעד נחום", "יסמין מועלם", "אלון עדר"]
ARTISTS["רוק"] = ["הדורבנים", "היהודים", "מוקי", "רמי פורטיס", "ברי סחרוף", "אביב גפן", "החברים של נטאשה", "ג'ירפות",
                  "מרסדס בנד", "יוני בלוך", "הבילויים", "איפה הילד", "כנסיית השכל", "מוניקה סקס", "שלומי שבן", "תיסלם", "דודו טסה"]
ARTISTS["ראפ"] = ["סאבלימינל", "סטטיק", "טונה", "פלד", "רביד פלוטניק", "ג'ימבו ג'יי", "קפה שחור חזק"]
ARTISTS["היפ הופ"] = ["הדג נחש", "שב\"ק ס'", "נועה קירל", "רביד פלוטניק", "נטע ברזילי"]
ARTISTS["מזרחי"] = ["זוהר ארגוב", "איתי לוי", "מרגלית צנעני", "עומר אדם", "אייל גולן", "שרית חדד", "עדן חסון",
                    "עדן בן זקן", "משה פרץ", "עופר לוי", "ליאור נרקיס", "קובי פרץ", "זהבה בן", "דודו אהרון", "פאר טסי",
                    "שלומי שבת"]
ARTISTS['רגאיי'] = ["מוש בן ארי", "שוטי הנבואה", "אברהם טל", "התקווה 6"]
ARTISTS["פופ"] = ["אתניקס", "דודו פארוק", "סטטיק", "ג'יין בורדו", "נתן גושן", "עילי בוטנר", "תומר יוסף", "טיפקס", "עידן עמדי", "אפרת גוש", "משינה"]
ARTISTS["אחר"] = ["אביתר בנאי", "תומר יוסף", "יובל המבולבל", "קרולינה", "עברי לידר", "רמי קלינשטיין", "שלמה ארצי", "קרן פלס", "עידן רייכל"]

DEFAULT_ARTISTS = ["נועה קירל", "יובל המבולבל", "הדורבנים"]
ALL_ARTISTS = list(set([artist for category in ARTISTS for artist in ARTISTS[category]]))

year_to_wiki_str = {
    2020: """"שלמים" – עידן רפאל חביב (עקיבא תורג'מן ואבי אוחיון/עקיבא תורג'מן, אבי אוחיון ומתן דרור)
"אם תרצי" – חנן בן-ארי (חנן בן-ארי)
"מיליון דולר" – נועה קירל עם שחר סאול (נועה קירל, ירדן פלג, רון ביטון ואיתי שמעוני)
"ואז את תראי" – דולי ופן עם דיקלה ועידן חביב (דולב רם ופן חזות)
"זוט עני" – אלה לי להב (יונתן גולדשטיין, רון ביטון וסקוט קין)
"שמש" – חנן בן-ארי (חנן בן-ארי)
"אל תעזבי ידיים" – עקיבא תורג'מן (עקיבא תורג'מן וצורית תורג'מן)
"אגרוף" – עדן בן זקן (אורי בן ארי/אורי בן ארי ואיתן דרמון)
"סיבובים" – עדן חסון (עדן חסון וסתיו בגר)
"נחכה לך" – נתן גושן וישי ריבו (נתן גושן)
"שבוע טוב" – אברהם טל (אברהם טל, בניה ברבי ואבי אוחיון/אברהם טל, בניה ברבי, אבי אוחיון ומתן דרור)
"בין קודש לחול" – אמיר דדון ושולי רנד (שחר הדר/אמיר דדון)
"את חסרה לי" – עדן חסון (עדן חסון, דולב רם ופן חזות)
"לא יוצא למסיבות" – יהונתן מרגי (יהונתן מרגי, יונתן גולדשטיין ורון ביטון)
"באת לי פתאום" – קרן פלס ורוני אלטר (קרן פלס)
"חביב אלבי" – סטטיק ובן-אל תבורי עם נסרין קדרי (לירז רוסו וירדן פלג)
"Alien" – דניס לויד (ניר טיבור, תום ברנס, פיט קלהר, בן קון וניק אטקינסון)
"Feker Libi" – עדן אלנה (דורון מדלי ועידן רייכל)
"יש לי חור בלב בצורה שלך" – ג'ירפות (גלעד כהנא/גלעד כהנא ועטר מיינר)
"מאושרים" – דולי ופן עם נועה קירל ולירן דנינו (דולב רם ופן חזות)
"אם אתה גבר" – נועה קירל (ירדן פלג, דורון מדלי ואיתי שמעוני)
"קוקוריקו" – עדן בן זקן ועומר אדם (עומר אדם, עדן בן זקן, אלעד טרבלסי, מאור תיתון, משה בן אברהם ואופק יקותיאל)
"רכבת הרים" – אייל גולן (מורן דוד ואבישי רם)
"פשוטים" – עקיבא תורג'מן (עקיבא תורג'מן וצורית תורג'מן/עקיבא תורג'מן)
"חצי בשבילי" – איתי לוי (אבי אוחיון/אבי אוחיון ומתן דרור)
"בחלומות שלנו" – דודו אהרון ועדן מאירי (דודו אהרון, דולב רם ופן חזות)
"כתר מלוכה" – ישי ריבו (ישי ריבו)
"דיבור נגוע" – יהונתן מרגי וסטפן לגר (סטפן לגר, יהונתן מרגי, רון ביטון ויונתן גולדשטיין)
"מה עבר עליי" – עדן חסון (אבי אוחיון ונתן גושן)
"איפה את" – אליעד נחום (מורן דוד ואבישי רם)
"אני רוצה" – עידן עמדי (עידן עמדי)
"תל אביב זה אני ואת" – אמיר ובן וג'יין בורדו (אמיר שדה, בן מאור ודורון טלמון)
"קחי את הפחדים" – בניה ברבי (בניה ברבי)
"סדר העבודה" – ישי ריבו (ישי ריבו)
"עוד יום" – פול טראנק (גיל ניסמן/גיל ניסמן ואריאל קשת)
"במקום הכי רחוק" – בניה ברבי (בניה ברבי ואבי אוחיון)
"חזרי אלי" – נתן גושן (נתן גושן)
"לקחת את המפתחות" – איתי לוי (דולב רם ופן חזות)
"מסיבה" – יסמין מועלם עם שקל (יסמין מועלם ואייל דוידי)
"מים שקופים" – עומר אדם (אבי אוחיון/אבי אוחיון ומתן דרור)"""
}

SELF_CORRELATION_SONGS = [
    "ג'ירפות - יש לי חור בלב בצורה שלך",
    "השמחות - יהודה יהודה",
    "מרסדס בנד - תגידי לי את",
    "קובי פרץ - בלבלי אותו",
    "עוזי חיטמן - אני תמיד נשאר אני",
    "נוער שוליים - ציירי לך שפם",
    "עממי - אחד מי יודע",
    "עממי - שרה שרה שיר שמח",
    "עממי - דיינו",
    "עממי - חד גדיא",
    "עממי - יש לי שיר שמעצבן אנשים",
    "עממי - לדוד משה הייתה חווה",
    "עידן רייכל - ואם תבואי אליי",
    "הכל עובר חביבי - הלילה",
    "כוורת - סוכר בתה",
    "נועה קירל - אם אתה גבר",
    "שוקולד מנטה מסטיק - אמור שלום",
    "אריק איינשטיין - אוהב להיות בבית",
    "הקומדי סטור - אינקובטור",
    "משה פרץ - מהשמיים",
    "שלומי שבן - אריק",
    "שוטי הנבואה - הילדים קופצים",
]


def parse_wiki_string(wiki_str):
    parsed_results = []
    lines = wiki_str.split('\n')
    for idx, line in enumerate(lines):
        if line.count('"') != 2:
            continue
        rank = idx + 1
        _, song_name, creators = line.split('"')
        song_name = song_name.replace('-', '').strip()
        if '(' in creators:
            creators = creators.split('(')[0]
        artist_name = creators.replace('–', '').strip()
        parsed_results.append(SongId(artist_name=artist_name, song_name=song_name))
    return parsed_results


def song_chart_for_year(year: int):
    # return parse_wiki_string(year_to_wiki_str[year])
    if year == 2020:
        return parse_wiki_string(year_to_wiki_str[year])
    return read_pizmonet_page(PIZMONET_PAGES[year - 1969])


def read_pizmonet_page(url):
    # We import here just as a hack to avoid a dependency
    import bs4
    import requests
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    parsed_results = []
    r = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"},
                     verify=False)
    bs = bs4.BeautifulSoup(r.content, "html.parser")
    tables = bs.find_all("table")
    found_table = None
    for table in tables:
        columns = table.find_all("th")
        if len(columns) == 6 and columns[0].text.strip() == "מיקום":
            found_table = table
            break
    assert found_table
    for r in found_table.find_all("tr")[1:]:
        index, song_name, artist_name, writer, composer, producer = [td.text.strip() for td in r.find_all("td")]
        parsed_results.append(SongId(song_name=song_name, artist_name=artist_name))

    return parsed_results


def main():
    # print(read_pizmonet_page(PIZMONET_PAGES[-1]))
    for year in year_to_wiki_str.keys():
        print(year)
        print(song_chart_for_year(year))


if __name__ == "__main__":
    main()
