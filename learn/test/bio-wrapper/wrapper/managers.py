# Copyright 2016 - Nguyen Quang "TechBK" Binh.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import swiftclient
import swiftclient.exceptions
import asyncio
import config


# from swiftclient.exceptions import ClientException


class SwiftManager(object):
    def __init__(self, user, key, tenant, container_name, file_name, out_file_name,
                 authurl='http://192.168.145.132:5000/v2.0'):
        """
        if not `container_name` check out whether container exist? if no Exception, not to create container.
        else check out whether container exist?
        :param str user:
        :param str key:
        :param tenant:
        :param container_name:
        :param file_name:
        :param out_file_name:
        :param authurl:
        :return:
        """
        self.conn = swiftclient.client.Connection(
                user=user,
                tenant_name=tenant,
                auth_version='2.0',
                key=key,
                authurl=authurl
        )

        self.file_name = file_name

        self.out_file_name = out_file_name

        if not container_name:
            self.container_name = config.INSTANCE_NAME
            # check out whether container exist? if no Exception, not to create container.
            try:
                self.conn.head_container(self.container_name)
            except swiftclient.exceptions.ClientException:
                self.conn.put_container(self.container_name)
        else:
            self.container_name = container_name
            # check out whether container exist?
            self.conn.head_container(self.container_name)

    @asyncio.coroutine
    def get_data(self):
        """
        Lay data tu swift, luu vao thu muc data/
        :return: string: tra ve duong dan toi file data thu dc
        """
        obj_tuple = self.conn.get_object(self.container_name, self.file_name)
        return obj_tuple.decode('utf-8')

    @asyncio.coroutine
    def put_data(self, out):
        """
        Lay du ket qua co duoc gui len swift
        :param out:
        :return: tra ve
        """
        return self.conn.put_object(self.container_name, self.out_file_name,
                                    contents=out,
                                    content_type='text/plain')


class Job(object):
    def __init__(self, swift, is_first):
        """

        :param swift:
        :param is_first: If True, the job is first, va nguoc lai :v
        :return:
        """
        self.first = is_first
        # self.is_first(is_first)
        self.swift = swift
        self.error = False
        self.process = asyncio.async(self.run_process())

    def is_first(self, is_first):
        """
        Check first.
        Khong ro co can ham nay ko nua :v
        if is_first: Error, because job need get_data.
        :param bool is_first:
        :return:
        :raises Exception: First :v
        """

        # if not is_first:
        #     self.error = True
        #     raise Exception("Job have to be first")
        if is_first:
            self.error = True
            raise Exception("Job have to be not first")

    @asyncio.coroutine
    def run_process(self):
        """

        :return:
        :raise Exception: set self.error = True
        """
        try:
            if not self.first:
                dictionary = yield from self.swift.get_data()
                commandline = u"ls -l %s" % dictionary
            else:
                commandline = u"ls -l"
            # Create the subprocess, redirect the standard output into a pipe
            create = asyncio.create_subprocess_shell(cmd=commandline,
                                                     stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            # Wait for create
            proc = yield from create  # proc is Process Instance

            out, err = yield from proc.communicate()
            if err:
                self.error = True
            yield from self.swift.put_data(out)
            return out, err
        except Exception as e:
            self.error = True
            raise e

    def __str__(self):
        return "Job Object"
