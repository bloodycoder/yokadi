# coding:utf-8
"""
Ical utils functions
@author: Sébastien Renard <Sebastien.Renard@digitalfox.org>
@license: GPL v3 or later
"""
import re

import icalendar


UID_PREFIX = "yokadi"
PROJECT_PREFIX = UID_PREFIX + "-project-"


def _clamp(value, minimum, maximum):
    return minimum if value < minimum else maximum if value > maximum else value


def convertIcalType(attr):
    """Convert data from icalendar types (vDates, vInt etc.) to python standard equivalent
    @param attr: icalendar type
    @return: python type"""
    if isinstance(attr, (icalendar.vDate, icalendar.vDatetime,
                         icalendar.vDuration, icalendar.vDDDTypes)):
        return attr.dt
    elif isinstance(attr, (icalendar.vInt, icalendar.vFloat)):
        return int(attr)
    else:
        # Default to unicode string
        return str(attr)


def icalPriorityToYokadiUrgency(priority):
    """Convert ical priority (1 / 9) to yokadi urgency (100 / -99)
    @param priority: ical priority
    @return: yokadi urgency"""
    urgency = 100 - 20 * priority
    return _clamp(urgency, -99, 100)


def yokadiUrgencyToIcalPriority(urgency):
    """Convert yokadi urgency (100 / -99) to ical priority (1 / 9)
    @param urgency: yokadi urgency
    @return: ical priority"""
    priority = int(-(urgency - 100) / 20)
    return _clamp(priority, 1, 9)


def yokadiTaskTitleToIcalSummary(title, taskId):
    """Append " (id)" to the end of title"""
    return "{} ({})".format(title, taskId)


def icalSummaryToYokadiTaskTitle(summary, taskId):
    """Remove " (id)" part of the summary"""
    return re.sub("\s?\({}\)".format(taskId), "", summary)


def yokadiProjectNameToIcalRelatedTo(projectName):
    return PROJECT_PREFIX + projectName


def icalRelatedToToYokadiProjectName(relatedTo):
    return relatedTo[len(PROJECT_PREFIX):]


# vi: ts=4 sw=4 et
