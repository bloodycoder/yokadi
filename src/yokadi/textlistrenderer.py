# -*- coding: UTF-8 -*-
"""
Text rendering of t_list output

@author: Aurélien Gâteau <aurelien.gateau@free.fr>
@license: GPLv3
"""
from datetime import datetime

import colors as C
import dateutils
from db import Config, Task


def colorizer(value, reverse=False):
    """Return a color according to value.
    @param value: value used to determine color. Low (0) value means not urgent/visible, high (100) value means important
    @param reverse: If false low value means important and vice versa
    @return: a color code or None for no color"""
    if reverse:
        value = 100 - value
    if value > 75:
        return C.RED
    elif value > 50:
        return C.PURPLE
    elif value > 25:
        return C.ORANGE
    else:
        return None


class Column(object):
    __slots__ = ["title", "width", "formater"]

    def __init__(self, title, width, formater):
        """
        formater is a callable which accepts a task and returns a tuple
        of the form (string, color)
        color may be None if no color should be applied
        """
        self.title = title
        self.width = width
        self.formater = formater


    def createHeader(self):
        return self.title.ljust(self.width)


    def createCell(self, task):
        value, color = self.formater(task)

        if color:
            cell = color
        else:
            cell = ""
        cell = cell + value.ljust(self.width)
        if color:
            cell = cell + C.RESET
        return cell


def idFormater(task):
    return str(task.id), None

class TitleFormater(object):
    def __init__(self, width):
        self.width = width

    def __call__(self, task):
        title = task.title
        hasDescription = task.description != ""
        maxLength = self.width
        if hasDescription:
            maxLength -= 1
        if len(title) > maxLength:
            title = title[:maxLength - 1] + ">"
        else:
            title = title.ljust(maxLength)
        if hasDescription:
            title = title + "*"

        return title, None

def urgencyFormater(task):
    return str(task.urgency), colorizer(task.urgency)

def statusFormater(task):
    if task.status == "started":
        color = C.BOLD
    else:
        color = None
    return task.status[0].upper(), color

class AgeFormater(object):
    def __init__(self, today):
        self.today = today

    def __call__(self, task):
        delta = self.today - task.creationDate
        return dateutils.formatTimeDelta(delta), colorizer(delta.days)

class DueDateFormater(object):
    def __init__(self, today):
        self.today = today

    def __call__(self, task):
        if not task.dueDate:
            return "", None
        delta = task.dueDate - self.today
        if delta.days != 0:
            value = task.dueDate.strftime("%x %H:%M")
        else:
            value = task.dueDate.strftime("%H:%M")

        value = value + " (%s)" % dateutils.formatTimeDelta(delta)

        color = colorizer(delta.days * 33, reverse=True)
        return value, color


class TextListRenderer(object):
    def __init__(self, out):
        self.out = out
        today = datetime.today().replace(microsecond=0)
        titleWidth = int(Config.byName("TEXT_WIDTH").value)
        idWidth = max(2, len(str(Task.select().max(Task.q.id))))
        self.columns = [
            Column("ID"       , idWidth   , idFormater),
            Column("Title"    , titleWidth, TitleFormater(titleWidth)),
            Column("U"        , 3         , urgencyFormater),
            Column("S"        , 1         , statusFormater),
            Column("Age"      , 8         , AgeFormater(today)),
            Column("Due date" , 23        , DueDateFormater(today))
            ]


    def addTaskList(self, project, taskList):
        self._renderTaskListHeader(project.name)
        for task in taskList:
            self._renderTaskListRow(task)


    def end(self):
        pass


    def _renderTaskListHeader(self, projectName):
        cells = [x.createHeader() for x in self.columns]
        line = "|".join(cells)
        width = len(line)
        print >>self.out
        print >>self.out, C.CYAN + projectName.center(width) + C.RESET
        print >>self.out, C.BOLD + line + C.RESET
        print >>self.out, "-" * width


    def _renderTaskListRow(self, task):
        cells = [column.createCell(task) for column in self.columns]
        print >>self.out, "|".join(cells)
# vi: ts=4 sw=4 et