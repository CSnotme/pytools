import requests
import csv
import time


def main():
    edit_data = read_csv()
    class_id_list = list(edit_data.keys())

    try:
        class_map = getClassList(class_id_list)
    except Exception as e:
        print("获取班级信息异常, err:".format(e))
        print("程序退出")
        exit(1)

    total = len(edit_data)
    no_class_info = []
    err_res = []
    finish = 0
    for class_id, class_name in edit_data.items():
        class_info = class_map.get(class_id, [])
        if not class_info:
            edit_res = "未找到班级{}的信息".format(class_id)
            no_class_info.append(edit_res)
        else:
            data = {
                'course_id': class_info['course_id'],
                'class_id': class_id,
                'class_name': class_name,
                'counselor_id': class_info['counselor_id'],
                'class_quota': class_info['class_quota'],
                'is_recommend': class_info['is_recommend'],
                'reason': '变更班级名称',
                'brand': '100',
            }

            try:
                # edit_res = ""
                edit_res = editClass(data)
            except Exception as e:
                edit_res = "更新班级名称异常, 班级id:{}, err:{}".format(class_id, e)
                err_res.append(edit_res)

        finish += 1

        time.sleep(0.01)

        print("{}, 进度：{}/{}".format(edit_res, finish, total))

    # 无班级信息的
    for i in no_class_info:
        print(i)

    # 执行异常的
    for j in err_res:
        print(j)

def getClassList(class_id_list=[]):
    cookies = {
        'MKC-ExternalAccessToken-3': 'eyJhcHBpZCI6IjIzNSIsInRva2VuIjoiMGE4MTNiZGNhOWMxN2U2MzcxNDBmMmFjYjQ5NzA0MTAifQ==',
        'MKC-ExternalAccessToken': 'eyJhcHBpZCI6IjIzNSIsInRva2VuIjoiMGE4MTNiZGNhOWMxN2U2MzcxNDBmMmFjYjQ5NzA0MTAifQ==',
        'xes_rfh': 'cdS79ATKQs-UVlASAGJJBiKWJza2mg4SHXZMtgRbIL_4LtirvLXQWAawzl7Pc0eUTWGOQnPz5VD29rW95LilECEOLOcmzcrhYNrDKLcS7EB4JsEflGPBzrJcl7v7sreUZFa3mAtslRVN47M7AHgtuv6rOQ-zDDrs2bIN3BQEepU.cv0',
        'is_login': '1',
        'stu_id': '2442509',
        'stu_name': '2442509',
        'userGrade': '13',
        'tfstk': 'fCk-GeaUqnIRNQdnF0OmTvvcEptDiYnzM4o1Ky4lOq3x4chuO9clRJ3x7WMuE00YAqitE2mS-2QKrq0LT3z3Ry3nAbxDIdmr4JyIJFvMI4ZANP38AWwBArZaVgH6wsmr4JSVxxym405LFU2ByJgQh-ZuAJZQP26fhrrUAaZCFnnbukwCPW6QhmZQvuG_FdUCfrXK36t1T7OPUTWrHoTTv0UT0rkY27FgGrBQ2xE8wPiSUTu3SkhsB7u6o_4S6fuTj4vfeVnSyfNsFZTYLmctJlHWf1UKzmMuGYth_oyENfwSpFQSc43rUfiWosExG0DYiATOp7ljzfPKKEvaEfmiL5MWeNz0_k3TFjLfeVsPNAD9jpQg0-CWDnCFT7Zm18Bo1_49KKqYSn8FT6PJYoUMDnCFT7Z4DPx2865UwH5..',
        'stu_area_id': '100',
        'isVisitFirst': '1',
        'currentGrade': '11',
        'tal-passport-run-heartbeat-timeStamp': '1712043224677',
        'tal_token': 'tal173EI_xCtR03R5HSbaJmjvSft_sN8ixPAnXwZBjPz6bTlTtLjpNC7dWcJMZlxDc57VUhPp2YdRA1pLYu6Q9_OVzh6zaGLl-NQB1VjfCpl8cGwjX9z_Iwc1P8ruQhj_37QVF5PII_P3SHF-ZsN4KeYFumL2oIPfEqJbpy9YyzUa-ZPkmkCIpm9xq3MAbqcLYQWI9zDQFJfz5yfZaGPIZ8gUZr4wRdnMtqq4PHUEN7ZcJwrtO4v9y2yGuF2tFiBazWkf6OkWJnZLWwJVgin--AxGkyn58TWL-KrV1KV9UiHVYTEo98',
        'xesId': '14d48b969eb9bd320bf8b4fb1cd2818b',
        'prelogid': 'c3762afd6e8a3178c38010da2c3a9593',
        'wx': '6e05a6698b5062f9626b2467b2fcc5d1qbsmmmyb',
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': 'MKC-ExternalAccessToken-3=eyJhcHBpZCI6IjIzNSIsInRva2VuIjoiMGE4MTNiZGNhOWMxN2U2MzcxNDBmMmFjYjQ5NzA0MTAifQ==; MKC-ExternalAccessToken=eyJhcHBpZCI6IjIzNSIsInRva2VuIjoiMGE4MTNiZGNhOWMxN2U2MzcxNDBmMmFjYjQ5NzA0MTAifQ==; xes_rfh=cdS79ATKQs-UVlASAGJJBiKWJza2mg4SHXZMtgRbIL_4LtirvLXQWAawzl7Pc0eUTWGOQnPz5VD29rW95LilECEOLOcmzcrhYNrDKLcS7EB4JsEflGPBzrJcl7v7sreUZFa3mAtslRVN47M7AHgtuv6rOQ-zDDrs2bIN3BQEepU.cv0; is_login=1; stu_id=2442509; stu_name=2442509; userGrade=13; tfstk=fCk-GeaUqnIRNQdnF0OmTvvcEptDiYnzM4o1Ky4lOq3x4chuO9clRJ3x7WMuE00YAqitE2mS-2QKrq0LT3z3Ry3nAbxDIdmr4JyIJFvMI4ZANP38AWwBArZaVgH6wsmr4JSVxxym405LFU2ByJgQh-ZuAJZQP26fhrrUAaZCFnnbukwCPW6QhmZQvuG_FdUCfrXK36t1T7OPUTWrHoTTv0UT0rkY27FgGrBQ2xE8wPiSUTu3SkhsB7u6o_4S6fuTj4vfeVnSyfNsFZTYLmctJlHWf1UKzmMuGYth_oyENfwSpFQSc43rUfiWosExG0DYiATOp7ljzfPKKEvaEfmiL5MWeNz0_k3TFjLfeVsPNAD9jpQg0-CWDnCFT7Zm18Bo1_49KKqYSn8FT6PJYoUMDnCFT7Z4DPx2865UwH5..; stu_area_id=100; isVisitFirst=1; currentGrade=11; tal-passport-run-heartbeat-timeStamp=1712043224677; tal_token=tal173EI_xCtR03R5HSbaJmjvSft_sN8ixPAnXwZBjPz6bTlTtLjpNC7dWcJMZlxDc57VUhPp2YdRA1pLYu6Q9_OVzh6zaGLl-NQB1VjfCpl8cGwjX9z_Iwc1P8ruQhj_37QVF5PII_P3SHF-ZsN4KeYFumL2oIPfEqJbpy9YyzUa-ZPkmkCIpm9xq3MAbqcLYQWI9zDQFJfz5yfZaGPIZ8gUZr4wRdnMtqq4PHUEN7ZcJwrtO4v9y2yGuF2tFiBazWkf6OkWJnZLWwJVgin--AxGkyn58TWL-KrV1KV9UiHVYTEo98; xesId=14d48b969eb9bd320bf8b4fb1cd2818b; prelogid=c3762afd6e8a3178c38010da2c3a9593; wx=6e05a6698b5062f9626b2467b2fcc5d1qbsmmmyb',
        'origin': 'https://scm.inner.xiwang.com',
        'priority': 'u=1, i',
        'referer': 'https://scm.inner.xiwang.com/',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'token': 'a7a91b1c90f8fe44b7d05168d64dc1af',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'x-brand': '100',
    }

    class_id_list = [str(i) for i in class_id_list]


    class_map = dict()

    ids_list = array_chunk(class_id_list, 50)

    for ids in ids_list:
        page = 1
        limit = 50
        ids_str = ",".join(ids)
        while True:
            data = {
                'page': page,
                'limit': limit,
                'status': '1',
                'class_ids': ids_str,
                'brand': '100',
            }

            response = requests.post(
                'https://erpadmin.inner.xiwang.com/delegation/ClassAdmin/liveclass/liveclass/list',
                cookies=cookies,
                headers=headers,
                data=data,
                timeout=2,
            )
            res = response.json()
            response.close()
            if not res or res.get('stat') != 1 or res.get('msg') != 'succ':
                raise Exception("班级数据获取失败")

            if not res.get('data') or not res['data']['list']:
                # print("没数据了")
                break

            print("批次查询班级数据：{}条".format(len(res['data']['list'])))
            for class_info in res['data']['list']:
                class_map[str(class_info['class_id'])] = class_info

            page += 1

            time.sleep(0.1)

    print("班级总数：", len(class_map))
    return class_map


def editClass(data):
    cookies = {
        'MKC-ExternalAccessToken-3': 'eyJhcHBpZCI6IjIzNSIsInRva2VuIjoiMGE4MTNiZGNhOWMxN2U2MzcxNDBmMmFjYjQ5NzA0MTAifQ==',
        'MKC-ExternalAccessToken': 'eyJhcHBpZCI6IjIzNSIsInRva2VuIjoiMGE4MTNiZGNhOWMxN2U2MzcxNDBmMmFjYjQ5NzA0MTAifQ==',
        'xes_rfh': 'cdS79ATKQs-UVlASAGJJBiKWJza2mg4SHXZMtgRbIL_4LtirvLXQWAawzl7Pc0eUTWGOQnPz5VD29rW95LilECEOLOcmzcrhYNrDKLcS7EB4JsEflGPBzrJcl7v7sreUZFa3mAtslRVN47M7AHgtuv6rOQ-zDDrs2bIN3BQEepU.cv0',
        'is_login': '1',
        'stu_id': '2442509',
        'stu_name': '2442509',
        'userGrade': '13',
        'tfstk': 'fCk-GeaUqnIRNQdnF0OmTvvcEptDiYnzM4o1Ky4lOq3x4chuO9clRJ3x7WMuE00YAqitE2mS-2QKrq0LT3z3Ry3nAbxDIdmr4JyIJFvMI4ZANP38AWwBArZaVgH6wsmr4JSVxxym405LFU2ByJgQh-ZuAJZQP26fhrrUAaZCFnnbukwCPW6QhmZQvuG_FdUCfrXK36t1T7OPUTWrHoTTv0UT0rkY27FgGrBQ2xE8wPiSUTu3SkhsB7u6o_4S6fuTj4vfeVnSyfNsFZTYLmctJlHWf1UKzmMuGYth_oyENfwSpFQSc43rUfiWosExG0DYiATOp7ljzfPKKEvaEfmiL5MWeNz0_k3TFjLfeVsPNAD9jpQg0-CWDnCFT7Zm18Bo1_49KKqYSn8FT6PJYoUMDnCFT7Z4DPx2865UwH5..',
        'stu_area_id': '100',
        'isVisitFirst': '1',
        'currentGrade': '11',
        'tal-passport-run-heartbeat-timeStamp': '1712043224677',
        'tal_token': 'tal173EI_xCtR03R5HSbaJmjvSft_sN8ixPAnXwZBjPz6bTlTtLjpNC7dWcJMZlxDc57VUhPp2YdRA1pLYu6Q9_OVzh6zaGLl-NQB1VjfCpl8cGwjX9z_Iwc1P8ruQhj_37QVF5PII_P3SHF-ZsN4KeYFumL2oIPfEqJbpy9YyzUa-ZPkmkCIpm9xq3MAbqcLYQWI9zDQFJfz5yfZaGPIZ8gUZr4wRdnMtqq4PHUEN7ZcJwrtO4v9y2yGuF2tFiBazWkf6OkWJnZLWwJVgin--AxGkyn58TWL-KrV1KV9UiHVYTEo98',
        'xesId': '14d48b969eb9bd320bf8b4fb1cd2818b',
        'prelogid': 'c3762afd6e8a3178c38010da2c3a9593',
        'wx': '6e05a6698b5062f9626b2467b2fcc5d1qbsmmmyb',
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': 'MKC-ExternalAccessToken-3=eyJhcHBpZCI6IjIzNSIsInRva2VuIjoiMGE4MTNiZGNhOWMxN2U2MzcxNDBmMmFjYjQ5NzA0MTAifQ==; MKC-ExternalAccessToken=eyJhcHBpZCI6IjIzNSIsInRva2VuIjoiMGE4MTNiZGNhOWMxN2U2MzcxNDBmMmFjYjQ5NzA0MTAifQ==; xes_rfh=cdS79ATKQs-UVlASAGJJBiKWJza2mg4SHXZMtgRbIL_4LtirvLXQWAawzl7Pc0eUTWGOQnPz5VD29rW95LilECEOLOcmzcrhYNrDKLcS7EB4JsEflGPBzrJcl7v7sreUZFa3mAtslRVN47M7AHgtuv6rOQ-zDDrs2bIN3BQEepU.cv0; is_login=1; stu_id=2442509; stu_name=2442509; userGrade=13; tfstk=fCk-GeaUqnIRNQdnF0OmTvvcEptDiYnzM4o1Ky4lOq3x4chuO9clRJ3x7WMuE00YAqitE2mS-2QKrq0LT3z3Ry3nAbxDIdmr4JyIJFvMI4ZANP38AWwBArZaVgH6wsmr4JSVxxym405LFU2ByJgQh-ZuAJZQP26fhrrUAaZCFnnbukwCPW6QhmZQvuG_FdUCfrXK36t1T7OPUTWrHoTTv0UT0rkY27FgGrBQ2xE8wPiSUTu3SkhsB7u6o_4S6fuTj4vfeVnSyfNsFZTYLmctJlHWf1UKzmMuGYth_oyENfwSpFQSc43rUfiWosExG0DYiATOp7ljzfPKKEvaEfmiL5MWeNz0_k3TFjLfeVsPNAD9jpQg0-CWDnCFT7Zm18Bo1_49KKqYSn8FT6PJYoUMDnCFT7Z4DPx2865UwH5..; stu_area_id=100; isVisitFirst=1; currentGrade=11; tal-passport-run-heartbeat-timeStamp=1712043224677; tal_token=tal173EI_xCtR03R5HSbaJmjvSft_sN8ixPAnXwZBjPz6bTlTtLjpNC7dWcJMZlxDc57VUhPp2YdRA1pLYu6Q9_OVzh6zaGLl-NQB1VjfCpl8cGwjX9z_Iwc1P8ruQhj_37QVF5PII_P3SHF-ZsN4KeYFumL2oIPfEqJbpy9YyzUa-ZPkmkCIpm9xq3MAbqcLYQWI9zDQFJfz5yfZaGPIZ8gUZr4wRdnMtqq4PHUEN7ZcJwrtO4v9y2yGuF2tFiBazWkf6OkWJnZLWwJVgin--AxGkyn58TWL-KrV1KV9UiHVYTEo98; xesId=14d48b969eb9bd320bf8b4fb1cd2818b; prelogid=c3762afd6e8a3178c38010da2c3a9593; wx=6e05a6698b5062f9626b2467b2fcc5d1qbsmmmyb',
        'origin': 'https://scm.inner.xiwang.com',
        'priority': 'u=1, i',
        'referer': 'https://scm.inner.xiwang.com/',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'token': 'a7a91b1c90f8fe44b7d05168d64dc1af',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'x-brand': '100',
    }

    response = requests.post(
        'https://erpadmin.inner.xiwang.com/delegation/ClassAdmin/liveclass/liveclass/edit',
        cookies=cookies,
        headers=headers,
        data=data,
        timeout=2,
    )

    res = response.json()
    response.close()
    return res

def read_csv():
    # file_path = "../update_class_name_curl/初中班级名称修改-2024-09-26.csv"
    file_path = "../update_class_name_curl/小学秋下班级名称修改(1)-2024.09-26.csv"

    id_name_mapping = dict()

    with open(file_path, newline='') as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            class_id = row['班级ID']
            class_name = row['修改后的班级名']
            id_name_mapping[str(class_id)] = class_name

    return id_name_mapping


def array_chunk(input_array, chunk_size, preserve_keys=False):
    if chunk_size < 1:
        return []

    chunks = []

    for i in range(0, len(input_array), chunk_size):
        # Get the chunk
        chunk = input_array[i:i + chunk_size]

        # If preserve_keys is True, retain the original keys
        if preserve_keys:
            chunk = {k: input_array[k] for k in range(i, min(i + chunk_size, len(input_array)))}

        # Append the chunk to the list of chunks
        chunks.append(chunk)

    return chunks


if __name__ == '__main__':
    # pass
    main()