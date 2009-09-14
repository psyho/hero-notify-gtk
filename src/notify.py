#!/usr/bin/python
import pygtk
pygtk.require('2.0')
import gtk
import pynotify
import time
import sys
import gobject
import urllib

def notifyAvailable():
  n = pynotify.Notification("HTC Hero available in Play!", "HTC Hero is now available in Play e-shop for purchase.", "dialog-info")
  n.show()
  return True

def notifyError(title, message):
  n = pynotify.Notification(title, message, "dialog-error")
  n.show()
  return True

def fetchPlayLinks():
  try:
    url = "http://web.playmobile.pl/resources/flash/telefony/linki.csv"
    result = urllib.urlopen(url)
    return result.read()
  except IOError:
    return None

def getHeroLine(content):
  for line in content.splitlines():
    if 'htchero' in line: return line
  return None

def isHeroAvailable(line):
  parts = [str for str in line.split(';') if str]
  return len(parts) > 2

def checkAvailability(trayIndicator):
  content = fetchPlayLinks()
  if not content: return notifyError("Error retrieving data", "Could not download the data file from play.")
  line = getHeroLine(content)
  if not line: return notifyError("Error parsing data", "Could not find the HTC hero line")
  available = isHeroAvailable(line)
  trayIndicator.setAvailable(available)
  if available: notifyAvailable()
  return True

class TrayIndicator:

  def __init__(self):
    self.statusIcon = gtk.StatusIcon()
    self.statusIcon.set_from_stock(gtk.STOCK_ABOUT)
    self.statusIcon.set_visible(True)
    self.statusIcon.set_tooltip("HTC Hero in Play")

    self.menu = gtk.Menu()
    self.menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
    self.menuItem.connect('activate', self.quit_cb, self.statusIcon)
    self.menu.append(self.menuItem)

    self.statusIcon.connect('popup-menu', self.popup_menu_cb, self.menu)
    self.statusIcon.set_visible(1)

    pynotify.init('HTC Hero in Play notifier')
    gobject.timeout_add(30000, checkAvailability, self)

    gtk.main()

  def quit_cb(self, widget, data=None):
    gtk.main_quit()

  def setAvailable(self, available):
    print 'setting status icon'
    icon = gtk.STOCK_NO
    if available: icon = gtk.STOCK_YES
    tooltip = "HTC Hero is not available"
    if available: tooltip = "HTC Hero is available!"

    self.statusIcon.set_visible(0)

    self.statusIcon = gtk.StatusIcon()
    self.statusIcon.set_from_stock(icon)
    self.statusIcon.set_visible(True)
    self.statusIcon.set_tooltip(tooltip)

    self.statusIcon.connect('popup-menu', self.popup_menu_cb, self.menu)
    self.statusIcon.set_visible(1)

  def popup_menu_cb(self, widget, button, time, data=None):
    if button == 3:
      if data:
        data.show_all()
        data.popup(None, None, gtk.status_icon_position_menu,
                   3, time, self.statusIcon)

if __name__ == '__main__':
  TrayIndicator()
  sys.exit(0)

