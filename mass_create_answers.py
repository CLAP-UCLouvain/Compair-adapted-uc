import datetime
import os
import time
import uuid

import requests

directory_path = "./Texts"
file_name_list = []


def submitAnswer(apiUrl, courseId, assignmentId, cookies, content, userId, file_name):
    global file_name_list
    answerUrl = f'{apiUrl}/courses/{courseId}/assignments/{assignmentId}/answers'
    timeNow = datetime.datetime.utcnow()
    oneSecond = datetime.timedelta(seconds=1)
    answer_uuid = str(uuid.uuid4())
    file_name_list.append({answer_uuid: file_name})
    answer = {
        'assignment_id': assignmentId,
        'attempt_duration': 'PT1.000S',
        'attempt_started': (timeNow - oneSecond).isoformat() + 'Z',
        'attempt_ended': timeNow.isoformat() + 'Z',
        'attempt_uuid': answer_uuid,
        'comparable': True,
        'content': f'<p>{content}</p>',
        'course_id': courseId,
        'draft': False,
        'existingFile': False,
        'rotated': False,
        'user_id': userId
    }
    req = requests.post(answerUrl, cookies=cookies, json=answer)
    try:
        req.raise_for_status()
    except requests.HTTPError as err:
        print("ERROR - Failed to submit answer:")
        print(req.text)
        raise err

    return req.json()


def read_and_send_data():
    global file_name_list
    session_str = ".eJxNjrtOBDEMRX8FpQZkO7GTTLeiokOIimaUh8Oulp2RZrIV4t_JahskN773XOn8mLltuh_N1LerPpr5VM1ksthknSi24EupTcCzMLsRAdWmXCS7alOpEUBrGA1x9qCxiQ1JKKAXiwMQxzG1zJGx1caAjMAlRHSp2UqKGRsmVesVq1WLWmONZohcd93uNjje7_XrtMwX7cf1Fr2sl7fD6_vDoZT1uvQB7Lrvp3W5LwSolJJjkmpdYK-aUoVAVhw4Cu4f39ezLmMSkPyQbz5EYqEGw9aSk1yVgCnfJj1tfU590ARkn-B2H8gT4MT-OSJ-mt8_Vz9gBA.ZAIL5Q.2THQy7J8fBbCp687aEAm2_3GRcs"
    api_url = "http://py-proficiency-project.sipr.ucl.ac.be/api"
    course_id = "HBmMDSLMQL6dfuw-I6HnJQ"
    assignment_id = "yT2Smm6cTneJESjYu7y-Wg"
    user_id = "wyJhv254S5Cio3Um8BO--g"
    cookies = {'session': session_str}
    for filename in os.listdir(directory_path):
        file_name_only = os.path.splitext(filename)[0]
        file_path = os.path.join(directory_path, filename)
        with open(file_path, "r", encoding='utf8') as f:
            content = f.read()
            submitAnswer(apiUrl=api_url, courseId=course_id, assignmentId=assignment_id, cookies=cookies,
                         content=content, userId=user_id, file_name=file_name_only)
            time.sleep(0.5)
            print(f'Text {file_name_only} uploaded...')
    print("All file are uploaded creating a .txt file for uploading using phpMyAdmin...")
    with open("update_file_name.txt", "a+", encoding="utf8") as f:
        for file_names in file_name_list:
            for key, values in file_names.items():
                f.write(f'UPDATE answer SET file_name = {str(values)} where attempt_uuid = "{str(key)}";\n')


read_and_send_data()
