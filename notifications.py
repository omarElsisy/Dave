import dbus
from collections import OrderedDict
from dbus.mainloop.glib import DBusGMainLoop
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from report import Ui_ReportWindow

APP_NAME = ''
DBUS_IFACE = None
NOTIFICATIONS = {}

def init(app_name):
    # Initializes the DBus connection
    global APP_NAME, DBUS_IFACE
    APP_NAME = app_name

    name = "org.freedesktop.Notifications"
    path = "/org/freedesktop/Notifications"
    interface = "org.freedesktop.Notifications"

    mainloop = DBusGMainLoop(set_as_default=True)

    bus = dbus.SessionBus(mainloop)
    proxy = bus.get_object(name, path)
    DBUS_IFACE = dbus.Interface(proxy, interface)

    # We have a mainloop, so connect callbacks
    DBUS_IFACE.connect_to_signal('ActionInvoked', _onActionInvoked)
    DBUS_IFACE.connect_to_signal('NotificationClosed', _onNotificationClosed)

def _onActionInvoked(nid, action):
    # Called when a notification action is clicked
    nid, action = int(nid), str(action)
    try:
        notification = NOTIFICATIONS[nid]
    except KeyError:
        # must have been created by some other program
        return
    notification._onActionInvoked(action)

def _onNotificationClosed(nid, reason):
    # Called when the notification is closed
    nid, reason = int(nid), int(reason)
    try:
        notification = NOTIFICATIONS[nid]
    except KeyError:
        # must have been created by some other program
        return
    notification._onNotificationClosed(notification)
    del NOTIFICATIONS[nid]

class Notification(object):
    id = 0
    timeout = -1
    _onNotificationClosed = lambda *args: None

    def __init__(self, title, body='', icon='', timeout=-1):
        self.title = title
        self.body = body
        self.icon = icon                # the path to the icon to use
        self.timeout = timeout          # time in ms before the notification disappears
        self.hints = {}                 # dict of various display hints
        self.actions = OrderedDict()    # actions names and their callbacks
        self.data = {}                  # arbitrary user data

    def show(self):

        # Asks the notification server to show the notification
        nid = DBUS_IFACE.Notify(APP_NAME, self.id, self.icon, self.title, self.body, self._makeActionsList(), self.hints, self.timeout)

        self.id = int(nid)

        NOTIFICATIONS[self.id] = self
        return True

    def close(self):
        # Ask the notification server to close the notification
        if self.id != 0:
            DBUS_IFACE.CloseNotification(self.id)

    def setUrgency(self, value):
        # Set the notification urgency level
        self.hints['urgency'] = dbus.Byte(value)

    def setSoundName(self, sound_name):
        # Set a sound name to play when notification shows
        self.hints['sound-name'] = sound_name

    def setIconPath(self, icon_path):
        # Set the URI of the icon to display in the notification
        self.hints['image-path'] = 'file://' + icon_path

    def setCategory(self, category):
        # Sets the the notification category
        self.hints['category'] = category

    def addAction(self, action, label, callback, main_window=None, mood=None, arousal_list=None, valence_list=None, heart_rate_list=None):
        # Add notification action (when a button is clicked)
        self.actions[action] = (label, callback, main_window, mood, arousal_list, valence_list, heart_rate_list)

    def _makeActionsList(self):
        # Make the actions array to send over DBus
        arr = []
        for action, (label, callback, main_window, mood, arousal_list, valence_list, heart_rate_list) in self.actions.items():
            arr.append(action)
            arr.append(label)
        return arr

    def _onActionInvoked(self, action):
        # Called when the user activates a notification action
        try:
            label, callback, main_window, mood, arousal_list, valence_list, heart_rate_list = self.actions[action]
        except KeyError:
            return

        if main_window is None:
            # Call the callback function of ignore button
            callback(self, action)
        else:
            # Call the callback function of show button
            callback(self, action, main_window, mood, arousal_list, valence_list, heart_rate_list)


def show_report(n, action, self, mood, arousal_list, valence_list, heart_rate_list):
    assert(action == "show"), "Action was not show!"
    # open the report window when show button is clicked
    self.MainWindow = QtWidgets.QMainWindow()
    self.ui = Ui_ReportWindow(arousal_list, valence_list, heart_rate_list, mood)
    self.ui.setupUi(self.MainWindow)
    self.MainWindow.show()
    n.close()

def ignore_report(n, action):
    assert(action == "ignore"), "Action was not ignore!"
    n.close()

def get_username():
    username = ""
    username = os.getenv("LOGNAME")
    if(username == ""):
        username = os.getenv("USERNAME")
        if(username == ""):
            username = os.getenv("USER")
    return username

def show_notification(self, mood, arousal_list, valence_list, heart_rate_list):
    # Initialize the DBus connection to the notification server
    init("Dave")

    username = get_username()
    # Initialize a new notification object
    n = Notification("Dave", "Hey "+username+", Your analysis report is ready. Check it out!", timeout=10000)
    n.setUrgency(1)
    n.setCategory("im.received")
    n.setSoundName("message-new-instant")
    n.setIconPath("/home/amr/Downloads/Projects/Dave/logo.png")
    n.addAction("show", "Show", show_report, self, mood, arousal_list, valence_list, heart_rate_list)
    n.addAction("ignore", "Ignore", ignore_report)
    n.show()