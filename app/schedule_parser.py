import pprint
import requests

base_url = 'https://ecampus.ncfu.ru'

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "ru-RU,ru;q=0.9,en-RU;q=0.8,en;q=0.7,en-US;q=0.6",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Host": "ecampus.ncfu.ru",
    "Origin": "https://ecampus.ncfu.ru",
    # "Referer": "https://ecampus.ncfu.ru/schedule/group/15033",
    "Sec-Ch-Ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 "
                  "Safari/537.36",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
}


def get_group_schedule(group_id: int, date: str):
    url = base_url + "/schedule/GetSchedule"
    data = {'date': date + "T00:00:00.000Z", 'Id': group_id, 'targetType': 2}
    response = requests.post(url, headers=headers, json=data)
    return response.json()


def get_group_id(group_name: str) -> int:
    url = base_url + f"/schedule/search"
    params = {
        "q": group_name
    }
    response = requests.get(url, headers=headers, params=params)
    if response.history:
        return int(response.url.split("/")[-1])
    return 0


def format_schedule_for_day(day_data):
    date = day_data['Date']
    weekday = day_data['WeekDay']
    lessons = day_data['Lessons']

    response = f"{weekday}, {date}:"

    for lesson in lessons:
        response += f"""\n
{lesson['PairNumberStart']} {lesson['LessonName']}
Дисциплина: {lesson['Discipline']}
Аудитория: {lesson['Aud']['Name']}
Тип занятия: {lesson['LessonType']}
Подгруппа: {lesson['Groups'][0]['Subgroup']}
Преподаватель: {lesson['Teacher']['Name']}
Время: с {lesson['TimeBegin']} до {lesson['TimeEnd']}"""

    return response


group = "кмб-с-о-19-1"
date = "2024-04-08"
# print(id := get_group_id(group))
# print(schedule := get_group_schedule(id, date))
# print(format_schedule_for_day(schedule[0]))

