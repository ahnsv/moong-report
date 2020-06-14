import json
import os
from datetime import timedelta, datetime

from dateutil.parser import parse
from requests import post

MOONG_SLACK_WEBHOOK = os.getenv("SLACK_WEB_HOOK", None)
headers = {
    'Content-Type': 'application/json'
}


# TODO: AWS CDK로 인프라를 관리한다
def report(event, context):
    """

    :param event:
        timestamp: isodate로 현재 시간을 알려주세요
        pride_index: 정시 퇴근 자신감 지표
        smoothness_index: 맨들 지수
    :param context:
    :return:
    """

    if (event['timestamp'] is None) \
            or (event['pride_index'] is None) \
            or (event['smoothness_index'] is None):
        print("필수 입력 정보가 누락되었습니다")
        return

    now = parse(event['timestamp'])
    now_formatted = now.strftime("%Y-%m-%d %H:%M:%S")
    exitable = now + timedelta(hours=9)
    exitable_formatted = exitable.strftime("%Y-%m-%d %H:%M:%S")

    payload = {
        "attachments": [
            {
                "color": "#36a64f",
                "title": "뭉망이의 출근 리포트",
                "text": "오늘의 뭉망이 출근 기록이에요\n",
                "fields": [
                    {
                        "title": "플래그원 도착 시간",
                        "value": f"{now_formatted}",
                        "short": True
                    },
                    {
                        "title": "퇴근 가능 시간",
                        "value": f"{exitable_formatted}",
                        "short": True
                    },
                    {
                        "title": "뭉망이 정시 퇴근 자신감 지표",
                        "value": f"{event['pride_index']}점 / 5점",
                        "short": True
                    },
                    {
                        "title": "뭉망이 맨들-니스",
                        "value": f"{event['smoothness_index']}점 / 5점",
                        "short": True
                    }
                ],
            }
        ]
    }
    response = post(url=MOONG_SLACK_WEBHOOK, headers=headers, data=json.dumps(payload))
    print(response.text.encode('utf8'))


if __name__ == '__main__':
    report({'timestamp': datetime.now().isoformat(), 'pride_index': 2, 'smoothness_index': 2}, None)
