# coding: utf-8

"""
    Determined API (Beta)

    Determined helps deep learning teams train models more quickly, easily share GPU resources, and effectively collaborate. Determined allows deep learning engineers to focus on building and training models at scale, without needing to worry about DevOps or writing custom code for common tasks like fault tolerance or experiment tracking.  You can think of Determined as a platform that bridges the gap between tools like TensorFlow and PyTorch --- which work great for a single researcher with a single GPU --- to the challenges that arise when doing deep learning at scale, as teams, clusters, and data sets all increase in size.  # noqa: E501

    OpenAPI spec version: 0.1
    Contact: community@determined.ai
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class V1Experiment(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'int',
        'description': 'str',
        'labels': 'list[str]',
        'start_time': 'datetime',
        'end_time': 'datetime',
        'state': 'Determinedexperimentv1State',
        'archived': 'bool',
        'num_trials': 'int',
        'progress': 'float',
        'username': 'str',
        'resource_pool': 'str',
        'searcher_type': 'str',
        'name': 'str',
        'notes': 'str'
    }

    attribute_map = {
        'id': 'id',
        'description': 'description',
        'labels': 'labels',
        'start_time': 'startTime',
        'end_time': 'endTime',
        'state': 'state',
        'archived': 'archived',
        'num_trials': 'numTrials',
        'progress': 'progress',
        'username': 'username',
        'resource_pool': 'resourcePool',
        'searcher_type': 'searcherType',
        'name': 'name',
        'notes': 'notes'
    }

    def __init__(self, id=None, description=None, labels=None, start_time=None, end_time=None, state=None, archived=None, num_trials=None, progress=None, username=None, resource_pool=None, searcher_type=None, name=None, notes=None):  # noqa: E501
        """V1Experiment - a model defined in Swagger"""  # noqa: E501

        self._id = None
        self._description = None
        self._labels = None
        self._start_time = None
        self._end_time = None
        self._state = None
        self._archived = None
        self._num_trials = None
        self._progress = None
        self._username = None
        self._resource_pool = None
        self._searcher_type = None
        self._name = None
        self._notes = None
        self.discriminator = None

        self.id = id
        if description is not None:
            self.description = description
        if labels is not None:
            self.labels = labels
        self.start_time = start_time
        if end_time is not None:
            self.end_time = end_time
        self.state = state
        self.archived = archived
        self.num_trials = num_trials
        if progress is not None:
            self.progress = progress
        self.username = username
        if resource_pool is not None:
            self.resource_pool = resource_pool
        self.searcher_type = searcher_type
        self.name = name
        if notes is not None:
            self.notes = notes

    @property
    def id(self):
        """Gets the id of this V1Experiment.  # noqa: E501

        The id of the experiment.  # noqa: E501

        :return: The id of this V1Experiment.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this V1Experiment.

        The id of the experiment.  # noqa: E501

        :param id: The id of this V1Experiment.  # noqa: E501
        :type: int
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def description(self):
        """Gets the description of this V1Experiment.  # noqa: E501

        The description of the experiment.  # noqa: E501

        :return: The description of this V1Experiment.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this V1Experiment.

        The description of the experiment.  # noqa: E501

        :param description: The description of this V1Experiment.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def labels(self):
        """Gets the labels of this V1Experiment.  # noqa: E501

        Labels attached to the experiment.  # noqa: E501

        :return: The labels of this V1Experiment.  # noqa: E501
        :rtype: list[str]
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """Sets the labels of this V1Experiment.

        Labels attached to the experiment.  # noqa: E501

        :param labels: The labels of this V1Experiment.  # noqa: E501
        :type: list[str]
        """

        self._labels = labels

    @property
    def start_time(self):
        """Gets the start_time of this V1Experiment.  # noqa: E501

        The time the experiment was started.  # noqa: E501

        :return: The start_time of this V1Experiment.  # noqa: E501
        :rtype: datetime
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this V1Experiment.

        The time the experiment was started.  # noqa: E501

        :param start_time: The start_time of this V1Experiment.  # noqa: E501
        :type: datetime
        """
        if start_time is None:
            raise ValueError("Invalid value for `start_time`, must not be `None`")  # noqa: E501

        self._start_time = start_time

    @property
    def end_time(self):
        """Gets the end_time of this V1Experiment.  # noqa: E501

        The time the experiment ended if the experiment is stopped.  # noqa: E501

        :return: The end_time of this V1Experiment.  # noqa: E501
        :rtype: datetime
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """Sets the end_time of this V1Experiment.

        The time the experiment ended if the experiment is stopped.  # noqa: E501

        :param end_time: The end_time of this V1Experiment.  # noqa: E501
        :type: datetime
        """

        self._end_time = end_time

    @property
    def state(self):
        """Gets the state of this V1Experiment.  # noqa: E501

        The current state of the experiment.  # noqa: E501

        :return: The state of this V1Experiment.  # noqa: E501
        :rtype: Determinedexperimentv1State
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this V1Experiment.

        The current state of the experiment.  # noqa: E501

        :param state: The state of this V1Experiment.  # noqa: E501
        :type: Determinedexperimentv1State
        """
        if state is None:
            raise ValueError("Invalid value for `state`, must not be `None`")  # noqa: E501

        self._state = state

    @property
    def archived(self):
        """Gets the archived of this V1Experiment.  # noqa: E501

        Boolean denoting whether the experiment was archived.  # noqa: E501

        :return: The archived of this V1Experiment.  # noqa: E501
        :rtype: bool
        """
        return self._archived

    @archived.setter
    def archived(self, archived):
        """Sets the archived of this V1Experiment.

        Boolean denoting whether the experiment was archived.  # noqa: E501

        :param archived: The archived of this V1Experiment.  # noqa: E501
        :type: bool
        """
        if archived is None:
            raise ValueError("Invalid value for `archived`, must not be `None`")  # noqa: E501

        self._archived = archived

    @property
    def num_trials(self):
        """Gets the num_trials of this V1Experiment.  # noqa: E501

        The number of trials linked to the experiment.  # noqa: E501

        :return: The num_trials of this V1Experiment.  # noqa: E501
        :rtype: int
        """
        return self._num_trials

    @num_trials.setter
    def num_trials(self, num_trials):
        """Sets the num_trials of this V1Experiment.

        The number of trials linked to the experiment.  # noqa: E501

        :param num_trials: The num_trials of this V1Experiment.  # noqa: E501
        :type: int
        """
        if num_trials is None:
            raise ValueError("Invalid value for `num_trials`, must not be `None`")  # noqa: E501

        self._num_trials = num_trials

    @property
    def progress(self):
        """Gets the progress of this V1Experiment.  # noqa: E501

        The current progress of the experiment.  # noqa: E501

        :return: The progress of this V1Experiment.  # noqa: E501
        :rtype: float
        """
        return self._progress

    @progress.setter
    def progress(self, progress):
        """Sets the progress of this V1Experiment.

        The current progress of the experiment.  # noqa: E501

        :param progress: The progress of this V1Experiment.  # noqa: E501
        :type: float
        """

        self._progress = progress

    @property
    def username(self):
        """Gets the username of this V1Experiment.  # noqa: E501

        The username of the user that created the experiment.  # noqa: E501

        :return: The username of this V1Experiment.  # noqa: E501
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this V1Experiment.

        The username of the user that created the experiment.  # noqa: E501

        :param username: The username of this V1Experiment.  # noqa: E501
        :type: str
        """
        if username is None:
            raise ValueError("Invalid value for `username`, must not be `None`")  # noqa: E501

        self._username = username

    @property
    def resource_pool(self):
        """Gets the resource_pool of this V1Experiment.  # noqa: E501


        :return: The resource_pool of this V1Experiment.  # noqa: E501
        :rtype: str
        """
        return self._resource_pool

    @resource_pool.setter
    def resource_pool(self, resource_pool):
        """Sets the resource_pool of this V1Experiment.


        :param resource_pool: The resource_pool of this V1Experiment.  # noqa: E501
        :type: str
        """

        self._resource_pool = resource_pool

    @property
    def searcher_type(self):
        """Gets the searcher_type of this V1Experiment.  # noqa: E501


        :return: The searcher_type of this V1Experiment.  # noqa: E501
        :rtype: str
        """
        return self._searcher_type

    @searcher_type.setter
    def searcher_type(self, searcher_type):
        """Sets the searcher_type of this V1Experiment.


        :param searcher_type: The searcher_type of this V1Experiment.  # noqa: E501
        :type: str
        """
        if searcher_type is None:
            raise ValueError("Invalid value for `searcher_type`, must not be `None`")  # noqa: E501

        self._searcher_type = searcher_type

    @property
    def name(self):
        """Gets the name of this V1Experiment.  # noqa: E501

        The experiment name.  # noqa: E501

        :return: The name of this V1Experiment.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this V1Experiment.

        The experiment name.  # noqa: E501

        :param name: The name of this V1Experiment.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def notes(self):
        """Gets the notes of this V1Experiment.  # noqa: E501

        The experiment notes.  # noqa: E501

        :return: The notes of this V1Experiment.  # noqa: E501
        :rtype: str
        """
        return self._notes

    @notes.setter
    def notes(self, notes):
        """Sets the notes of this V1Experiment.

        The experiment notes.  # noqa: E501

        :param notes: The notes of this V1Experiment.  # noqa: E501
        :type: str
        """

        self._notes = notes

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(V1Experiment, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, V1Experiment):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
