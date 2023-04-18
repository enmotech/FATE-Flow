#
#  Copyright 2019 The FATE Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
from fate_flow.db.runtime_config import RuntimeConfig
from fate_flow.settings import API_VERSION
from fate_flow.utils.log_utils import getLogger
from fate_flow.utils import api_utils

LOGGER = getLogger()


class ControllerClient(object):
    @classmethod
    def update_job(cls, job_info):
        LOGGER.info("request update job {} on {} {}".format(job_info["job_id"], job_info["role"], job_info["party_id"]))
        response = api_utils.local_api(
            job_id=job_info["job_id"],
            method='POST',
            endpoint='/party/{}/{}/{}/update'.format(
                job_info["job_id"],
                job_info["role"],
                job_info["party_id"]
            ),
            json_body=job_info)
        return response

    @classmethod
    def report_task(cls, task_info):
        LOGGER.info("request update job {} task {} {} on {} {}".format(task_info["job_id"], task_info["task_id"],
                                                                       task_info["task_version"], task_info["role"],
                                                                       task_info["party_id"]))
        response = api_utils.local_api(
            job_id=task_info["job_id"],
            method='POST',
            endpoint='/party/{}/{}/{}/{}/{}/{}/report'.format(
                task_info["job_id"],
                task_info["component_name"],
                task_info["task_id"],
                task_info["task_version"],
                task_info["role"],
                task_info["party_id"]
            ),
            json_body=task_info)
        return response

    @classmethod
    def query_task(cls, task_info):
        import requests
        data = {
            "job_id": task_info["job_id"],
            "role": task_info["role"],
            "party_id": task_info["party_id"],
            "component_name": task_info["component_name"],
            "task_version": task_info["task_version"]
        }
        response = requests.post(
            url=f"http://{RuntimeConfig.JOB_SERVER_HOST}:{RuntimeConfig.HTTP_PORT}/{API_VERSION}/job/task/query",
            json=data
        )
        response_json = response.json().get("data", [])
        if not response_json:
            raise Exception(response.text)
        return response_json[0].get("f_party_status")
