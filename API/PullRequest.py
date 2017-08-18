import requests
from config.enviroment import *
from exception.exceptions import ExpectedStatusCodeError, ResourceNotFound
from faker import Faker
import random


class PullRequest(object):
    def __init__(self):
        self.session = git_hub()
        self.header = {'Authorization': 'token {}'.format(token)}

    def get_all_pull_requests(self, dto):
        """
        :param dto:
        :return:
        https://developer.github.com/v3/pulls/#list-pull-requests
        """
        return requests.get(url=self.session + '/repos/{owner}/{repo}/pulls'.format(
            owner=dto['owner'],
            repo=dto['repo']),
                            headers=self.header)

    def get_single_pull_request(self, dto):
        """
        :param dto:
        :return:
        https://developer.github.com/v3/pulls/#get-a-single-pull-request
        """
        return requests.get(url=self.session + '/repos/{owner}/{repo}/pulls/{number}'.format(
            owner=dto['owner'],
            repo=dto['repo'],
            number=dto['number']),
                            headers=self.header)

    def create_pull_request(self, dto, json):
        """
        :param dto:
        :return:
        https://developer.github.com/v3/pulls/#create-a-pull-request
        """
        return requests.post(url=self.session + '/repos/{owner}/{repo}/pulls'.format(
            owner=dto['owner'],
            repo=dto['repo']),
                             json=json,
                             headers=self.header)

    def update_pull_request(self, dto, json):
        """
        :param dto:
        :param json:
        :return:
        https://developer.github.com/v3/pulls/#update-a-pull-request
        """
        return requests.patch(url=self.session + '/repos/{owner}/{repo}/pulls/{number}'.format(
            owner=dto['owner'],
            repo=dto['repo'],
            number=dto['number']),
                              json=json,
                              headers=self.header)

    def get_pull_request_commits(self, dto):
        """
        :param dto:
        :return:
        https://developer.github.com/v3/pulls/#list-commits-on-a-pull-request
        """
        return requests.get(url=self.session + '/repos/{owner}/{repo}/pulls/{number}/commits'.format(
            owner=dto['owner'],
            repo=dto['repo'],
            number=dto['number']),
                            headers=self.header)

    def get_pull_request_files(self, dto):
        """
        :param dto:
        :return:
        https://developer.github.com/v3/pulls/#list-pull-requests-files
        """
        return requests.get(url=self.session + '/repos/{owner}/{repo}/pulls/{number}/files'.format(
            owner=dto['owner'],
            repo=dto['repo'],
            number=dto['number']),
                            headers=self.header)

    def get_pull_request_has_been_merged(self, dto):
        """
        :param dto:
        :return:
        https://developer.github.com/v3/pulls/#get-if-a-pull-request-has-been-merged
        """
        return requests.get(url=self.session + '/repos/{owner}/{repo}/pulls/{number}/merge'.format(
            owner=dto['owner'],
            repo=dto['repo'],
            number=dto['number']),
                            headers=self.header)

    def merge_pull_request(self, dto):
        """
        :param dto:
        :return:
        https://developer.github.com/v3/pulls/#merge-a-pull-request-merge-button
        """
        return requests.put(url=self.session + '/repos/{owner}/{repo}/pulls/{number}/merge'.format(
            owner=dto['owner'],
            repo=dto['repo'],
            number=dto['number']),
                            headers=self.header)

    def get_list_reviewed_requests(self, dto):
        """
        :param dto:
        :return:
        https://developer.github.com/v3/pulls/review_requests/#list-review-requests
        """
        return requests.get(url=self.session + '/repos/{owner}/{repo}/pulls/{number}/requested_reviewers'.format(
            owner=dto['owner'],
            repo=dto['repo'],
            number=dto['number']),
                            headers=self.header)

    def delete_pending_review(self, dto, number, id):
        """
        :return:
        https://developer.github.com/v3/pulls/reviews/#delete-a-pending-review
        """
        return requests.delete(url=self.session + '/repos/{owner}/{repo}/pulls/{number}/reviews/{id}'.format(
            owner=dto['owner'],
            repo=dto['repo'],
            number=number,
            id=id),
                               headers=self.header)

    def delete_reviewed_request(self, dto):
        """
        :param dto:
        :return:
        https://developer.github.com/v3/pulls/review_requests/#delete-a-review-request
        """
        return requests.delete(url=self.session + '/repos/{owner}/{repo}/pulls/{number}/requested_reviewers'.format(
            owner=dto['owner'],
            repo=dto['repo'],
            number=dto['number']),
                               headers=self.header)


class PullRequestAPI(object):
    def __init__(self):
        self.pull_request = PullRequest()

    def all_pull_request_dto(self):
        return {
            'owner': environment['test_data']['owner'],
            'repo': environment['test_data']['repo']['name']
        }

    def single_pull_request_dto(self, pull_request_number):
        return {
            'owner': environment['test_data']['owner'],
            'repo': environment['test_data']['repo']['name'],
            'number': pull_request_number
        }

    def create_pull_request_dto(self, branch=None):
        if branch == 'conflict':
            branch = environment['test_data']['conflict_branch']
        elif branch == 'not exist':
            branch = 'branch_not_exist'
        else:
             branch = random.choice(environment['test_data']['branches'])
        return {
            "title": 'Amazing new feature',
            "body": str(Faker().text()[0:20]),
            "head": '{username}:{branch}'.format(
                username=environment['test_data']['owner'],
                branch=branch
            ),
            "base": "master"}

    def update_pull_request_dto(self, state):
        return {
            "body": "updated body",
            "state": state,
            "base": "master"
        }

    def get_all_pull_requests(self):
        request = self.pull_request.get_all_pull_requests(self.all_pull_request_dto())
        if request.status_code != 200:
            raise ExpectedStatusCodeError
        return request.json()

    def get_single_pull_requests(self, pull_request):
        request = self.pull_request.get_single_pull_request(self.single_pull_request_dto(pull_request['number']))
        if request.status_code != 200:
            raise ExpectedStatusCodeError(request, 200)
        return request.json()

    def create_pull_request(self, conflict=None):
        request = self.pull_request.create_pull_request(self.all_pull_request_dto(),
                                                        self.create_pull_request_dto(conflict))
        if request.status_code != 201:
            raise ExpectedStatusCodeError(request, 201)
        return request.json()

    def update_pull_request(self, pull_request, state):
        request = self.pull_request.update_pull_request(self.single_pull_request_dto(pull_request['number']),
                                                        self.update_pull_request_dto(state))
        if request.status_code != 200:
            raise ExpectedStatusCodeError(request, 200)
        return request.json()

    def merge_pull_request(self, pull_request):
        request = self.pull_request.merge_pull_request(self.single_pull_request_dto(pull_request['number']))
        if request.status_code != 200:
            raise ResourceNotFound(request)
        return request.json()
