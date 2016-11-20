"""
Defines Redmine resources.
"""

from .base import BaseResource, registry
from .standard import (Project, Issue, TimeEntry, Enumeration, Attachment, IssueJournal, WikiPage, ProjectMembership,
                       IssueCategory, IssueRelation, Version, User, Group, Role, News, IssueStatus, Tracker, Query,
                       CustomField)
