import requests
import time


def main():
    course_single_class_num_map = {
        2007733: 6,
        2007735: 6,
    }

    total = len(course_single_class_num_map)
    print("开始更新课程单人开班数, 课程数量总计:{}".format(total))

    err_list = []
    finish = 0
    for course_id, single_class_num in course_single_class_num_map.items():
        finish += 1
        try:
            # 获取数据
            course_info = getCourseInfo(course_id).get('course_info', [])
            if len(course_info) == 0:
                raise Exception("获取course_info信息为空")
            # msg = "获取课程信息:{}成功, 当前进度:{}/{}".format(course_id, finish, total)

            # 更新数据
            editCourseServiceInfo(formatEditData(course_info, single_class_num))
            msg = "更新课程:{} 单人开班数:{}成功, 当前进度:{}/{}".format(course_id, single_class_num, finish, total)
        except Exception as e:
            msg = "更新课程:{} 单人开班数:{}异常, 当前进度:{}/{}, err:".format(course_id, single_class_num, finish, total, e)
            err_list.append([course_id, single_class_num, e.__str__()])

        print(msg)

        time.sleep(0.1)

    if len(err_list) > 0:
        print("更新课程单人开班数，异常数据：")
        for i in err_list:
            print("课程id:{}, 单人开班数:{}, 异常信息:{}".format(i[0], i[1], i[2]))


def formatEditData(info, single_class_num):
    course_service_data = {
        'have_goods': info['have_goods'],
        'course_quota': info['course_quota'],
        'class_type': info['class_type'],
        'course_class_limit': info['course_class_limit'],
        'single_class_num': single_class_num,
        'is_counselor_change_class': info['is_counselor_change_class'],
        'rate1': '',
        'rate2': '',
        'rate3': '',
        'id': info['course_id'],
        'brand': '100',
    }

    return course_service_data


# 获取课程信息
def getCourseInfo(course_id):
    cookies, headers = getHeaderAndCookies()

    params = {
        'course_id': course_id,
        'brand': '100',
    }

    response = requests.get(
        'https://erpadmin.inner.xiwang.com/supply/course/courseInfo',
        params=params,
        cookies=cookies,
        headers=headers,
    )

    res = response.json()
    response.close()
    if not res or res.get('stat') != 1 or res.get('msg') != 'succ':
        raise Exception("课程:{}数据获取失败".format(course_id))

    return res['data']


# 编辑课程服务信息
def editCourseServiceInfo(data):
    cookies, headers = getHeaderAndCookies()

    response = requests.post(
        'https://erpadmin.inner.xiwang.com/supply/course/editServiceInfo',
        cookies=cookies,
        headers=headers,
        data=data,
    )

    res = response.json()
    response.close()
    if not res or res.get('stat') != 1 or res.get('msg') != 'success':
        raise Exception("课程:{}服务信息数据更新失败, resp:{}".format(data['id'], res))


def getHeaderAndCookies():
    cookies = {
        'MKC-ExternalAccessToken-3': 'eyJhcHBpZCI6IjIzNSIsInRva2VuIjoiMGE4MTNiZGNhOWMxN2U2MzcxNDBmMmFjYjQ5NzA0MTAifQ==',
        'MKC-ExternalAccessToken': 'eyJhcHBpZCI6IjIzNSIsInRva2VuIjoiMGE4MTNiZGNhOWMxN2U2MzcxNDBmMmFjYjQ5NzA0MTAifQ==',
        'xes_rfh': 'cdS79ATKQs-UVlASAGJJBiKWJza2mg4SHXZMtgRbIL_4LtirvLXQWAawzl7Pc0eUTWGOQnPz5VD29rW95LilECEOLOcmzcrhYNrDKLcS7EB4JsEflGPBzrJcl7v7sreUZFa3mAtslRVN47M7AHgtuv6rOQ-zDDrs2bIN3BQEepU.cv0',
        'is_login': '1',
        'stu_id': '2442509',
        'stu_name': '2442509',
        'userGrade': '13',
        'stu_area_id': '100',
        'isVisitFirst': '1',
        'currentGrade': '11',
        'tal-passport-run-heartbeat-timeStamp': '1712043224677',
        'xesId': '14d48b969eb9bd320bf8b4fb1cd2818b',
        'tal_token': 'tal173UPjCVTjLaxDBl6-xQ6xDLBfnabFxL03cG8ZSLRJWJGGsGhc-U4WzoAE6J045zE40b6l7C9QUfA8mLnPbuZ1LNx3nG-xSVf8MeLrakGcmrAvJx1rT5KtcR7ZK-ae4t3Y5qQjUvx8SR9FGxo-9NvQ6h4e2iTTmz17FRttW8Me0e1omkCIpm9xq3MAbqcLYQWI9zDQFJfz5yfZaGPIZ8gUZr4wRdnMtqq4PHUEN7ZcJwrtO4v9y2yGuF2tFiBazWkf6OkWJnZLWwJVgin--AxGkyn58TWL-KrV1KV9UiHVYTEo98',
        'prelogid': '30ab3959fb193a525ce663ade3ca47b7',
        'wx': '0e55ab7a1d34e618896e620298f08fda9xqs09yy9f',
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': 'MKC-ExternalAccessToken-3=eyJhcHBpZCI6IjIzNSIsInRva2VuIjoiMGE4MTNiZGNhOWMxN2U2MzcxNDBmMmFjYjQ5NzA0MTAifQ==; MKC-ExternalAccessToken=eyJhcHBpZCI6IjIzNSIsInRva2VuIjoiMGE4MTNiZGNhOWMxN2U2MzcxNDBmMmFjYjQ5NzA0MTAifQ==; xes_rfh=cdS79ATKQs-UVlASAGJJBiKWJza2mg4SHXZMtgRbIL_4LtirvLXQWAawzl7Pc0eUTWGOQnPz5VD29rW95LilECEOLOcmzcrhYNrDKLcS7EB4JsEflGPBzrJcl7v7sreUZFa3mAtslRVN47M7AHgtuv6rOQ-zDDrs2bIN3BQEepU.cv0; is_login=1; stu_id=2442509; stu_name=2442509; userGrade=13; stu_area_id=100; isVisitFirst=1; currentGrade=11; tal-passport-run-heartbeat-timeStamp=1712043224677; xesId=14d48b969eb9bd320bf8b4fb1cd2818b; tal_token=tal173UPjCVTjLaxDBl6-xQ6xDLBfnabFxL03cG8ZSLRJWJGGsGhc-U4WzoAE6J045zE40b6l7C9QUfA8mLnPbuZ1LNx3nG-xSVf8MeLrakGcmrAvJx1rT5KtcR7ZK-ae4t3Y5qQjUvx8SR9FGxo-9NvQ6h4e2iTTmz17FRttW8Me0e1omkCIpm9xq3MAbqcLYQWI9zDQFJfz5yfZaGPIZ8gUZr4wRdnMtqq4PHUEN7ZcJwrtO4v9y2yGuF2tFiBazWkf6OkWJnZLWwJVgin--AxGkyn58TWL-KrV1KV9UiHVYTEo98; prelogid=30ab3959fb193a525ce663ade3ca47b7; wx=0e55ab7a1d34e618896e620298f08fda9xqs09yy9f',
        'origin': 'https://scm.inner.xiwang.com',
        'priority': 'u=1, i',
        'referer': 'https://scm.inner.xiwang.com/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'token': 'd13e6406c07d4c875728cd170cf0b500',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'x-brand': '100',
        'x-check-data-tag': 'true',
    }

    return cookies, headers


if __name__ == '__main__':
    pass

    # todo 换cookies， 测试是否能请求成功
    # main()
