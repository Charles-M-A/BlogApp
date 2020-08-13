import os
import shutil

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import ScreenManager, Screen

import crypto
from database import DataBase


if os.name == "posix":
    private = "/home/charles/Downloads/CW/private/"
    userpath = "/home/charles/Downloads/CW/users/"
    public = "/home/charles/Downloads/CW/public/"
    path = "/home/charles/Downloads/CW/"
else:
    public = "C:/Users/macha/PycharmProjects/CW/public/"
    userpath = "C:/Users/macha/PycharmProjects/CW/users/"
    private = "C:/Users/macha/PycharmProjects/CW/private/"
    path = "C:/Users/macha/PycharmProjects/CW/"

value = {}


# the following two classes are for the selectable list view that is usedd to display the posts in order and interact
# with them
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''
    pass


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
            value.update(rv.data[index])
        else:
            print("selection removed for {0}".format(rv.data[index]))


# the account creation window class and its functions
class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):  # saving data to the normal and encrypted file
        log = open(path + "log.txt", "a")
        elog = open(path + "elog.txt", "a")
        if self.namee.text != "" and self.email.text != "" and self.email.text.count(
                "@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)
                os.mkdir(userpath + self.email.text + "/")
                log.write(self.email.text + " crated account\n")
                e = (self.email.text + " created account\n")
                e = e.encode()
                elog.write(crypto.encrypt(e) + "\n")
                self.reset()

                sm.current = "login"
            else:
                invalidForm()
                log.write(self.email.text + " account creation error\n")
                e = (self.email.text + " account creation error\n")
                e = e.encode()
                elog.write(crypto.encrypt(e) + "\n")
        else:
            invalidForm()
            log.write(self.email.text + " account creation error\n")
            e = (self.email.text + " account creation error\n")
            e = e.encode()
            elog.write(crypto.encrypt(e) + "\n")

        log.close()
        elog.close()

    def login(self):  # back to login sceen
        self.reset()
        sm.current = "login"

    def reset(self):  # clear all data
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""


# the login window class and its functions
class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):  # verifying credentials entered
        log = open(path + "log.txt", "a")
        elog = open(path + "elog.txt", "a")
        if db.validate(self.email.text, self.password.text):
            HomeWindow.current = self.email.text
            log.write(self.email.text + " logged in\n")
            e = (self.email.text + " logged in\n")
            e = e.encode()
            elog.write(crypto.encrypt(e) + "\n")
            self.reset()
            sm.current = "home"
        else:
            invalidLogin()
            log.write(self.email.text + " log in error\n")
            e = (self.email.text + "log in error\n")
            e = e.encode()
            elog.write(crypto.encrypt(e) + "\n")
        log.close()
        elog.close()

    def guestBtn(self):  # guest entry button
        allWindow.current = "Guest"
        self.reset()
        sm.current = "all"

    def createBtn(self):  # to create a new account
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


# home window with all the key navigation buttons and their functions
class HomeWindow(Screen):
    current = ""

    def logOut(self):  # logout
        log = open(path + "log.txt", "a")
        elog = open(path + "elog.txt", "a")
        log.write(self.current + " logged out\n")
        e = (self.current + " logged out\n")
        e = e.encode()
        elog.write(crypto.encrypt(e) + "\n")
        log.close()
        elog.close()
        sm.current = "login"

    def postBtn(self):  # to create a new post
        log = open(path + "log.txt", "a")
        elog = open(path + "elog.txt", "a")
        print("post button clicked")
        log.write(self.current + " clicked post\n")
        e = (self.current + " clicked post\n")
        e = e.encode()
        elog.write(crypto.encrypt(e) + "\n")
        PostWindow.current = self.current
        log.close()
        elog.close()
        sm.current = "postwin"

    def updateBtn(self):  # to update an existing post
        log = open(path + "log.txt", "a")
        elog = open(path + "elog.txt", "a")
        print("update post button clicked")
        log.write(self.current + " clicked update\n")
        e = (self.current + " clicked update\n")
        e = e.encode()
        elog.write(crypto.encrypt(e) + "\n")
        myWindow.current = self.current
        log.close()
        elog.close()
        sm.current = "my"

    def allBtn(self):  # to see all the public posts
        log = open(path + "log.txt", "a")
        elog = open(path + "elog.txt", "a")
        print("all post button clicked")
        log.write(self.current + " clicked all post\n")
        e = (self.current + " clicked all post\n")
        e = e.encode()
        elog.write(crypto.encrypt(e) + "\n")
        allWindow.current = self.current
        log.close()
        elog.close()
        sm.current = "all"

    def shared(self):  # to see all the posts that are shared with the current user
        log = open(path + "log.txt", "a")
        elog = open(path + "elog.txt", "a")
        print("shared with me button is clicked")
        log.write(self.current + " clicked shared with me\n")
        e = (self.current + " shared with me\n")
        e = e.encode()
        elog.write(crypto.encrypt(e) + "\n")
        sharedWindow.current = self.current
        log.close()
        elog.close()
        sm.current = "shared"


# the post creation window and its functions
class PostWindow(Screen):
    current = ""
    pname = ObjectProperty(None)
    content = ObjectProperty(None)
    visibility = ObjectProperty(None)
    imgsrc = ""
    videosrc = ""
    audiosrc = ""

    def cancelBtn(self):  # to cancel
        log = open(path + "log.txt", "a")
        elog = open(path + "elog.txt", "a")
        print("clicked cancel")
        log.write(self.current + " clicked cancel\n")
        e = (self.current + " clicked cancel\n")
        e = e.encode()
        elog.write(crypto.encrypt(e) + "\n")
        log.close()
        elog.close()
        sm.current = "home"

    def additionBtn(self):  # to upload image or video or audio
        log = open(path + "log.txt", "a")
        elog = open(path + "elog.txt", "a")
        print("clicked additions")
        log.write(self.current + " clicked additions\n")
        e = (self.current + " clicked additions\n")
        e = e.encode()
        elog.write(crypto.encrypt(e) + "\n")
        log.close()
        elog.close()
        additionsWindow.current = self.current
        sm.current = "addition"

    def post(self):  # to create the post
        log = open(path + "log.txt", "a")
        elog = open(path + "elog.txt", "a")
        print("clicked post")
        fold = self.pname.text
        fold = fold.replace(' ', '_')
        os.mkdir(userpath + self.current + "/" + fold)
        os.mkdir(userpath + self.current + "/" + fold + "/image/")
        os.mkdir(userpath + self.current + "/" + fold + "/video/")
        os.mkdir(userpath + self.current + "/" + fold + "/audio/")

        if self.visibility.text.lower() == "public":  # for public posts
            os.mkdir(public + fold + "/")
            os.mkdir(public + fold + "/image/")
            os.mkdir(public + fold + "/audio/")
            os.mkdir(public + fold + "/video/")
            f = open(public + fold + "/comment.txt", "w")
            f.close()
            f = open(public + fold + "/content.txt", "w")
            f.write(self.content.text)
            f.close()

            f = open(userpath + self.current + "/" + fold + "/comment.txt", "w")
            f.close()
            f = open(userpath + self.current + "/" + fold + "/content.txt", "w")
            f.write(self.content.text)
            f.close()
            if self.imgsrc:
                shutil.copy(self.imgsrc, userpath + self.current + "/" + fold + "/image/")
            if self.audiosrc:
                shutil.copy(self.audiosrc, userpath + self.current + "/" + fold + "/audio/")
            if self.videosrc:
                shutil.copy(self.videosrc, userpath + self.current + "/" + fold + "/video/")

            f = open(public + fold + "/ecomment.txt", "w")
            f.close()
            f = open(public + fold + "/econtent.txt", "w")
            f.write(crypto.encrypt(self.content.text.encode()))
            f.close()
            f = open(userpath + self.current + "/" + fold + "/ecomment.txt", "w")
            f.close()
            f = open(userpath + self.current + "/" + fold + "/econtent.txt", "w")
            f.write(crypto.encrypt(self.content.text.encode()))
            f.close()
        elif self.visibility.text.lower() == "private":  # for private posts
            os.mkdir(private + fold + "/")
            os.mkdir(private + fold + "/image/")
            os.mkdir(private + fold + "/audio/")
            os.mkdir(private + fold + "/video/")
            f = open(private + fold + "/comment.txt", "w")
            f.close()
            f = open(private + fold + "/content.txt", "w")
            f.write(self.content.text)
            f.close()
            f = open(userpath + self.current + "/" + fold + "/comment.txt", "w")
            f.close()
            f = open(userpath + self.current + "/" + fold + "/content.txt", "w")
            f.write(self.content.text)
            f.close()
            if self.imgsrc:
                shutil.copy(self.imgsrc, userpath + self.current + "/" + fold + "/image/")
            if self.audiosrc:
                shutil.copy(self.audiosrc, userpath + self.current + "/" + fold + "/audio/")
            if self.videosrc:
                shutil.copy(self.videosrc, userpath + self.current + "/" + fold + "/video/")

            f = open(private + fold + "/ecomment.txt", "w")
            f.close()
            f = open(private + fold + "/econtent.txt", "w")
            f.write(crypto.encrypt(self.content.text.encode()))
            f.close()
            f = open(userpath + self.current + "/" + fold + "/ecomment.txt", "w")
            f.close()
            f = open(userpath + self.current + "/" + fold + "/econtent.txt", "w")
            f.write(crypto.encrypt(self.content.text.encode()))
            f.close()
        else:  # in the case an email is provided
            s = []
            os.mkdir(private + fold + "/")
            os.mkdir(private + fold + "/image/")
            os.mkdir(private + fold + "/audio/")
            os.mkdir(private + fold + "/video/")
            f = open(private + fold + "/comment.txt", "w")
            f.close()
            f = open(private + fold + "/content.txt", "w")
            f.write(self.content.text)
            f.close()
            f = open(private + fold + "/shared.txt", "w")
            s = self.visibility.text.split(',')
            for d in s:
                f.write(d + "\n")
            f.close()
            f = open(userpath + self.current + "/" + fold + "/comment.txt", "w")
            f.close()
            f = open(userpath + self.current + "/" + fold + "/content.txt", "w")
            f.write(self.content.text)
            f.close()
            if self.imgsrc:
                shutil.copy(self.imgsrc, userpath + self.current + "/" + fold + "/image/")
            if self.audiosrc:
                shutil.copy(self.audiosrc, userpath + self.current + "/" + fold + "/audio/")
            if self.videosrc:
                shutil.copy(self.videosrc, userpath + self.current + "/" + fold + "/video/")

            f = open(private + fold + "/ecomment.txt", "w")
            f.close()
            f = open(private + fold + "/econtent.txt", "w")
            f.write(crypto.encrypt(self.content.text.encode()))
            f.close()
            f = open(private + fold + "/eshared.txt", "w")
            s = self.visibility.text.split(',')
            for d in s:
                f.write(crypto.encrypt(d.encode()) + "\n")
            f.close()
            f = open(userpath + self.current + "/" + fold + "/ecomment.txt", "w")
            f.close()
            f = open(userpath + self.current + "/" + fold + "/econtent.txt", "w")
            f.write(crypto.encrypt(self.content.text.encode()))
            f.close()

        log.write(self.current + " made a post\n")
        e = (self.current + " made a post\n")
        e = e.encode()
        elog.write(crypto.encrypt(e) + "\n")
        self.reset()
        log.close()
        elog.close()
        sm.current = "home"

    def reset(self):
        self.visibility.text = ""
        self.pname.text = ""
        self.content.text = ""


# lists all the owned posts
class myWindow(Screen):
    current = ""
    search_results = ObjectProperty()

    def cancelBtn(self):  # tp cancel
        log = open(path + "log.txt", "a")
        elog = open(path + "elog.txt", "a")
        print("clicked cancel")
        log.write(self.current + " clicked cancel\n")
        e = (self.current + " clicked cancel\n")
        e = e.encode()
        elog.write(crypto.encrypt(e) + "\n")
        log.close()
        elog.close()
        sm.current = "home"

    def update(self):  # to update any post
        log = open(path + "log.txt", "a")
        elog = open(path + "elog.txt", "a")
        print("clicked update")
        UpdateWindow.current = self.current
        UpdateWindow.post = value['text']
        log.write(self.current + " clicked update\n")
        e = (self.current + " clicked update\n")
        e = e.encode()
        elog.write(crypto.encrypt(e) + "\n")
        log.close()
        elog.close()
        sm.current = "update"

    def delete(self):  # to delete any post
        log = open(path + "log.txt", "a")
        elog = open(path + "elog.txt", "a")
        post = value['text']
        post = post.replace(" ", "_")
        shutil.rmtree(userpath + self.current + "/" + post + "/")
        if os.path.isdir(public + post + "/"):
            shutil.rmtree(public + post + "/")
        else:
            shutil.rmtree(private + post + "/")
        log.write(self.current + " delete\n" + post)
        e = (self.current + " delete\n" + post)
        e = e.encode()
        elog.write(crypto.encrypt(e) + "\n")
        log.close()
        elog.close()
        sm.current = "home"

    def on_enter(self, *args):
        mydir = []
        os.chdir(userpath + self.current + "/")
        all_subdirs = [d for d in os.listdir('.') if os.path.isdir(d)]
        for dirs in all_subdirs:
            dirs = dirs.replace("_", " ")
            mydir.append(dirs)
        self.search_results.data = [{'text': str(x)} for x in mydir]


# the update post window and functions
class UpdateWindow(Screen):
    current = ""
    post = ""
    flag = ""
    pname = ObjectProperty(None)
    content = ObjectProperty(None)
    visibility = ObjectProperty(None)

    def cancelBtn(self):  # to cancel
        log = open(path + "log.txt", "a")
        elog = open(path + "elog.txt", "a")
        print("clicked cancel")
        log.write(self.current + " clicked cancel\n")
        e = (self.current + " clicked cancel\n")
        e = e.encode()
        elog.write(crypto.encrypt(e) + "\n")
        log.close()
        elog.close()
        sm.current = "home"

    def updateB(self):  # to update
        log = open(path + "log.txt", "a")
        elog = open(path + "elog.txt", "a")
        print("clicked update")
        if self.flag == "public":
            if self.visibility.text.lower() == "public":  # public to public
                f = open(public + self.pname.text + "/content.txt", "w")
                f.write(self.content.text)
                f.close()
                f = open(userpath + self.current + "/" + self.pname.text + "/content.txt", "w")
                f.write(self.content.text)
                f.close()

                f = open(public + self.pname.text + "/econtent.txt", "w")
                f.write(crypto.encrypt(self.content.text.encode()))
                f.close()
                f = open(userpath + self.current + "/" + self.pname.text + "/econtent.txt", "w")
                f.write(crypto.encrypt(self.content.text.encode()))
                f.close()
            elif self.visibility.text.lower() == "private":  # public to private
                f = open(public + self.pname.text + "/content.txt", "w")
                f.write(self.content.text)
                f.close()
                shutil.move(public + self.pname.text + "/", private)
                f = open(userpath + self.current + "/" + self.pname.text + "/content.txt", "w")
                f.write(self.content.text)
                f.close()
            else:  # public to an email
                s = []
                f = open(public + self.pname.text + "/content.txt", "w")
                f.write(self.content.text)
                f.close()
                shutil.move(public + self.pname.text + "/", private)
                f.open(private + self.pname.text + "/shared.txt")
                s = self.visibility.text.split(',')
                for d in s:
                    f.write(d + "\n")
                f.close()
                f = open(userpath + self.current + "/" + self.pname.text + "/content.txt", "w")
                f.write(self.content.text)
                f.close()

                f = open(public + self.pname.text + "/econtent.txt", "w")
                f.write(crypto.encrypt(self.content.text.encode()))
                f.close()
                shutil.move(public + self.pname.text + "/", private)
                f.open(private + self.pname.text + "/eshared.txt")
                s = self.visibility.text.split(',')
                for d in s:
                    f.write(crypto.encrypt(d.encode()) + "\n")
                f.close()
                f = open(userpath + self.current + "/" + self.pname.text + "/econtent.txt", "w")
                f.write(crypto.encrypt(self.content.text.encode()))
                f.close()
        elif self.flag == "private":  # private to private
            if self.visibility.text.lower() == "private":
                f = open(private + self.pname.text + "/content.txt", "w")
                f.write(self.content.text)
                f.close()
                f = open(userpath + self.current + "/" + self.pname.text + "/content.txt", "w")
                f.write(self.content.text)
                f.close()

                f = open(private + self.pname.text + "/econtent.txt", "w")
                f.write(crypto.encrypt(self.content.text.encode()))
                f.close()
                f = open(userpath + self.current + "/" + self.pname.text + "/econtent.txt", "w")
                f.write(crypto.encrypt(self.content.text.encode()))
                f.close()
            elif self.visibility.text.lower() == "public":  # private to public
                f = open(private + self.pname.text + "/content.txt", "w")
                f.write(self.content.text)
                f.close()
                shutil.move(private + self.pname.text + "/", public)
                f = open(userpath + self.current + "/" + self.pname.text + "/content.txt", "w")
                f.write(self.content.text)
                f.close()

                f = open(public + self.pname.text + "/econtent.txt", "w")
                f.write(crypto.encrypt(self.content.text.encode()))
                f.close()
                shutil.move(public + self.pname.text + "/", public)
                f = open(userpath + self.current + "/" + self.pname.text + "/econtent.txt", "w")
                f.write(crypto.encrypt(self.content.text.encode()))
                f.close()
            else:  # private to an email
                f = open(private + self.pname.text + "/content.txt", "w")
                f.write(self.content.text)
                f.close()
                f.open(private + self.pname.text + "/shared.txt")
                s = self.visibility.text.split(',')
                for d in s:
                    f.write(d + "\n")
                f.close()
                f = open(userpath + self.current + "/" + self.pname.text + "/content.txt", "w")
                f.write(self.content.text)
                f.close()

                f = open(private + self.pname.text + "/econtent.txt", "w")
                f.write(crypto.encrypt(self.content.text.encode()))
                f.close()
                f.open(private + self.pname.text + "/eshared.txt")
                s = self.visibility.text.split(',')
                for d in s:
                    f.write(crypto.encrypt(d.encode()) + "\n")
                f.close()
                f = open(userpath + self.current + "/" + self.pname.text + "/econtent.txt", "w")
                f.write(crypto.encrypt(self.content.text))
                f.close()
        log.write(self.current + " updated post\n")
        e = (self.current + " updated post\n")
        e = e.encode()
        elog.write(crypto.encrypt(e) + "\n")
        self.reset()
        log.close()
        elog.close()
        sm.current = "home"

    def reset(self):
        self.visibility.text = ""
        self.pname.text = ""
        self.content.text = ""

    def on_enter(self, *args):
        self.post = self.post.replace(" ", "_")
        self.pname.text = self.post
        f = open(userpath + self.current + "/" + self.post + "/content.txt", "r")
        data = f.read()
        self.content.text = data
        if os.path.isdir(public + self.post + "/"):
            self.visibility.text = "public"
            self.flag = "public"
        else:
            self.visibility.text = "private"
            self.flag = "private"


# to see all the public posts
class allWindow(Screen):
    current = ""
    search_results = ObjectProperty()

    def cancelBtn(self):  # to cancel
        log = open(path + "log.txt", "a")
        elog = open(path + "elog.txt", "a")
        print("clicked cancel")
        log.write(self.current + " clicked cancel\n")
        e = (self.current + " clicked cancel\n")
        e = e.encode()
        elog.write(crypto.encrypt(e) + "\n")
        log.close()
        elog.close()
        if self.current == "Guest":
            sm.current = "login"
        else:
            sm.current = "home"

    def view(self):  # to view a selected post
        log = open(path + "log.txt", "a")
        elog = open(path + "elog.txt", "a")
        print("clicked view")
        log.write(self.current + " clicked view\n")
        e = (self.current + " clicked view\n")
        e = e.encode()
        elog.write(crypto.encrypt(e) + "\n")
        viewWindow.current = self.current
        # viewWindow.post = value['text']
        viewWindow.shared = False
        log.close()
        elog.close()
        sm.current = "view"

    def on_enter(self, *args):
        mydir = []
        os.chdir(public)
        all_subdirs = [d for d in os.listdir('.') if os.path.isdir(d)]
        for dirs in all_subdirs:
            dirs = dirs.replace("_", " ")
            mydir.append(dirs)
        self.search_results.data = [{'text': str(x)} for x in mydir]


# the post viewing window
class viewWindow(Screen):
    current = ""
    post = ""
    folder = ""
    shared = bool

    def back(self):  # to go back
        print("clicked back")
        log = open(path + "log.txt", "a")
        elog = open(path + "elog.txt", "a")
        log.write(self.current + " clicked back\n")
        e = (self.current + " clicked back\n")
        e = e.encode()
        elog.write(crypto.encrypt(e) + "\n")
        log.close()
        elog.close()
        if self.shared:
            sm.current = "shared"
        else:
            sm.current = "all"

    def on_enter(self, *args):
        self.post = value["text"]
        print("view wndow " + self.post)
        self.folder = self.post
        self.post = self.post.replace(" ", "_")
        self.head.text = self.folder
        if self.shared == True:
            print("shared true " + self.post)
            f = open(private + self.post + "/content.txt", "r")
            data = f.read()
            self.slabel.text = data
            f.close()
            f = open(private + self.post + "/comment.txt", "r")
            com = f.read()
            f.close()
        else:
            print("shared false " + self.post)
            f = open(public + self.post + "/content.txt", "r")
            data = f.read()
            self.slabel.text = data
            f.close()
            f = open(public + self.post + "/comment.txt", "r")
            com = f.read()
            f.close()
        self.comment.text = com

    def add(self):  # to comment
        if self.current == "Guest":
            self.com.text = "Guest cannot comment"
        else:
            log = open(path + "log.txt", "a")
            elog = open(path + "elog.txt", "a")
            if self.shared:
                f = open(private + self.post + "/comment.txt", "a+")
                print(self.com.text)
                data = self.current + ": " + self.com.text + "\n"
                f.write(data)
                f.close()
                print(self.current)
                print(self.folder)

                f = open(private + self.post + "/ecomment.txt", "a+")
                data = self.current + ": " + self.com.text + "\n"
                f.write(crypto.encrypt(data.encode()))
                f.close()
            else:
                f = open(public + self.post + "/comment.txt", "a")
                print(self.com.text)
                data = self.current + ": " + self.com.text
                f.write(data)
                f.close()
                print(self.current)
                print(self.folder)

                f = open(public + self.post + "/ecomment.txt", "a")
                print(self.com.text)
                data = self.current + ": " + self.com.text
                f.write(crypto.encrypt(data.encode()))
                f.close()
                print(self.current)
                print(self.folder)

            log.write(self.current + " clicked comment\n")
            e = (self.current + " clicked comment\n")
            e = e.encode()
            elog.write(crypto.encrypt(e) + "\n")
            self.com.text = ""
            log.close()
            elog.close()


# to see all the posts that are shared with the user
class sharedWindow(Screen):
    current = ""
    search_results = ObjectProperty()

    def cancelBtn(self):  # to cancel
        log = open(path + "log.txt", "a")
        elog = open(path + "elog.txt", "a")
        print("clicked cancel")
        log.write(self.current + " clicked cancel\n")
        e = (self.current + " clicked cancel\n")
        e = e.encode()
        elog.write(crypto.encrypt(e) + "\n")
        log.close()
        elog.close()
        sm.current = "home"

    def viewb(self):  # to view a selected post
        log = open(path + "log.txt", "a")
        elog = open(path + "elog.txt", "a")
        print("clicked view")
        viewWindow.current = self.current
        print(value['text'] + "     ---")
        # viewWindow.post = value['text']
        log.write(self.current + " clicked view\n")
        e = (self.current + " clicked view\n")
        e = e.encode()
        elog.write(crypto.encrypt(e) + "\n")
        log.close()
        elog.close()
        viewWindow.shared = True
        sm.current = "view"

    def on_enter(self, *args):
        shareddir = []
        myshared = []
        os.chdir(private)
        all_subdirs = [d for d in os.listdir('.') if os.path.isdir(d)]
        for dirs in all_subdirs:
            if os.path.isfile(private + dirs + "/shared.txt"):
                shareddir.append(dirs)
        for dirs in shareddir:
            with open(private + dirs + "/shared.txt") as f:
                if self.current in f.read():
                    myshared.append(dirs)
        self.search_results.data = [{'text': str(x)} for x in myshared]


# the multimedia pload window
class additionsWindow(Screen):
    img = ObjectProperty(None)
    video = ObjectProperty(None)
    audio = ObjectProperty(None)
    current = ""

    def cancelBtn(self):  # to cancel
        log = open(path + "log.txt", "a")
        elog = open(path + "elog.txt", "a")
        print("clicked cancel")
        log.write(self.current + " clicked cancel\n")
        e = (self.current + " clicked cancel\n")
        e = e.encode()
        elog.write(crypto.encrypt(e) + "\n")
        log.close()
        elog.close()
        sm.current = "postwin"

    def upload(self):  # to upload
        PostWindow.imgsrc = self.img.text
        PostWindow.videosrc = self.video.text
        PostWindow.audiosrc = self.audio.text
        PostWindow.current = self.current
        log = open(path + "log.txt", "a")
        elog = open(path + "elog.txt", "a")
        print("clicked upload")
        log.write(self.current + " clicked upload\n")
        e = (self.current + " clicked upload\n")
        e = e.encode()
        elog.write(crypto.encrypt(e) + "\n")
        log.close()
        elog.close()
        sm.current = "postwin"


class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Invalid Login',
                content=Label(text='Invalid username or password.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                content=Label(text='Please fill in all inputs with valid information.'),
                size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()
db = DataBase("users.txt", "eusers.txt")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"),
           HomeWindow(name="home"), PostWindow(name="postwin"), myWindow(name="my"), UpdateWindow(name="update"),
           allWindow(name="all"), viewWindow(name="view"), sharedWindow(name="shared"),
           additionsWindow(name="addition")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
