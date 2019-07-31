from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
from random import randint, choice
from math import radians
import kivent_core
import kivent_cymunk
from kivent_core.gameworld import GameWorld
from kivent_core.managers.resource_managers import texture_manager
from kivent_core.systems.renderers import RotateRenderer
from kivent_core.systems.position_systems import PositionSystem2D
from kivent_core.systems.rotate_systems import RotateSystem2D
from kivent_cymunk.interaction import CymunkTouchSystem
from kivy.properties import StringProperty, NumericProperty
import kivent_particles
from kivent_core.systems.gamesystem import GameSystem
from kivy.factory import Factory
from cymunk import PivotJoint
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.graphics import Color, Rectangle
from kivy.storage.dictstore import DictStore
from kivy.graphics.vertex_instructions import Rectangle
from assestsids import ent, attgen
from utils import get_asset_path
import os
# from jnius import autoclass
# from android.runnable import run_on_ui_thread

os.environ['KIVY_AUDIO'] = 'sdl2'


# PythonActivity = autoclass('org.kivy.android.PythonActivity')
# Context = autoclass('android.content.Context')
# activity = PythonActivity.mActivity
# vibrator = activity.getSystemService(Context.VIBRATOR_SERVICE)
#
# View = autoclass('android.view.View')
# Param = autoclass('android.view.WindowManager$LayoutParams')


sysbox = []

texture_manager.load_atlas('assets/platform.atlas')
rendertop = 'rotate_color_scale_renderertop'
render = 'rotate_color_scale_renderer'
render2 = 'rotate_color_scale_renderer2'

bg_width, bg_height = 950, 587
width, height = Window.size
center = Window.center
ws = float(width) / bg_width
hs = float(height) / bg_height

scale = min(ws, hs)

if ws > hs:
    gap = width - (bg_width * hs)
    blank_rect1 = ((width - gap/2, 0), (gap/2, height))
    blank_rect2 = ((0, 0), (gap/2, height))
    wscale = gap/2
    hscale = 0

else:
    gap = height - (bg_height * ws)
    blank_rect1 = ((0, (height - (gap/2))+1), (width, gap/2))
    blank_rect2 = ((0, -1), (width, gap/2))
    hscale = gap/2
    wscale = 0



class BoundarySystem(GameSystem):
    def __init__(self, **kwargs):
        super(BoundarySystem, self).__init__(**kwargs)
        self.shut = 0
        self.bottomset = False
        self.level = 0

        self.touchbox = []
        self.force = []
        self.removebulletlist = []

        self.bulletlist = ['bullet', 'bullet2', 'bullet3', 'bullet4', 'bullet5', 'bullet6', 'bullet7', 'bullet8',
        'bullet9', 'bullet10', 'bullet11', 'bullet12', 'bullet13', 'bullet14', 'bullet15',
        'bullet16', 'bullet17', 'bullet18', 'bullet19', 'bullet20', 'bullet21', 'bullet22',
        'bullet23', 'bullet24', 'bullet25', 'bullet26', 'bullet27', 'bullet28', 'bullet29', 'bullet30']

        self.samelevels = [1,2,3,5,6,]
        self.cur_str = None
        self.sp1 = False
        self.sp2 = False

        self.stopbullets = False
        self.objs = []
        self.objs2 = []
        self.objs3 = []
        self.objs4 = []
        self.magicforce = None
        self.cancelcall = False

    def bottomborder(self):
        entities = self.gameworld.entities
        physics = self.gameworld.system_manager['cymunk_physics']
        if self.level != 4:
            entity = entities[ent['barrier2']]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = ((475 *scale)+wscale, (46 *scale)+hscale)
            physics.space.reindex_shape(shape[0])
            self.bottomset = True

        else:
            entity = entities[ent['barrier4']]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = ((-12 *scale)+wscale, (293.5 *scale)+hscale)
            physics.space.reindex_shape(shape[0])
            self.bottomset = True

    def bottomborderoff(self):
        entities = self.gameworld.entities
        physics = self.gameworld.system_manager['cymunk_physics']
        if self.level != 4:
            entity = entities[ent['barrier2']]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = (475 *scale, -1735 *scale)
            physics.space.reindex_shape(shape[0])
            self.bottomset = True

        else:
            entity = entities[ent['barrier4']]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = (475 *scale, -1735 *scale)
            physics.space.reindex_shape(shape[0])
            self.bottomset = True

    def call8(self):
        entities = self.gameworld.entities
        physics = self.gameworld.system_manager['cymunk_physics']
        if self.cur_str == ent['spstriker']:
            entity = entities[ent['bot1']]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = ((475 *scale)+wscale, (46 *scale)+hscale)
            physics.space.reindex_shape(shape[0])

        elif self.cur_str == ent['spstriker2']:
            entity = entities[ent['bot2']]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = ((475 *scale)+wscale, (46 *scale)+hscale)
            physics.space.reindex_shape(shape[0])

    def on_touch_down(self, touch):
        entities = self.gameworld.entities
        physics = self.gameworld.system_manager['cymunk_physics']

        if self.level in self.samelevels and self.shut == 1:
            entity = entities[ent['barrier']]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = ((475 *scale)+wscale, (400 *scale)+hscale)
            physics.space.reindex_shape(shape[0])

        elif self.level == 4 and self.shut == 1:
            entity = entities[ent['barrier3']]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = ((745 *scale)+wscale, (293.5 *scale)+hscale)
            physics.space.reindex_shape(shape[0])

        elif self.level == 8:
            physics = self.gameworld.system_manager['cymunk_physics']
            if not self.sp1 or not self.sp2:
                if self.cur_str == None:
                    entity = entities[ent['barrier']]
                    body = entity.cymunk_physics.body
                    shape = entity.cymunk_physics.shapes
                    body.position = ((475 *scale)+wscale, (400 *scale)+hscale)
                    physics.space.reindex_shape(shape[0])

                elif self.cur_str == ent['spstriker']:
                    entity = entities[ent['bar1']]
                    body = entity.cymunk_physics.body
                    shape = entity.cymunk_physics.shapes
                    body.position = ((475 *scale)+wscale, (400 *scale)+hscale)
                    physics.space.reindex_shape(shape[0])



                elif self.cur_str == ent['spstriker2']:
                    entity = entities[ent['bar2']]
                    body = entity.cymunk_physics.body
                    shape = entity.cymunk_physics.shapes
                    body.position = ((475 *scale)+wscale, (400 *scale)+hscale)
                    physics.space.reindex_shape(shape[0])

    def on_touch_up(self, touch):
        entities = self.gameworld.entities
        physics = self.gameworld.system_manager['cymunk_physics']
        if self.level in self.samelevels and self.shut == 1:
            entity = entities[ent['barrier']]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = (475 *scale, 2265 *scale)
            physics.space.reindex_shape(shape[0])

        elif self.level == 4 and self.shut == 1:
            entity = entities[ent['barrier3']]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = (475 *scale, 2265 *scale)
            physics.space.reindex_shape(shape[0])

        elif self.level == 8 and self.cur_str == None:
            entity = entities[ent['barrier']]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = (475 *scale, 2265 *scale)
            physics.space.reindex_shape(shape[0])

        elif self.level == 8 and self.cur_str == ent['spstriker']:
            entity = entities[ent['bar1']]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = (475 *scale, 2265 *scale)
            physics.space.reindex_shape(shape[0])

        elif self.level == 8 and self.cur_str == ent['spstriker2']:
            entity = entities[ent['bar2']]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = (475 *scale, 2265 *scale)
            physics.space.reindex_shape(shape[0])

        elif self.level == 9 and not self.stopbullets:
            if len(self.bulletlist) == 0:
                self.bulletlist = ['bullet', 'bullet2', 'bullet3', 'bullet4', 'bullet5', 'bullet6', 'bullet7', 'bullet8',
        'bullet9', 'bullet10', 'bullet11', 'bullet12', 'bullet13', 'bullet14', 'bullet15',
        'bullet16', 'bullet17', 'bullet18', 'bullet19', 'bullet20', 'bullet21', 'bullet22',
        'bullet23', 'bullet24', 'bullet25', 'bullet26', 'bullet27', 'bullet28', 'bullet29', 'bullet30']

            # entity = entities[ent['gun']]
            # body = entity.cymunk_physics.body
            # body.reset_forces()
            # body.angular_velocity = 0
            # body.velocity = [0, 0]
            if len(self.touchbox) > 4 and self.touchbox[-1] > self.touchbox[-0]:
                entity = entities[ent['startpoint']]
                body = entity.cymunk_physics.body

                startpos = body.position


                entity = entities[ent['endpoint']]
                body = entity.cymunk_physics.body
                endpos = body.position

                for x in endpos:
                    self.force.append(x)
                for x in startpos:
                    self.force.append(x)

                force = self.force[0]-self.force[2], self.force[1]- self.force[3]


                entity = entities[ent[self.bulletlist[0]]]
                body = entity.cymunk_physics.body
                shape = entity.cymunk_physics.shapes
                body.position = startpos
                physics.space.reindex_shape(shape[0])

                magnitude = 200
                force = (force[0]*magnitude, force[1]*magnitude)
                r = (-5*scale, 0)
                body.apply_force(force, r)
                self.removebulletlist.append(self.bulletlist[0])
                Clock.schedule_once(lambda x:self.remove_bullet(self.removebulletlist[0]), 7)
                del self.bulletlist[0]

                self.force = []
            self.touchbox = []

            if len(self.bulletlist) == 0:
                self.bulletlist = ['bullet', 'bullet2', 'bullet3', 'bullet4', 'bullet5', 'bullet6', 'bullet7', 'bullet8',
        'bullet9', 'bullet10', 'bullet11', 'bullet12', 'bullet13', 'bullet14', 'bullet15',
        'bullet16', 'bullet17', 'bullet18', 'bullet19', 'bullet20', 'bullet21', 'bullet22',
        'bullet23', 'bullet24', 'bullet25', 'bullet26', 'bullet27', 'bullet28', 'bullet29', 'bullet30']

    def remove_bullet(self, currentbullet):
        entities = self.gameworld.entities
        physics = self.gameworld.system_manager['cymunk_physics']
        if not self.cancelcall:
            entity = entities[ent[currentbullet]]
            body = entity.cymunk_physics.body
            body.reset_forces()
            body.velocity = (0, 0)
            shape = entity.cymunk_physics.shapes
            body.position = (2000 *scale, 3250 *scale)
            physics.space.reindex_shape(shape[0])

            del self.removebulletlist[0]

    def on_touch_move(self, touch):
        if self.level == 9:
            self.touchbox.append(touch.y)

    def update(self, dt):
        entities = self.gameworld.entities
        for x in range(len(self.objs)):
            entity = entities[ent[self.objs[x]]]
            body = entity.cymunk_physics.body
            force = (0, -80000)
            body.reset_forces()
            body.apply_force(force)

        if self.level == 3:
            for x in range(len(self.objs2)):
                entity = entities[ent[self.objs2[x]]]
                body = entity.cymunk_physics.body
                if self.magicforce:
                    force = (10000, -10000)
                else:
                    force = (0, -10000)
                body.reset_forces()
                body.apply_force(force)
            for x in range(len(self.objs3)):
                entity = entities[ent[self.objs3[x]]]
                body = entity.cymunk_physics.body
                force = (0, -5000)
                body.reset_forces()
                body.apply_force(force)

        elif self.level == 4:
            for x in range(len(self.objs2)):
                entity = entities[ent[self.objs2[x]]]
                body = entity.cymunk_physics.body
                force = (0, -500)
                body.reset_forces()
                body.apply_force(force)

        elif self.level == 6:
            for x in range(len(self.objs2)):
                entity = entities[ent[self.objs2[x]]]
                body = entity.cymunk_physics.body
                force = (0, -7000)
                body.reset_forces()
                body.apply_force(force)

        elif self.level == 7:
            for x in range(len(self.objs3)):
                entity = entities[ent[self.objs3[x]]]
                body = entity.cymunk_physics.body
                force = (0, -30000)
                body.reset_forces()
                body.apply_force(force)

        elif self.level == 8:
            for x in range(len(self.objs2)):
                entity = entities[ent[self.objs2[x]]]
                body = entity.cymunk_physics.body
                force = (0, -10000)
                body.reset_forces()
                body.apply_force(force)

        elif self.level == 9:
            for x in range(len(self.objs2)):
                entity = entities[ent[self.objs2[x]]]
                body = entity.cymunk_physics.body
                force = (0, -5000)
                r = (0, -51*scale)
                body.reset_forces()
                body.apply_force(force, r)

        elif self.level == 10:
            for x in range(len(self.objs2)):
                entity = entities[ent[self.objs2[x]]]
                body = entity.cymunk_physics.body
                force = (0, -7000)
                body.reset_forces()
                body.apply_force(force)

            for x in range(len(self.objs3)):
                entity = entities[ent[self.objs3[x]]]
                body = entity.cymunk_physics.body
                force = (0, -3000)
                body.reset_forces()
                body.apply_force(force)

Factory.register('BoundarySystem', cls=BoundarySystem)

class RotationSystem(GameSystem):
    def __init__(self, **kwargs):
        super(RotationSystem, self).__init__(**kwargs)
        self.level = ''
        self.camerastate = 'up'
        self.caught = False
        self.pushed = False
        self.count = 0

    def systemspeed(self, speed):
        self.update_time = speed

    def update(self, dt):
        if self.level == 2:
            entities = self.gameworld.entities
            entity = entities[ent['camera']]
            body = entity.cymunk_physics.body
            if not self.caught:
                if self.camerastate == 'down':
                    body.reset_forces()
                    force = (0, -3000)
                    r = (334*scale, -5*scale)
                    body.apply_force(force, r)


                else:
                    body.reset_forces()
                    force = (0, 3000)
                    r = (334*scale, -5*scale)
                    body.apply_force(force, r)


            else:
                if self.camerastate == 'down':
                    body.reset_forces()
                    force = (0, -20000)
                    r = (334*scale, -5*scale)
                    body.apply_force(force, r)


                else:
                    body.reset_forces()
                    force = (0, 20000)
                    r = (334*scale, -5*scale)
                    body.apply_force(force, r)


        elif self.level == 'howto':
            entities = self.gameworld.entities
            if self.count < 7:
                entity = entities[ent['showhand']]
                imagerender = entity.rotate_color_scale_renderertop
                imagerender.texture_key = 'showhand'
                imagescale = entity.scale
                imagescale.s = 1*scale
                imagepos = entity.position
                imagepos.x -= (6*scale)
                self.count += 1

            elif self.count >= 4 and self.count < 16:
                entity = entities[ent['showhand']]
                imagerender = entity.rotate_color_scale_renderertop
                imagerender.texture_key = 'showhand2'
                entity = entities[ent['showhand']]
                showhandpos = entity.position
                entity = entities[ent['showball']]
                showballpos = entity.position
                showhandpos.y += (10*scale)
                showballpos.y += (10*scale)
                self.count += 1
            elif self.count >= 16 and self.count < 20:
                entity = entities[ent['showhand']]
                imagerender = entity.rotate_color_scale_renderertop
                imagerender.texture_key = 'showhand'
                imagescale = entity.scale
                imagescale.s = 1.2*scale

                entity = entities[ent['showhand']]
                showhandpos = entity.position
                entity = entities[ent['showball']]
                showballpos = entity.position
                showhandpos.x += (10*scale)
                showballpos.y += (10*scale)

                self.count += 1

            elif self.count >= 20 and self.count < 35:
                entity = entities[ent['showball']]
                showballpos = entity.position
                showballpos.y += (10*scale)
                self.count += 1

            elif self.count == 35:
                entity = entities[ent['showhand']]
                showhandscale = entity.scale
                showhandscale = 1*scale
                showhandpos = entity.position

                entity = entities[ent['showball']]
                showballpos = entity.position

                showhandpos.pos = ((515*scale)+wscale, (30 *scale)+hscale)
                showballpos.pos = ((469*scale)+wscale, (50 *scale)+hscale)

                self.count = 0


        elif self.level == 'howtospecial':
            entities = self.gameworld.entities
            if self.count < 7:
                entity = entities[ent['showhand']]
                imagerender = entity.rotate_color_scale_renderertop
                imagerender.texture_key = 'showhand'
                imagescale = entity.scale
                imagescale.s = 1*scale
                imagepos = entity.position
                imagepos.x -= (6*scale)
                self.count += 1

            elif self.count >= 4 and self.count < 16:
                entity = entities[ent['showhand']]
                imagerender = entity.rotate_color_scale_renderertop
                imagerender.texture_key = 'showhand2'
                entity = entities[ent['showhand']]
                showhandpos = entity.position
                entity = entities[ent['showball']]
                showballpos = entity.position
                showhandpos.y += (10*scale)
                showballpos.y += (10*scale)
                self.count += 1
            elif self.count >= 16 and self.count < 20:
                entity = entities[ent['showhand']]
                imagerender = entity.rotate_color_scale_renderertop
                imagerender.texture_key = 'showhand'
                imagescale = entity.scale
                imagescale.s = 1.2*scale

                entity = entities[ent['showhand']]
                showhandpos = entity.position
                entity = entities[ent['showball']]
                showballpos = entity.position
                showhandpos.x += (10*scale)
                showballpos.y += (10*scale)

                self.count += 1

            elif self.count >= 20 and self.count < 35:
                entity = entities[ent['showball']]
                showballpos = entity.position
                showballpos.y += (10*scale)
                self.count += 1

            elif self.count == 35:
                entity = entities[ent['showhand']]
                showhandscale = entity.scale
                showhandscale = 1*scale
                showhandpos = entity.position

                entity = entities[ent['showball']]
                showballpos = entity.position


                self.paused = True
                objs = ['showhand', 'showball', 'msg']
                for x in range(len(objs)):
                    entity = entities[ent[objs[x]]]
                    imagepos = entity.position
                    imagepos.pos = (2629 *scale, 2882 *scale)
                sysbox = []

                self.count = 0


        elif self.level == 8:
            entities = self.gameworld.entities
            entity = entities[ent['Ynormal']]
            body = entity.cymunk_physics.body
            for x in range(20):
                force = (0, 10000)
                r = (-4*scale, 40*scale)
                body.apply_force(force,r)

                force = (0, 10000)
                r = (4*scale, 40*scale)
                body.apply_force(force,r)

Factory.register('RotationSystem', cls=RotationSystem)

class Blank(Widget):
    def __init__(self, pos, size):
        super(Blank, self).__init__()
        with self.canvas:
            Color(0, 0, 0)
            Rectangle(pos=pos, size=size)

class TestGame(Widget):

    def __init__(self, **kwargs):
        super(TestGame, self).__init__(**kwargs)
        self.gameworld.init_gameworld(
            ['position', 'rotate', 'color', 'scale', 'cymunk_physics', 'cymunk_touch',
             rendertop, render, render2, 'camera1',
             'particles', 'emitters', 'particle_renderer',
             'boundary', 'rotation', ],
            callback=self.init_game)


        self.consnum = 0
        self.more_force = False

        self.startguide = False
        self.hitside = False
        self.hittop = False
        self.touchedside = False
        self.touchedtop = False
        self.fintime = 0
        self.rank = 0
        self.ranklist = []
        self.cur_ranks = []

        self.nametimer = False
        self.dovibrate = True
        self.soundvol = 0
        self.tracktimer = None
        self.currenttrack = None
        self.voltimer = None
        self.setentry = False

        self.assetsloaded = False

        self.btnlist = []

        self.lvprog = []

        self.turned = False
        self.successbtn = False
        self.level = 0
        self.won = False

        self.samelevels = [1,2,3]
        self.samelevels2 = [5,6]
        self.timer = False
        self.count = 0

        self.camerastate = 'down'
        self.caught = False

        self.magictimer = False

        self.basket = False

        self.five = False

        self.remsupport = False

        self.strikerpushed = False

        self.ball = ['cannonball', 'cannonball2', 'cannonball3', 'cannonball4']

        self.cantime = None
        self.cantime2 = None
        self.cantime3 = None
        self.cantime4 = None
        self.cantime5 = None

        self.successcheckcalled = False

        self.sresetstriker = False
        self.sresetstriker2 = False
        self.sresetstriker3 = False
        self.sresetstriker4 = False
        self.scannoncannon2 = False
        self.scannoncannon3 = False
        self.scannoncannon4 = False
        self.scannon2cannon3 = False
        self.scannon2cannon4 = False
        self.scannon3cannon4 = False
        self.successchecktimer = False

        self.scgoal = False
        self.scgoal2 = False
        self.scgoal3 = False
        self.scgoal4 = False

        self.fired = False

        self.cur_str = None

        self.ntimer = False
        self.ncount = 0
        self.double = False
        self.doubletm = False

        self.ngoalkey = False
        self.ngoal2key = False
        self.opengate = True
        self.opengate2 = True
        self.tentimer = False


        self.attnum = 0
        self.attobj = [
            ['missle1', 'missle2', 'missle3', 'missle4', 'missle5',
        'missle6', 'missle7',],
            ['bigmissle1', 'bigmissle2', 'bigmissle3', 'bigmissle4', 'bigmissle5',
        'bigmissle6', 'bigmissle7',],
            ['omissle1', 'omissle2', 'omissle3', 'omissle4', 'omissle5',
        'omissle6', 'omissle7',]

        ]
        self.type = [0,1,2]
        self.ser = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,19,20,21,22,
                    23,24,25,26,27,28,29,30]

        self.attgenctrl = False
        self.lv8slit = False

        self.lv9done = False
        self.lv10breached = False

        self.lv10downforce = False

        self.attgencount = 0

        self.slamrollpos = 3500
        self.slamrolly = 800
        self.intropart = False

    def init_game(self):
        self.setup_states()
        self.set_state()
        self.load_emitter()
        self.loadintro()
        self.startgame()
        self.add_widget(Blank(*blank_rect1))
        self.add_widget(Blank(*blank_rect2))
        self.collision_callbacks()
        self.load_data()
        self.load_music()

#intro
    # @run_on_ui_thread
    # def android_setflag(self, *args):
    #     PythonActivity.mActivity.getWindow().addFlags(Param.FLAG_KEEP_SCREEN_ON)


    def loadintro(self):
        # self.android_setflag()

        init_entity = self.gameworld.init_entity
        tex = [('title', render),
                ('start', render),
                ('play', render),
                ('howto', render),

                ('settings', render),
                ('extras', render),
                ('one', render),
                ('two', render),
                ('three', render),
                ('four', render),
                ('five', render),
                ('six', render),
                ('seven', render),
                ('eight', render),
                ('nine', render),
                ('ten',render),
                ('showball', render),
                ('showhand',rendertop),
                ('vibrate', render),
                ('on', render),
                ('sound', render),
                ('sliderglow', render),
                ('slambtnimg', render),
                ('backbutton', render),
                ('hbound', render2),
                ('blank', render), #blankdecor
                 ]

        for x in range(len(tex)):
            pos = (2629 *scale, 4000 *scale)
            areabound = {tex[x][1]: {'texture': tex[x][0], 'render': True},
                  'position': pos, 'rotate': 0, 'scale': 1*scale, 'color': (255,255,255,255),
                         'emitters': []}
            component_order = ['position', 'rotate', 'scale', 'color', tex[x][1], 'emitters']
            areabound = init_entity(areabound, component_order)

        btnid = ['start', 'play', 'howto', 'settings', 'extras',
                 '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                 'btnrestart', 'btnmainmenu', 'btnlevels',
                 'slamtable',
                 'backbutton']

        btnsize = [(151, 41), (151, 41), (151, 41), (151, 41), (151, 41), (151, 41),
                   (75, 75), (75, 75), (75, 75), (75, 75), (75, 75), (75, 75), (75, 75), (75, 75), (75, 75), (75, 75),
                   (120, 120), (120, 120), (120, 120),
                   (550, 295),
                   (80, 80)]

        for x in range(len(btnid)):
            self.btn = Button(size_hint=(None, None),
                              text = btnid[x],
                              size=(btnsize[x][0]*scale, btnsize[x][1]*scale),
                              pos=(1083 *scale, 624 *scale),
                              opacity=0)

            self.add_widget(self.btn)
            self.btnlist.append(self.btn)

        self.extrabtn = Button(size_hint=(None, None),
                          text = 'slamtablex',
                          size=(550*scale, 295*scale),
                          pos=(1083 *scale, 1000 *scale),
                          opacity=0)
        self.add_widget(self.extrabtn)

        self.slamreset = Button(size_hint=(None, None),
                          text = 'slam++',
                          size=(50*scale, 50*scale),
                          pos=(1083 *scale, 1000 *scale),
                          opacity=0)
        self.add_widget(self.slamreset)

        self.closebutton = Button(size_hint=(None, None),
                          text = 'x',
                          size=(60*scale, 60*scale),
                          pos=(1083 *scale, 1000 *scale),
                          opacity=0)
        self.add_widget(self.closebutton)


        self.togglebtn = Button(size_hint=(None, None),
                                  text = '',
                                  size= (50*scale, 50*scale),
                                  pos=(1083 *scale, 624 *scale),
                                  opacity=0)



        self.slder = Slider(size_hint=(None, None),
                            max = 1.0,
                            value = .8,
                            size= (475*scale, 50*scale),
                            pos=(1083 *scale, 624 *scale),
                            opacity=1)


        self.add_widget(self.togglebtn)
        self.add_widget(self.slder)


        self.watchvidbtn = Button(size_hint=(None, None),
                          text = 'watchvidbtn',
                          size=(360*scale, 41*scale),
                          pos=(1083 *scale, 1000 *scale),
                          opacity=0)
        self.add_widget(self.watchvidbtn)


        for x in self.btnlist[1:5]:
            x.bind(on_release = self.introclear)



        self.funcs = [self.lv1 ,self.lv2, self.lv3, self.lv4, self.lv5,
                      self.lv6, self.lv7, self.lv8, self.lv9, self.lv10]
        numberbtns = self.btnlist[5:15]
        for x in range(len(numberbtns)):
            numberbtns[x].bind(on_release = self.funcs[x])

        self.btnlist[0].bind(on_release = self.powerload)
        self.btnlist[1].bind(on_release = self.levelselect)
        self.btnlist[2].bind(on_release = self.howtoshow)
        self.btnlist[3].bind(on_release = self.settings)
        self.btnlist[4].bind(on_release = self.extras)

        # self.btnlist[-2].bind(on_release = self.slam)
        self.btnlist[-1].bind(on_release = self.backtomain)

        self.btnlist[15].bind(on_release = self.roundrestart)
        self.btnlist[16].bind(on_release = self.tomainmenu)
        self.btnlist[17].bind(on_release = self.levelselectmenu)

        self.extrabtn.bind(on_release = self.slam)
        self.slamreset.bind(on_release = self.slamresetmini)
        self.closebutton.bind(on_release = self.closecall)

        self.togglebtn.bind(on_press= self.changevibrate)
        self.slder.bind(value = self.changesound)




        self.btnlist[0].bind(on_press = lambda x:self.pressing('start'))
        self.btnlist[1].bind(on_press = lambda x:self.pressing('play'))
        self.btnlist[2].bind(on_press = lambda x:self.pressing('howto'))
        self.btnlist[3].bind(on_press = lambda x:self.pressing('settings'))
        self.btnlist[4].bind(on_press = lambda x:self.pressing('extras'))
        self.btnlist[-1].bind(on_press = lambda x:self.pressing('backbutton'))

        self.btnlist[5].bind(on_press = lambda x:self.pressing('one'))
        self.btnlist[6].bind(on_press = lambda x:self.pressing('two'))
        self.btnlist[7].bind(on_press = lambda x:self.pressing('three'))
        self.btnlist[8].bind(on_press = lambda x:self.pressing('four'))
        self.btnlist[9].bind(on_press = lambda x:self.pressing('five'))
        self.btnlist[10].bind(on_press = lambda x:self.pressing('six'))
        self.btnlist[11].bind(on_press = lambda x:self.pressing('seven'))
        self.btnlist[12].bind(on_press = lambda x:self.pressing('eight'))
        self.btnlist[13].bind(on_press = lambda x:self.pressing('nine'))
        self.btnlist[14].bind(on_press = lambda x:self.pressing('ten'))

        self.btnlist[15].bind(on_press = lambda x:self.pressing('restartbtn'))
        self.btnlist[16].bind(on_press = lambda x:self.pressing('mainmenubtn'))
        self.btnlist[17].bind(on_press = lambda x:self.pressing('stageselectbtn'))

        self.slamreset.bind(on_press = lambda x:self.pressing('slamre'))
        self.watchvidbtn.bind(on_press = lambda x:self.pressing('watchvideo'))

        self.store = DictStore('store.dat')
        if 'info' in self.store.keys():
            self.dovibrate = self.store.get('info')['vibrate']
            self.soundvol = self.store.get('info')['sound']

        else:
            self.store.put('info',
                           vibrate=True,
                           sound = .8,)
            self.soundvol = .8

        self.store2 = DictStore('store2.dat')
        if 'lvprog' in self.store2.keys():
            self.lvprog = self.store2.get('lvprog')['progress']

        else:
            self.store2.put('lvprog',
                           progress=['one', 'lock', 'lock', 'lock',
                                     'lock', 'lock', 'lock', 'lock',
                                     'lock', 'lockred'],
                           )

        self.store3 = DictStore('store3.dat')
        if 'rankingsys' in self.store3.keys():
            self.ranklist = self.store3.get('rankingsys')['ranks']


        else:
            self.store3.put('rankingsys',
                           ranks=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0,]
                           )

    def closecall(self, touch):
        self.rollbackassets()
        self.reset()
        self.levelselect()
        self.closebutton.pos = (1083 *scale, 1000 *scale)

    def changevibrate(self, change):
        entities = self.gameworld.entities
        if self.dovibrate:
            self.dovibrate = False
            self.store.put('info',
                           vibrate=self.dovibrate,
                           sound = self.soundvol,)

            entity = entities[ent['vibratec']]
            rend = entity.rotate_color_scale_renderer
            rend.texture_key = 'off'

        else:
            self.dovibrate = True
            self.store.put('info',
                           vibrate=self.dovibrate,
                           sound = self.soundvol,)

            entity = entities[ent['vibratec']]
            rend = entity.rotate_color_scale_renderer
            rend.texture_key = 'on'

    def changesound(self, change, value):
        value = "%.2f" % value
        value = float(value)

        if self.setentry:
            self.soundvol = value
            if self.voltimer:
                self.voltimer.cancel()
            self.voltimer = Clock.schedule_once(self.newsound, .1)
        else:
            self.setentry = True

    def newsound(self, once):
        sound_manager = self.gameworld.sound_manager
        sound_manager.sound_volume = self.soundvol
        sound_manager.stop('track1')
        sound_manager.play_loop('track1', float(self.soundvol))

    def load_music(self):
        sound_manager = self.gameworld.sound_manager

        sound_manager.cutoff = 0.10

        track = 'track1'
        address = get_asset_path(track + '.ogg')
        track_name = sound_manager.load_sound(track, address, track_count = 1)

        track2 = 'track2'
        address = get_asset_path(track2 + '.ogg')
        track_name2 = sound_manager.load_sound(track2, address, track_count = 1)

        sound_manager.play_loop('track1', float(self.soundvol))
        sound_manager.cutoff = 0.1

    def tomainmenu(self, touch):
        # self.rollbackassets()
        self.controlscreenoff()
        self.reset()
        self.intro()

    def roundrestart(self, touch):
        # self.rollbackassets()
        self.funcs = [self.lv1 ,self.lv2, self.lv3, self.lv4, self.lv5,
                      self.lv6, self.lv7, self.lv8, self.lv9, self.lv10]
        currentlv = self.level-1
        self.controlscreenoff()
        self.reset()
        self.funcs[currentlv]()

    def levelselectmenu(self, touch):
        # self.rollbackassets()
        self.controlscreenoff()
        self.reset()
        self.levelselect()

    def startgame(self, *args):
        Clock.schedule_once(self.startgame0, .2)
        Clock.schedule_once(self.startgame1, 2)

    def startgame0(self, once):
        entities = self.gameworld.entities
        objs = ['blankdecor']
        pos = [((475 *scale)+wscale, (293.5 *scale)+hscale)]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            imagepos = entity.position
            imagepos.pos = pos[x]

        emitter_system = self.gameworld.system_manager['emitters']
        emitter_system.add_effect(ent['blankdecor'], 'introeffects')
        self.intropart = True

    def startgame1(self, once):
        entities = self.gameworld.entities
        objs = ['title', 'start']
        pos = [((475 *scale)+wscale, (450 *scale)+hscale),
               ((475 *scale)+wscale, (240 *scale)+hscale)]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            imagepos = entity.position
            imagepos.pos = pos[x]

        self.btnlist[0].pos = (((475-75.5) *scale)+wscale, ((240-20.5) *scale)+hscale)

    def rollbackstartgame(self, *args):
        entities = self.gameworld.entities
        objs = ['title', 'start']
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            imagepos = entity.position
            imagepos.pos = (2629 *scale, 4000 *scale)
        self.btnlist[0].pos = (1083 *scale, 624 *scale)

    def intro(self, *args):
        entities = self.gameworld.entities

        touch = self.gameworld.system_manager['cymunk_touch']
        ignore = range(1, 85)
        touch.ignore_groups = ignore

        sound_manager = self.gameworld.sound_manager
        if self.currenttrack == 'track2':
            sound_manager.stop('track2')
            sound_manager.play_loop('track1', float(self.soundvol))

        objs = ['title', 'play', 'howto', 'settings', 'extras']
        pos = [((475*scale)+wscale, (450 *scale)+hscale), ((475*scale)+wscale, (300 *scale)+hscale), ((475*scale)+wscale, (240 *scale)+hscale),
               ((475*scale)+wscale, (180 *scale)+hscale), ((475*scale)+wscale, (120 *scale)+hscale)]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            imagepos = entity.position
            imagepos.pos = pos[x]


        pos = [((475-75.5), (300-20.5)), ((475-75.5), (240-20.5)),
               ((475-75.5), (180-20.5)), ((475-75.5), (120-20.5)),]
        btns = self.btnlist[1:5]

        for x in range(len(btns)):
            btns[x].pos = ((pos[x][0]*scale)+wscale, (pos[x][1]*scale)+hscale)


        emitter_system = self.ids.emitter
        if not self.intropart:
            emitter_system.add_effect(ent['blankdecor'], 'introeffects')
            self.intropart = True

        if self.currenttrack == 1:
            sound_manager = self.gameworld.sound_manager
            sound_manager.stop_direct(self.currenttrack)
            sound_manager.play_direct_loop(0, float(self.soundvol))
            self.currenttrack = 0

    def introclear(self, touch):
        entities = self.gameworld.entities
        objs = ['title', 'play', 'howto', 'settings', 'extras']
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            imagepos = entity.position
            imagepos.pos = (2629 *scale, 2882 *scale)
        btns = self.btnlist[1:5]
        btns.append(self.btnlist[18])

        for x in range(5):
            btns[x].pos = (1083 *scale, 624 *scale)
        btns = []

    def levelselect(self, *args):
        self.level = 'levelselect'
        entities = self.gameworld.entities
        emitter_system = self.ids.emitter
        sound_manager = self.gameworld.sound_manager


        if self.currenttrack == 'track2':
            sound_manager.stop('track2')
            sound_manager.play_loop('track1', float(self.soundvol))


        if not self.intropart:
            emitter_system.add_effect(ent['blankdecor'], 'introeffects')
            self.intropart = True

        self.lvprog = self.store2.get('lvprog')['progress']
        progcheck = self.lvprog

        entity = entities[ent['backbutton']]
        imagepos = entity.position
        imagepos.pos = ((70*scale)+wscale, (530*scale)+hscale)

        self.btnlist[-1].pos = (((70-40)*scale)+wscale, ((530-40)*scale)+hscale)


        objs = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',]
        pos = [(158, 391), (317, 391), (475, 391), (633, 391), (792, 391),
               (158, 196), (317, 196), (475, 196), (633, 196), (792, 196),]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            renderimg = entity.rotate_color_scale_renderer
            renderimg.texture_key = self.lvprog[x]
            imagepos = entity.position
            imagepos.pos = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)


        btns = self.btnlist[5:15]
        pos = [(158-37.5, 391-37.5), (317-37.5, 391-37.5), (475-37.5, 391-37.5), (633-37.5, 391-37.5), (792-37.5, 391-37.5),
               (158-37.5, 196-37.5), (317-37.5, 196-37.5), (475-37.5, 196-37.5), (633-37.5, 196-37.5), (792-37.5, 196-37.5),]

        for x in self.lvprog:
            if x == 'lock':
                pass
            elif x == 'lockred':
                pass
            else:
                num = self.lvprog.index(x)
                btns[num].pos = ((pos[num][0]*scale)+wscale, (pos[num][1]*scale)+hscale)


        self.ranklist = self.store3.get('rankingsys')['ranks']


        objs = []
        for idx, val in enumerate(self.ranklist):
            if val == 0:
                obj = 'nostar'+str(idx)
                objs.append(obj)
            elif val == 1:
                obj = 'onestar'+str(idx)
                objs.append(obj)
            elif val == 2:
                obj = 'twostar'+str(idx)
                objs.append(obj)
            else:
                obj = 'threestar'+str(idx)
                objs.append(obj)


        delidx = []
        for idx, val in enumerate(self.lvprog):
            if val == 'lock' or val == 'lockred':
                delidx.append(idx)




        if len(delidx) != 0:
            del objs[delidx[0]-1:delidx[-1]]

        pos = [(158, 315), (317, 315), (475, 315), (633, 315), (792, 315),
               (158, 120), (317, 120), (475, 120), (633, 120), (792, 120),]

        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            imagepos = entity.position
            imagepos.pos = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)
        self.cur_ranks = objs


    def rollbacklevelselect(self, *args):
        entities = self.gameworld.entities

        objs = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
                'backbutton', 'watchvideo', 'watchvideoimg']

        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            imagepos = entity.position
            imagepos.pos = (2629 *scale, 2882 *scale)

        for x in range(len(self.cur_ranks)):
            entity = entities[ent[self.cur_ranks[x]]]
            imagepos = entity.position
            imagepos.pos = (2629 *scale, 2882 *scale)

        btns = self.btnlist[5:15]
        btns.append(self.btnlist[-1])
        for x in range(len(btns)):
            btns[x].pos = (1083 *scale, 624 *scale)

        self.watchvidbtn.pos = (1083 *scale, 624 *scale)

        if self.intropart:
            emitter_system = self.ids.emitter
            emitter_system.remove_effect(ent['blankdecor'], 0)
            self.intropart = False

    def rollbacklevelselect2(self, *args):
        entities = self.gameworld.entities

        objs = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
                'backbutton', 'watchvideo', 'watchvideoimg']

        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            imagepos = entity.position
            imagepos.pos = (2629 *scale, 2882 *scale)

        for x in range(len(self.cur_ranks)):
            entity = entities[ent[self.cur_ranks[x]]]
            imagepos = entity.position
            imagepos.pos = (2629 *scale, 2882 *scale)

        btns = self.btnlist[5:15]
        btns.append(self.btnlist[-1])
        for x in range(len(btns)):
            btns[x].pos = (1083 *scale, 624 *scale)

        self.watchvidbtn.pos = (1083 *scale, 624 *scale)

        # if self.intropart:
        #     emitter_system = self.ids.emitter
        #     emitter_system.remove_effect(ent['blankdecor'], 0)
        #     self.intropart = False

    def howtoshow(self, touch):
        rotation = self.gameworld.system_manager['rotation']
        rotation.level = 'howto'
        rotation.paused = False
        rotation.count = 0
        rotation.systemspeed(.2)
        sysbox.append('rotation')

        self.level = 'howto'
        entities = self.gameworld.entities
        objs = ['showhand', 'showball', 'hbound',
                'backbutton', 'msg', 'msgrankhigher']
        pos = [(515, 30), (469, 50), (475, 293.5),
               (70, 530), (200, 210), (700, 520)]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            imagepos = entity.position
            imagepos.pos = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)

        self.btnlist[-1].pos = (((70-40)*scale)+wscale, ((530-40)*scale)+hscale)

        if self.intropart:
            emitter_system = self.ids.emitter
            emitter_system.remove_effect(ent['blankdecor'], 0)
            self.intropart = False

    def rollbackhowtoshow(self, *args):
        rotation = self.gameworld.system_manager['rotation']
        rotation.level = 'howto'
        rotation.paused = True
        sysbox = []

        entities = self.gameworld.entities
        objs = ['showhand', 'showball', 'hbound',
                'backbutton', 'msg', 'msgrankhigher']
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            imagepos = entity.position
            imagepos.pos = (2629 *scale, 2882 *scale)

        self.btnlist[-1].pos = (1083 *scale, 624 *scale)

    def settings(self, touch):
        self.level = 'settings'
        entities = self.gameworld.entities

        objs = ['vibrate', 'sound', 'backbutton', 'vibratec', 'sliderglow',]
        pos = [(237.5, 400), (237.5, 200), (70, 530), (712.5, 400),
               (705, 198)]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            imagepos = entity.position
            imagepos.pos = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)

        self.btnlist[-1].pos = (((70-40)*scale)+wscale, ((530-40)*scale)+hscale)
        self.togglebtn.pos = (((712.5-25) *scale)+wscale, ((400-25) *scale)+hscale)
        self.slder.pos = (((712.5-250)*scale)+wscale, ((200-25) *scale)+hscale)

        if self.dovibrate:
            entity = entities[ent['vibratec']]
            rend = entity.rotate_color_scale_renderer
            rend.texture_key = 'on'
        else:
            entity = entities[ent['vibratec']]
            rend = entity.rotate_color_scale_renderer
            rend.texture_key = 'off'

        self.slder.value = self.soundvol

    def rollbacksettings(self, *args):
        entities = self.gameworld.entities

        objs = ['vibrate', 'sound', 'backbutton', 'vibratec', 'sliderglow',]

        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            imagepos = entity.position
            imagepos.pos = (2629*scale, 2882*scale)

        self.btnlist[-1].pos = (1083 *scale, 624 *scale)
        self.togglebtn.pos = (1083 *scale, 624 *scale)
        self.slder.pos = (1083 *scale, 624 *scale)

        if self.dovibrate:
            self.store.put('info',
                           vibrate=True,
                           sound = self.slder.value,)


        elif not self.dovibrate:
            self.store.put('info',
                           vibrate=False,
                           sound = self.slder.value,)

    def extras(self, *args):
        self.level = 'extras'
        entities = self.gameworld.entities

        objs = ['slamtable',
                'backbutton']
        pos = [(475, 287),
               (70, 530)]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            imagepos = entity.position
            imagepos.pos = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)


        self.btnlist[-1].pos = (((70-40)*scale)+wscale, ((530-40)*scale)+hscale)
        self.extrabtn.pos = (((475-275)*scale)+wscale, ((293.5-147.5)*scale)+hscale)

    def rollbackextras(self, *args):
        entities = self.gameworld.entities

        objs = ['slamtable',
                'backbutton']

        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            imagepos = entity.position
            imagepos.pos = (2629 *scale, 2882 *scale)


        self.btnlist[-1].pos = (1083 *scale, 624 *scale)
        self.extrabtn.pos = (1083 *scale, 624 *scale)

    def backtomain(self, touch):
        if self.level == 'levelselect':
            self.rollbacklevelselect2()
            self.intro()

        elif self.level == 'howto':
            self.rollbackhowtoshow()
            self.intro()

        elif self.level == 'settings':
            self.rollbacksettings()
            self.intro()
            self.store.put('info',
               vibrate=self.dovibrate,
               sound = self.soundvol,)
            self.setentry = False

        elif self.level == 'extras':
            self.rollbackextras()
            self.intro()

        elif self.level == 'slam':
            self.rollbackslam()
            self.intro()

        elif self.level == 'customize':
            self.rollbackcustomize()
            self.intro()

        else:
            self.rollbackassets()
            self.intro()

    def pressing(self, image):
        entities = self.gameworld.entities
        entity = entities[ent[image]]
        imagerender = entity.rotate_color_scale_renderer
        imagerender.texture_key = image+'pressed'
        Clock.schedule_once(lambda x:self.releasing(image), .2)

    def releasing(self, image):
        entities = self.gameworld.entities
        entity = entities[ent[image]]
        imagerender = entity.rotate_color_scale_renderer
        imagerender.texture_key = image

    def load_emitter(self):
        emitter_system = self.ids.emitter


        data = {'number_of_particles': 300,
                'texture': 'strp1',
                'paused': False,
                'pos_variance': (475*scale, 293.5*scale),

                'radial_acceleration': 200,
                'tangential_acceleration': 15,
                'rotate_per_second': 15,
                'start_scale': .1*scale,
                'end_scale': 1.5*scale,
                'start_color_variance': (255 ,255, 255, 0),
                'end_color_variance': (255 ,255, 255, 255),
               }
        eff_id = emitter_system.load_effect_from_data(data, 'introeffects')

        data = {'number_of_particles': 25,
                'texture': 'shadow',
                'paused': False,
                'pos_variance': (0, 0),
                'emitter_type': 0,
                'gravity': (0, 0),
                'start_scale': .5*scale,
                'end_scale': .5*scale,
                'start_color': (255, 255, 255, 255),
                'end_color': (255, 0, 0, 200),
                'life_span': 1.0,
               }
        eff_id = emitter_system.load_effect_from_data(data, 'strikereffects')




        data = {'number_of_particles': 25,
                'texture': 'shadow2',
                'paused': False,
                'pos_variance': (0, 0),
                'emitter_type': 0,
                'gravity': (0, 0),
                'start_scale': .5*scale,
                'end_scale': .5*scale,
                'start_color': (255, 255, 255, 255),
                'end_color': (0, 0, 255, 200),
                'life_span': 1.0,
               }
        eff_id = emitter_system.load_effect_from_data(data, 'striker2effects')


        data = {'number_of_particles': 20,
                'texture': 'telepart',
                'paused': False,
                'pos_variance': (13*scale, 73*scale),
                'start_color': (255, 255, 255, 255),
                'end_color': (255, 255, 255, 0),
                'speed_variance': 50,
                'start_scale': 1*scale,
                'end_scale': 1*scale,

               }
        eff_id = emitter_system.load_effect_from_data(data, 'teleporteffects')

        data = {'number_of_particles': 20,
                'texture': 'telepart',
                'paused': False,
                'pos_variance': (13*scale, 73*scale),
                'start_color': (255, 255, 255, 255),
                'end_color': (255, 255, 255, 0),
                'speed_variance': 50,
                'start_scale': 1*scale,
                'end_scale': 1*scale,

               }
        eff_id = emitter_system.load_effect_from_data(data, 'teleport2effects')


        data = {'number_of_particles': 10,
                'texture': 'cnshadow',
                'paused': False,
                'pos_variance': (0, 0),
                'emitter_type': 0,
                'gravity': (0, 0),
                'start_scale': .5*scale,
                'end_scale': .5*scale,
                'start_color': (255, 255, 255, 255),
                'end_color': (255, 255, 255, 128),
                'life_span': .5,
               }
        eff_id = emitter_system.load_effect_from_data(data, 'cneffects')

        data = {'number_of_particles': 10,
                'texture': 'cnshadow2',
                'paused': False,
                'pos_variance': (0, 0),
                'emitter_type': 0,
                'gravity': (0, 0),
                'start_scale': .5*scale,
                'end_scale': .5*scale,
                'start_color': (255, 255, 255, 255),
                'end_color': (255, 255, 255, 128),
                'life_span': .5,
               }
        eff_id = emitter_system.load_effect_from_data(data, 'cneffects2')

        data = {'number_of_particles': 10,
                'texture': 'cnshadow3',
                'paused': False,
                'pos_variance': (0, 0),
                'emitter_type': 0,
                'gravity': (0, 0),
                'start_scale': .5*scale,
                'end_scale': .5*scale,
                'start_color': (255, 255, 255, 255),
                'end_color': (255, 255, 255, 128),
                'life_span': .5,
               }
        eff_id = emitter_system.load_effect_from_data(data, 'cneffects3')

        data = {'number_of_particles': 10,
                'texture': 'cnshadow4',
                'paused': False,
                'pos_variance': (0, 0),
                'emitter_type': 0,
                'gravity': (0, 0),
                'start_scale': .5*scale,
                'end_scale': .5*scale,
                'start_color': (255, 255, 255, 255),
                'end_color': (255, 255, 255, 128),
                'life_span': .5,
               }
        eff_id = emitter_system.load_effect_from_data(data, 'cneffects4')


        data = {'number_of_particles': 10,
                'texture': 'mpar',
                'paused': False,
                'pos_offset': (-30*scale, 0*scale),
                'start_color': (255, 255, 255, 255),
                'end_color': (255, 255, 0, 0),

                'start_scale': 1*scale,
                'end_scale': 2*scale,
                'life_span': .5,

               }
        eff_id = emitter_system.load_effect_from_data(data, 'meffects')

        data = {'number_of_particles': 10,
                'texture': 'bpar',
                'paused': False,
                'pos_offset': (-45*scale, 0*scale),
                'start_color': (255, 255, 255, 255),
                'end_color': (255, 255, 255, 0),

                'start_scale': 1*scale,
                'end_scale': 2*scale,
                'life_span': .5,

               }
        eff_id = emitter_system.load_effect_from_data(data, 'beffects')

        data = {'number_of_particles': 10,
                'texture': 'opar',
                'paused': False,
                'pos_offset': (0*scale, 23*scale),
                'start_color': (255, 255, 255, 255),
                'end_color': (255, 255, 255, 0),

                'start_scale': 1*scale,
                'end_scale': .1*scale,
                'life_span': .5,

               }
        eff_id = emitter_system.load_effect_from_data(data, 'oeffects')

        data = {'number_of_particles': 25,
                'texture': 'whitepar',
                'paused': False,
                'pos_offset': (0, 0),
                'start_color': (255, 255, 255, 255),
                'end_color': (255, 255, 255, 0),

                'start_scale': 1*scale,
                'end_scale': 1*scale,
                'life_span': 1,

               }
        eff_id = emitter_system.load_effect_from_data(data, 'whiteeffects')

        data = {'number_of_particles': 300,
                'texture': 'star',
                'paused': False,
                'pos_variance': (475*scale, 293.5*scale),
                'tangential_acceleration': 15,
                'radial_acceleration': 200,
                'rotate_per_second': 15,
                'start_scale': .1*scale,
                'end_scale': 1.5*scale,
                'start_color_variance': (255 ,255, 255, 0),
                'end_color_variance': (255 ,255, 255, 255),
               }
        eff_id = emitter_system.load_effect_from_data(data, 'successeffects')



        data = {'number_of_particles': 50,
                'texture': 'failp',
                'paused': False,
                'pos_variance': (475*scale, 293.5*scale),
                'start_color': (255, 255, 255, 255),
                'end_color': (255, 255, 255, 0),
                'start_scale': 1*scale,
                'end_scale': .1*scale,
                'life_span': 2.0,

               }
        eff_id = emitter_system.load_effect_from_data(data, 'failureeffects')

    def powerload(self, touch):
        self.rollbackstartgame()
        self.load_assets()
        self.intro()

    def load_data(self):

        self.obnor = [
            ['striker', (2702 *scale, 2060 *scale), render, 2000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 16.5 *scale, 'mass': 200, 'offset': (0, 0)},
              'collision_type': 4, 'group': 3, 'elasticity': .8, 'friction': 1, 'shape_type': 'circle'}]
             ],
            ['goal', (2702 *scale, 2000 *scale), render, 2000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 16.5 *scale, 'mass': 200, 'offset': (0, 0)},
              'collision_type': 6, 'group': 0, 'elasticity': .5, 'friction': 1, 'shape_type': 'circle'}]
             ],

        #slit 1,2,3
            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 950 *scale, 'height': 10 *scale, 'mass': 0,},
              'collision_type': 7, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],
            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 950 *scale, 'height': 10 *scale, 'mass': 0,},
              'collision_type': 12, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],
            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 10 *scale, 'height': 587 *scale, 'mass': 0,},
              'collision_type': 7, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

        #barrier 1,2,3,4
            ['blank', (475 *scale, 2265 *scale), render, 1000,
            [{'shape_info': {'width': 950 *scale, 'height': 363 *scale, 'mass': 0,},
              'collision_type': 8, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],
            ['blank', (475 *scale, -1735 *scale), render,
            [{'shape_info': {'width': 950 *scale, 'height': 363 *scale, 'mass': 0,},
              'collision_type': 9, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],
            ['blank', (475 *scale, 2265 *scale), render, 1000,
            [{'shape_info': {'width': 750 *scale, 'height': 587 *scale, 'mass': 0,},
              'collision_type': 8, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],
            ['blank', (475 *scale, -1735 *scale), render, 1000,
            [{'shape_info': {'width': 750 *scale, 'height': 587 *scale, 'mass': 0,},
              'collision_type': 9, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

        #bar1
            ['blank', (475 *scale, 2265 *scale), render, 1000,
            [{'shape_info': {'width': 950 *scale, 'height': 363 *scale, 'mass': 0,},
              'collision_type': 55, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],
        #bar1
            ['blank', (475 *scale, -1735 *scale), render, 1000,
            [{'shape_info': {'width': 950 *scale, 'height': 363 *scale, 'mass': 0,},
              'collision_type': 56, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],
        #bot1
            ['blank', (475 *scale, 2265 *scale), render, 1000,
            [{'shape_info': {'width': 950 *scale, 'height': 363 *scale, 'mass': 0,},
              'collision_type': 57, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],
        #bot2
            ['blank', (475 *scale, -1735 *scale), render, 1000,
            [{'shape_info': {'width': 950 *scale, 'height': 363 *scale, 'mass': 0,},
              'collision_type': 58, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

        #cameraholder
            ['cameraholder', (1947*scale, 2326.5*scale), render2, 1000,
            [{'shape_info': {'width': 63 *scale, 'height': 34 *scale, 'mass': 0,},
              'collision_type': 11, 'group': 2, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

        #magicball
            ['magicball', (2603*scale, 2060 *scale), render, 2000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 16.5 *scale, 'mass': 100, 'offset': (0, 0)},
              'collision_type': 13, 'group': 0, 'elasticity': .8, 'friction': 1, 'shape_type': 'circle'}]
             ],
            ['blank', (2498*scale, 1181 *scale), render2, 1000,
            [{'shape_info': {'width': 60 *scale, 'height': 100 *scale, 'mass': 0,},
              'collision_type': 15, 'group': 0, 'elasticity': .5, 'friction': 0, 'shape_type': 'box'}]
             ],
            ['blank', (3558 *scale, 991 *scale), render2, 1000,
            [{'shape_info': {'width': 60 *scale, 'height': 100 *scale, 'mass': 0,},
              'collision_type': 15, 'group': 0, 'elasticity': .5, 'friction': 0, 'shape_type': 'box'}]
             ],

        #ropestopper
            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 86 *scale, 'height': 20 *scale, 'mass': 0,},
              'collision_type': 5, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
            ],

        #basketedges
            ['blank', (3409*scale, 1410 *scale), render, 1000,
            [{'shape_info': {'width': 4 *scale, 'height': 4 *scale, 'mass': 0,},
              'collision_type': 3, 'group': 4, 'elasticity': .3, 'friction': 1, 'shape_type': 'box'}]
             ],
            ['blank', (3454 *scale, 1410 *scale), render, 1000,
            [{'shape_info': {'width': 4 *scale, 'height': 4 *scale, 'mass': 0,},
              'collision_type': 3, 'group': 4, 'elasticity': .3, 'friction': 1, 'shape_type': 'box'}]
             ],

        #basket
            ['blank', (2647*scale, 2000*scale), render2, 1000,
            [{'shape_info': {'width': 7 *scale, 'height': 20 *scale, 'mass': 0,},
              'collision_type': 3, 'group': 4, 'elasticity': .5, 'friction': 1, 'shape_type': 'box'}]
             ],

            ['blank', (2647*scale, 2000*scale), render2, 1000,
            [{'shape_info': {'width': 54 *scale, 'height': 6 *scale, 'mass': 0,},
              'collision_type': 3, 'group': 4, 'elasticity': .5, 'friction': 1, 'shape_type': 'box'}]
             ],

            ['blank', (2647*scale, 2000*scale), render2, 1000,
            [{'shape_info': {'width': 13 *scale, 'height': 73 *scale, 'mass': 0,},
              'collision_type': 3, 'group': 4, 'elasticity': .5, 'friction': 1, 'shape_type': 'box'}]
             ],

            ['blank', (2647*scale, 2000*scale), render2, 1000,
            [{'shape_info': {'width': 8 *scale, 'height': 8 *scale, 'mass': 0,},
              'collision_type': 3, 'group': 4, 'elasticity': .5, 'friction': 1, 'shape_type': 'box'}]
             ],

            ['blank', (2647*scale, 2000*scale), render2, 1000,
            [{'shape_info': {'width': 8 *scale, 'height': 4 *scale, 'mass': 0,},
              'collision_type': 3, 'group': 4, 'elasticity': .5, 'friction': 1, 'shape_type': 'box'}]
             ],

        #lv5screen
            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 10 *scale, 'height': 49 *scale, 'mass': 0,},
              'collision_type': 3, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 10 *scale, 'height': 49 *scale, 'mass': 0,},
              'collision_type': 3, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 10 *scale, 'height': 140 *scale, 'mass': 0,},
              'collision_type': 3, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 10 *scale, 'height': 140 *scale, 'mass': 0,},
              'collision_type': 3, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 624 *scale, 'height': 10 *scale, 'mass': 0,},
              'collision_type': 3, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 30 *scale, 'height': 127 *scale, 'mass': 0,},
              'collision_type': 27, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 613 *scale, 'height': 30 *scale, 'mass': 0,},
              'collision_type': 27, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 25 *scale, 'height': 15 *scale, 'mass': 0,},
              'collision_type': 3, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 25 *scale, 'height': 15 *scale, 'mass': 0,},
              'collision_type': 3, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 25 *scale, 'height': 15 *scale, 'mass': 0,},
              'collision_type': 3, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 25 *scale, 'height': 15 *scale, 'mass': 0,},
              'collision_type': 3, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

        #lv6screen
            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 10 *scale, 'height': 250 *scale, 'mass': 0,},
              'collision_type': 3, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 475 *scale, 'height': 10 *scale, 'mass': 0,},
              'collision_type': 3, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 30 *scale, 'height': 240 *scale, 'mass': 0,},
              'collision_type': 27, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 465 *scale, 'height': 30 *scale, 'mass': 0,},
              'collision_type': 27, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

        #topbar
            ['topbar', (-2134*scale, 2468.5*scale), rendertop, 2000,
            [{'shape_info': {'width': 150 *scale, 'height': 20 *scale, 'mass': 1500,},
              'collision_type': 24, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

        #leftweight
            ['blank', (-2209*scale, 2458.5*scale), rendertop, 1000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 30*scale, 'mass': 200, 'offset': (0, 0)},
              'collision_type': 25, 'group': 1, 'elasticity': .1, 'friction': .1, 'shape_type': 'circle'}]
             ],
        #rightweight
            ['blank', (-2059*scale, 2458.5*scale), rendertop, 1000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 30*scale, 'mass': 1000, 'offset': (0, 0)},
              'collision_type': 25, 'group': 1, 'elasticity': .1, 'friction': .1, 'shape_type': 'circle'}]
             ],

        #cartwheel
            ['cartwheel', (3040*scale, 2045*scale), render, 1000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 10.5 *scale, 'mass': 100, 'offset': (0, 0)},
              'collision_type': 26, 'group': 0, 'elasticity': 1, 'friction': .1, 'shape_type': 'circle'}]
             ],
        #supporter
            ['blank', (3040*scale, 1800*scale), render, 1000,
            [{'shape_info': {'width': 30*scale, 'height': 5*scale, 'mass': 0,},
              'collision_type': 28, 'group': 3, 'elasticity': .5, 'friction': 1, 'shape_type': 'box'}]
             ],
        #supporter
            ['blank', (3040*scale, 1800*scale), render, 1000,
            [{'shape_info': {'width': 30*scale, 'height': 5*scale, 'mass': 0,},
              'collision_type': 28, 'group': 3, 'elasticity': .5, 'friction': 1, 'shape_type': 'box'}]
             ],


        #cannonballs
            ['cnone', (3070*scale, 1800*scale), render, 10000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 15 *scale, 'mass': 100, 'offset': (0, 0)},
              'collision_type': 33, 'group': 0, 'elasticity': .8, 'friction': 1, 'shape_type': 'circle'}]
             ],

            ['cntwo', (3120*scale, 1800*scale), render, 10000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 15 *scale, 'mass': 100, 'offset': (0, 0)},
              'collision_type': 34, 'group': 0, 'elasticity': .8, 'friction': 1, 'shape_type': 'circle'}]
             ],

            ['cnthree', (3170 *scale, 1800 *scale), render, 10000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 15 *scale, 'mass': 100, 'offset': (0, 0)},
              'collision_type': 35, 'group': 0, 'elasticity': .8, 'friction': 1, 'shape_type': 'circle'}]
             ],

            ['cnfour', (3220 *scale, 1800 *scale), render, 10000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 15 *scale, 'mass': 100, 'offset': (0, 0)},
              'collision_type': 36, 'group': 0, 'elasticity': .8, 'friction': 1, 'shape_type': 'circle'}]
             ],

        #cgoal
            ['goal', (3070*scale, 1700*scale), render, 2000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 16.5 *scale, 'mass': 100, 'offset': (0, 0)},
              'collision_type': 38, 'group': 0, 'elasticity': .5, 'friction': 1, 'shape_type': 'circle'}]
             ],

            ['goal', (3120*scale, 1700*scale), render, 2000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 16.5 *scale, 'mass': 100, 'offset': (0, 0)},
              'collision_type': 39, 'group': 0, 'elasticity': .5, 'friction': 1, 'shape_type': 'circle'}]
             ],

            ['goal', (3170 *scale, 1700 *scale), render, 2000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 16.5 *scale, 'mass': 100, 'offset': (0, 0)},
              'collision_type': 40, 'group': 0, 'elasticity': .5, 'friction': 1, 'shape_type': 'circle'}]
             ],

            ['goal', (3220 *scale, 1700 *scale), render, 2000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 16.5 *scale, 'mass': 100, 'offset': (0, 0)},
              'collision_type': 41, 'group': 0, 'elasticity': .5, 'friction': 1, 'shape_type': 'circle'}]
             ],

        #cannon
            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 50 *scale, 'height': 8 *scale, 'mass': 0,},
              'collision_type': 21, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 50 *scale, 'height': 8 *scale, 'mass': 0,},
              'collision_type': 21, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

        #sensor
            ['blank', (3150 *scale, 1800 *scale), render, 1000,
            [{'shape_info': {'width': 5 *scale, 'height': 5 *scale, 'mass': 0,},
              'collision_type': 37, 'group': 3, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

        #teleblocker
            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 70 *scale, 'height': 146 *scale, 'mass': 0,},
              'collision_type': 29, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

        #lv8screen
            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 10 *scale, 'height': 92 *scale, 'mass': 0,},
              'collision_type': 3, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 371 *scale, 'height': 10 *scale, 'mass': 0,},
              'collision_type': 3, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 10 *scale, 'height': 173 *scale, 'mass': 0,},
              'collision_type': 3, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 92 *scale, 'height': 10 *scale, 'mass': 0,},
              'collision_type': 3, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 30 * scale, 'height': 82 *scale, 'mass': 0,},
              'collision_type': 27, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 351 *scale, 'height': 50 *scale, 'mass': 0,},
              'collision_type': 27, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 28 *scale, 'height': 153 *scale, 'mass': 0,},
              'collision_type': 27, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 82 *scale, 'height': 28 *scale, 'mass': 0,},
              'collision_type': 27, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

        #spstriker
            ['striker', (3170 *scale, 1600 *scale), render, 2000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 16.5 *scale, 'mass': 200, 'offset': (0, 0)},
              'collision_type': 42, 'group': 4, 'elasticity': .1, 'friction': 1, 'shape_type': 'circle'}]
             ],
        #spstriker
            ['striker2', (3220 *scale, 1600 *scale), render, 2000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 16.5 *scale, 'mass': 200, 'offset': (0, 0)},
              'collision_type': 43, 'group': 4, 'elasticity': .1, 'friction': 1, 'shape_type': 'circle'}]
             ],
            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 12 *scale, 'height': 36 *scale, 'mass': 0,},
              'collision_type': 47, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],
            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 12 *scale, 'height': 36 *scale, 'mass': 0,},
              'collision_type': 47, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],


        #Ysensor
            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 150 *scale, 'height': 5 *scale, 'mass': 0,},
              'collision_type': 44, 'group': 0, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],


        #buttonblocker
            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 36 *scale, 'height': 60 *scale, 'mass': 0,},
              'collision_type': 46, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 36 *scale, 'height': 60 *scale, 'mass': 0,},
              'collision_type': 46, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

            ['blank', (-2134*scale, 2343.5*scale), render, 1000,
            [{'shape_info': {'width': 36 *scale, 'height': 60 *scale, 'mass': 0,},
              'collision_type': 46, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

        #button
            ['button1', (-1000*scale, 2343.5*scale), render2, 1000,
            [{'shape_info': {'width': 12 *scale, 'height': 24 *scale, 'mass': 50,},
              'collision_type': 45, 'group': 0, 'elasticity': .1, 'friction': 1, 'shape_type': 'box'}]
             ],

            ['blank', (-1000*scale, 2380.5*scale), render2, 1000,
            [{'shape_info': {'width': 36 *scale, 'height': 10 *scale, 'mass': 50,},
              'collision_type': 45, 'group': 0, 'elasticity': .1, 'friction': 1, 'shape_type': 'box'}]
             ],

        #start, end point
            ['blank', (1700 *scale, 3104 *scale), render, 1000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 10 *scale, 'mass': 50, 'offset': (0, 0)},
              'collision_type': 48, 'group': 2, 'elasticity': 1, 'friction': 1, 'shape_type': 'circle'}]
             ],
            ['spot', (1700 *scale, 3340 *scale), render, 1000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 10 *scale, 'mass': 50, 'offset': (0, 0)},
              'collision_type': 48, 'group': 2, 'elasticity': 1, 'friction': 1, 'shape_type': 'circle'}]
             ],


        #gunarch
            ['gunarch', (1700 *scale, 3100 *scale), render2, 1000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 50 *scale, 'mass': 0, 'offset': (0, 0)},
              'collision_type': 52, 'group': 2, 'elasticity': 1, 'friction': 1, 'shape_type': 'circle'}]
             ],

        #gunstopper
            ['blank', (1700 *scale, 3160 *scale), rendertop, 1000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 10 *scale, 'mass': 10, 'offset': (0, 0)},
              'collision_type': 82, 'group': 1, 'elasticity': 1, 'friction': .1, 'shape_type': 'circle'}]
             ],

        #ngoal
            ['goal', (2000*scale, 1700*scale), render, 1000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 16.5 *scale, 'mass': 100, 'offset': (0, 0)},
              'collision_type': 61, 'group': 0, 'elasticity': 1, 'friction': 1, 'shape_type': 'circle'}]
             ],

            ['goal', (2050*scale, 1700*scale), render, 1000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 16.5 *scale, 'mass': 100, 'offset': (0, 0)},
              'collision_type': 54, 'group': 0, 'elasticity': 1, 'friction': 1, 'shape_type': 'circle'}]
             ],



        #arenahor
            ['blank', (3000*scale, 2500*scale), render, 1000,
            [{'shape_info': {'width': 70 *scale, 'height': 10 *scale, 'mass': 0,},
              'collision_type': 60, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],
            ['blank', (3000*scale, 2500*scale), render, 1000,
            [{'shape_info': {'width': 70 *scale, 'height': 10 *scale, 'mass': 0,},
              'collision_type': 60, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],
            ['blank', (3000*scale, 2500*scale), render, 1000,
            [{'shape_info': {'width': 70 *scale, 'height': 10 *scale, 'mass': 0,},
              'collision_type': 60, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],
            ['blank', (3000*scale, 2500*scale), render, 1000,
            [{'shape_info': {'width': 70 *scale, 'height': 10 *scale, 'mass': 0,},
              'collision_type': 60, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],
            ['blank', (3000*scale, 2500*scale), render, 1000,
            [{'shape_info': {'width': 120 *scale, 'height': 10 *scale, 'mass': 0,},
              'collision_type': 60, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],
            ['blank', (3000*scale, 2500*scale), render, 1000,
            [{'shape_info': {'width': 10 *scale, 'height': 147 *scale, 'mass': 0,},
              'collision_type': 3, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],
            ['blank', (3000*scale, 2500*scale), render, 1000,
            [{'shape_info': {'width': 10 *scale, 'height': 70 *scale, 'mass': 0,},
              'collision_type': 3, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]
             ],

        #fireball
            ['fireball', (1200 *scale, 300 *scale), render, 12000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 16.5 *scale, 'mass': 150, 'offset': (0, 0)},
              'collision_type': 51, 'group': 0, 'elasticity': 1, 'friction': 1, 'shape_type': 'circle'}]
             ],

            ['fireball', (1302 *scale, 300 *scale), render, 12000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 16.5 *scale, 'mass': 150, 'offset': (0, 0)},
              'collision_type': 51, 'group': 0, 'elasticity': 1, 'friction': 1, 'shape_type': 'circle'}]
             ],
        #white
            ['white', (3400 *scale, 293 *scale), render, 5000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 11.5 *scale, 'mass': 150, 'offset': (0, 0)},
              'collision_type': 65, 'group': 0, 'elasticity': 1, 'friction': 1, 'shape_type': 'circle'}]
             ],
        #green
            ['green', (3530 *scale, 293 *scale), render, 5000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 11.5 *scale, 'mass': 300, 'offset': (0, 0)},
              'collision_type': 66, 'group': 0, 'elasticity': 1, 'friction': 1, 'shape_type': 'circle'}]
             ],
        #yellow
            ['yellow', (3560 *scale, 293 *scale), render, 5000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 11.5 *scale, 'mass': 300, 'offset': (0, 0)},
              'collision_type': 67, 'group': 0, 'elasticity': 1, 'friction': 1, 'shape_type': 'circle'}]
             ],
        #brown
            ['brown', (3590 *scale, 293 *scale), render, 5000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 11.5 *scale, 'mass': 300, 'offset': (0, 0)},
              'collision_type': 68, 'group': 0, 'elasticity': 1, 'friction': 1, 'shape_type': 'circle'}]
             ],
        #blue
            ['blue', (3620 *scale, 293 *scale), render, 5000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 11.5 *scale, 'mass': 300, 'offset': (0, 0)},
              'collision_type': 69, 'group': 0, 'elasticity': 1, 'friction': 1, 'shape_type': 'circle'}]
             ],
        #pink
            ['pink', (3650 *scale, 293 *scale), render, 5000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 11.5 *scale, 'mass': 300, 'offset': (0, 0)},
              'collision_type': 70, 'group': 0, 'elasticity': 1, 'friction': 1, 'shape_type': 'circle'}]
             ],
        #black
            ['black', (3680 *scale, 293 *scale), render, 5000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 11.5 *scale, 'mass': 300, 'offset': (0, 0)},
              'collision_type': 71, 'group': 0, 'elasticity': 1, 'friction': 1, 'shape_type': 'circle'}]
             ],

        #cue
            ['blank', (3400 *scale, 293 *scale), render2, 5000,
            [{'shape_info': {'inner_radius': 0, 'outer_radius': 30 *scale, 'mass': 150, 'offset': (0, 0)},
              'collision_type': 81, 'group': 0, 'elasticity': 1, 'friction': 1, 'shape_type': 'circle'}]
             ],


        ]

        self.objspoly = [
             ['camera', (2282*scale, 2321.5*scale), rendertop, 200, 4000,
             [{'shape_info': {'mass': 10, 'vertices': [(-265*scale, 52*scale), (-352*scale, 52*scale), (-352*scale, 9*scale), (-264*scale, 9*scale)], 'offset': (0, 0)},
               'collision_type': 11, 'group': 2, 'elasticity': .1, 'friction': 1.0, 'shape_type': 'poly'},
              {'shape_info': {'mass': 10, 'vertices': [(-264*scale, 15*scale), (301*scale, -92*scale), (301*scale, 86*scale), (-264*scale, 37*scale)], 'offset': (0, 0)},
               'collision_type': 10, 'group': 2, 'elasticity': .1, 'friction': 1.0, 'shape_type': 'poly'},

              ]],

             ['cart', (3000*scale, 2060 *scale), render, 200, 2000,
             [{'shape_info': {'mass': 10, 'vertices': [(-39*scale, 20*scale), (-38*scale, 17*scale), (-32*scale, 18*scale), (-32*scale, 21*scale)], 'offset': (0, 0)},
               'collision_type': 26, 'group': 0, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},
              {'shape_info': {'mass': 10, 'vertices': [(-32*scale, 21*scale), (-32*scale, 18*scale), (-27*scale, 17*scale), (-26*scale, 20*scale)], 'offset': (0, 0)},
               'collision_type': 26, 'group': 0, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},
              {'shape_info': {'mass': 10, 'vertices': [(-26*scale, 20*scale), (-27*scale, 17*scale), (-24*scale, 12*scale), (-21*scale, 13*scale)], 'offset': (0, 0)},
               'collision_type': 26, 'group': 0, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},
              {'shape_info': {'mass': 10, 'vertices': [(-25*scale, 10*scale), (-19*scale, -3*scale), (-19*scale, 12*scale),], 'offset': (0, 0)},
               'collision_type': 26, 'group': 0, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},
              {'shape_info': {'mass': 10, 'vertices': [(-18*scale, -2*scale), (-14*scale, -11*scale), (26*scale, -13*scale), (28*scale, -2*scale)], 'offset': (0, 0)},
               'collision_type': 26, 'group': 0, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},
              {'shape_info': {'mass': 10, 'vertices': [(36*scale, 22*scale), (28*scale, -2*scale), (30*scale, -2*scale), (39*scale, 23*scale)], 'offset': (0, 0)},
               'collision_type': 26, 'group': 0, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},
              {'shape_info': {'mass': 10, 'vertices': [(-10*scale, -12*scale), (-4*scale, -23*scale), (0*scale, -13*scale),], 'offset': (0, 0)},
               'collision_type': 26, 'group': 0, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},

              ]],


             ['batholder', (3347 *scale, 2027 *scale), render2, 0, 2000,
             [{'shape_info': {'mass': 0, 'vertices': [(0*scale, 36*scale), (-9*scale, 26*scale), (-17*scale, -35*scale), (17*scale, -35*scale), (9*scale, 26*scale)], 'offset': (0, 0)},
               'collision_type': 3, 'group': 2, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},

              ]],

             ['bat', (3347 *scale, 2065 *scale), render, 560, 2000,
             [{'shape_info': {'mass': 280, 'vertices': [(-72*scale, 9*scale), (-77*scale, 0*scale), (-72*scale, -9*scale), (45*scale, -5*scale), (45*scale, 5*scale)], 'offset': (0, 0)},
               'collision_type': 20, 'group': 3, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},
              {'shape_info': {'mass': 280, 'vertices': [(45*scale, 0*scale), (49*scale, -11*scale), (60*scale, -15*scale), (71*scale, -11*scale), (75*scale, 0*scale),
                                                        (71*scale, 11*scale), (60*scale, 15*scale), (49*scale, 11*scale)], 'offset': (0, 0)},
               'collision_type': 20, 'group': 3, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},

              ]],


        #Ynormal
             ['Y', (4500 *scale, 2027*scale), render2, 400, 2000,
             [{'shape_info': {'mass': 100, 'vertices': [(-53*scale, 94*scale), (-60*scale, 87*scale), (-7*scale, 41*scale), (-3*scale, 51*scale)], 'offset': (0, 0)},
               'collision_type': 19, 'group': 1, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},
              {'shape_info': {'mass': 100, 'vertices': [(2*scale, 51*scale), (4*scale, 40*scale), (59*scale, 87*scale), (52*scale, 94*scale)], 'offset': (0, 0)},
               'collision_type': 19, 'group': 1, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},
              {'shape_info': {'mass': 100, 'vertices': [(-1*scale, 50*scale), (-5*scale, 40*scale), (4*scale, 40*scale)], 'offset': (0, 0)},
               'collision_type': 19, 'group': 1, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},
              {'shape_info': {'mass': 100, 'vertices': [(-5*scale, 40*scale), (-5*scale, -14*scale), (5*scale, -14*scale), (4*scale, 40*scale)], 'offset': (0, 0)},
               'collision_type': 19, 'group': 1, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},

              ]],


             ['gun', (1700 *scale, 3140 *scale), rendertop, 250, 2000,
             [{'shape_info': {'mass': 100, 'vertices': [(-15*scale, 53*scale), (-15*scale, -46*scale), (-11*scale, -46*scale), (-11*scale, 53*scale)], 'offset': (0, 0)},
               'collision_type': 59, 'group': 2, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},
              {'shape_info': {'mass': 100, 'vertices': [(11*scale, 53*scale), (10*scale, -46*scale), (14*scale, -46*scale), (14*scale, 53*scale)], 'offset': (0, 0)},
               'collision_type': 59, 'group': 2, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},
              {'shape_info': {'mass': 100, 'vertices': [(-15*scale, -46*scale), (-15*scale, -48*scale), (0*scale, -53*scale), (14*scale, -48*scale), (14*scale, -46*scale)], 'offset': (0, 0)},
               'collision_type': 59, 'group': 2, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},

              ]],

             ['ropehook2', (1291 *scale, 300 *scale), render2, 80, 12000,
             [{'shape_info': {'mass': 20, 'vertices': [(-12*scale, 3*scale), (-13*scale, 2*scale), (-14*scale, 0*scale), (-13*scale, -1*scale), (-11*scale, -2*scale), ], 'offset': (0, 0)},
               'collision_type': 50, 'group': 0, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},
              {'shape_info': {'mass': 20, 'vertices': [(-10*scale, 2*scale), (-10*scale, -1*scale), (-9*scale, 0*scale)], 'offset': (0, 0)},
               'collision_type': 50, 'group': 0, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},
              {'shape_info': {'mass': 20, 'vertices': [(12*scale, 3*scale), (13*scale, 2*scale), (14*scale, 0*scale), (13*scale, -1*scale),(11*scale, -2*scale), ], 'offset': (0, 0)},
               'collision_type': 50, 'group': 0, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},
              {'shape_info': {'mass': 20, 'vertices': [(10*scale, 2*scale), (10*scale, -1*scale), (9*scale, 0*scale)], 'offset': (0, 0)},
               'collision_type': 50, 'group': 1, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},

              ]],

             ['ropecomp', (1227 *scale, 300 *scale), render2, 80, 12000,
             [{'shape_info': {'mass': 50, 'vertices': [(-9*scale, 1*scale), (-10*scale, 0*scale), (-9*scale, -2*scale), (-7*scale, -3*scale),
                        (-5*scale, -2*scale), (-5*scale, 0*scale), (-6*scale, 1*scale), (-7*scale, 2*scale)], 'offset': (0, 0)},
               'collision_type': 50, 'group': 0, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},
              {'shape_info': {'mass': 50, 'vertices': [(7*scale, 2*scale), (7*scale, -3*scale), (9*scale, -3*scale), (9*scale, 2*scale),], 'offset': (0, 0)},
               'collision_type': 50, 'group': 0, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},
              ]],
             ['ropecomp', (1239 *scale, 300 *scale), render2, 80, 12000,
             [{'shape_info': {'mass': 50, 'vertices': [(-9*scale, 1*scale), (-10*scale, 0*scale), (-9*scale, -2*scale), (-7*scale, -3*scale),
                        (-5*scale, -2*scale), (-5*scale, 0*scale), (-6*scale, 1*scale), (-7*scale, 2*scale)], 'offset': (0, 0)},
               'collision_type': 50, 'group': 0, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},
              {'shape_info': {'mass': 50, 'vertices': [(7*scale, 2*scale), (7*scale, -3*scale), (9*scale, -3*scale), (9*scale, 2*scale),], 'offset': (0, 0)},
               'collision_type': 50, 'group': 0, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},
              ]],
             ['ropecomp', (1251 *scale, 300 *scale), render2, 80, 12000,
             [{'shape_info': {'mass': 50, 'vertices': [(-9*scale, 1*scale), (-10*scale, 0*scale), (-9*scale, -2*scale), (-7*scale, -3*scale),
                        (-5*scale, -2*scale), (-5*scale, 0*scale), (-6*scale, 1*scale), (-7*scale, 2*scale)], 'offset': (0, 0)},
               'collision_type': 50, 'group': 0, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},
              {'shape_info': {'mass': 50, 'vertices': [(7*scale, 2*scale), (7*scale, -3*scale), (9*scale, -3*scale), (9*scale, 2*scale),], 'offset': (0, 0)},
               'collision_type': 50, 'group': 0, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},
              ]],
             ['ropecomp', (1263 *scale, 300 *scale), render2, 80, 12000,
             [{'shape_info': {'mass': 50, 'vertices': [(-9*scale, 1*scale), (-10*scale, 0*scale), (-9*scale, -2*scale), (-7*scale, -3*scale),
                        (-5*scale, -2*scale), (-5*scale, 0*scale), (-6*scale, 1*scale), (-7*scale, 2*scale)], 'offset': (0, 0)},
               'collision_type': 50, 'group': 0, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},
              {'shape_info': {'mass': 50, 'vertices': [(7*scale, 2*scale), (7*scale, -3*scale), (9*scale, -3*scale), (9*scale, 2*scale),], 'offset': (0, 0)},
               'collision_type': 50, 'group': 0, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},

              ]],

             ['ropecomp', (1275 *scale, 300 *scale), render2, 80, 12000,
             [{'shape_info': {'mass': 50, 'vertices': [(-9*scale, 1*scale), (-10*scale, 0*scale), (-9*scale, -2*scale), (-7*scale, -3*scale),
                        (-5*scale, -2*scale), (-5*scale, 0*scale), (-6*scale, 1*scale), (-7*scale, 2*scale)], 'offset': (0, 0)},
               'collision_type': 50, 'group': 0, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},
              {'shape_info': {'mass': 50, 'vertices': [(7*scale, 2*scale), (7*scale, -3*scale), (9*scale, -3*scale), (9*scale, 2*scale),], 'offset': (0, 0)},
               'collision_type': 50, 'group': 0, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},

              ]],

             ['ropehook', (1211 *scale, 300 *scale), render2, 80, 12000,
             [{'shape_info': {'mass': 50, 'vertices': [(-11*scale, 3*scale), (-13*scale, 2*scale), (-14*scale, 0*scale), (-13*scale, -1*scale),
                    (-11*scale, -2*scale), (-9*scale, -1*scale), (-9*scale, 0*scale), (-9*scale, 2*scale)], 'offset': (0, 0)},
               'collision_type': 50, 'group': 0, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},
              {'shape_info': {'mass': 50, 'vertices': [(11*scale, 3*scale), (11*scale, -2*scale), (13*scale, -2*scale), (13*scale, 3*scale)], 'offset': (0, 0)},
               'collision_type': 50, 'group': 1, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},
              ]],




        ]

    def load_assets(self):
        init_entity = self.gameworld.init_entity
        entities = self.gameworld.entities
        physics = self.gameworld.system_manager['cymunk_physics']


        tex = [('timeline', render2),
               ('aaa', render2),
               ('areabound2', render2),
               ('timeline2', render2),
               ('msg', render),

               ('segtex', render2),
               ('segtex', render2),
               ('segtex', render2),
               ('segtex', render2),
               ('screen', rendertop),

               ('basketkit', render2),

               ('lv5screen', rendertop),

               ('lv6screen', rendertop),

               ('cannon', rendertop),

               ('Y', render2),
               ('lv8screen', rendertop),


               ('lv9screen', rendertop),
               ('lv9screen2', rendertop),
               ('ab', render2),
               ('tl', render2),
               ('ab', render2),
               ('tl', render2),
               ('ab', render2),
               ('tl', render2),
               ('ab', render2),
               ('tl', render2),
               ('aaaa', render2),
               ('aaaa', render2),


               ('table', render2),
               ('redimg', render2),
               ('yellowimg', render2),
               ('greenimg', render2),
               ('brownimg', render2),
               ('blueimg', render2),
               ('pinkimg', render2),
               ('blackimg', render2),
               ('slamre', render),
               ('closeimg', rendertop),
               ('name1', render2),
               ('name2', render2),
               ('name3', render2),
               ('name4', render2),
               ('name5', render2),
               ('name6', render2),
               ('name7', render2),
               ('name8', render2),
               ('name9', render2),
               ('name10', render2),
               ('tankguide', render2),
               ('star1', render),
               ('watchvideo', render),
               ('watchvideoimg', render),
               ('msgrankhigher', render),

               ]



        for x in range(len(tex)):
            pos = (2629 *scale, 4000 *scale)
            areabound = {tex[x][1]: {'texture': tex[x][0], 'render': True},
                  'position': pos, 'rotate': 0, 'scale': 1*scale, 'color': (255,255,255,255),
                         'emitters': []}
            component_order = ['position', 'rotate', 'scale', 'color', tex[x][1], 'emitters']
            areabound = init_entity(areabound, component_order)

        for x in range(10):
            pos = (2629 *scale, 4000 *scale)
            areabound = {render: {'texture': 'rankstar0', 'render': True},
                  'position': pos, 'rotate': 0, 'scale': 1*scale, 'color': (255,255,255,255),
                         }
            component_order = ['position', 'rotate', 'scale', 'color', render]
            areabound = init_entity(areabound, component_order)

        for x in range(10):
            pos = (2629 *scale, 4000 *scale)
            areabound = {render: {'texture': 'rankstar1', 'render': True},
                  'position': pos, 'rotate': 0, 'scale': 1*scale, 'color': (255,255,255,255),
                         }
            component_order = ['position', 'rotate', 'scale', 'color', render]
            areabound = init_entity(areabound, component_order)

        for x in range(10):
            pos = (2629 *scale, 4000 *scale)
            areabound = {render: {'texture': 'rankstar2', 'render': True},
                  'position': pos, 'rotate': 0, 'scale': 1*scale, 'color': (255,255,255,255),
                         }
            component_order = ['position', 'rotate', 'scale', 'color', render]
            areabound = init_entity(areabound, component_order)

        for x in range(10):
            pos = (2629 *scale, 4000 *scale)
            areabound = {render: {'texture': 'rankstar3', 'render': True},
                  'position': pos, 'rotate': 0, 'scale': 1*scale, 'color': (255,255,255,255),
                         }
            component_order = ['position', 'rotate', 'scale', 'color', render]
            areabound = init_entity(areabound, component_order)

        for x in range(len(self.obnor)):

            object_physics = {'main_shape': self.obnor[x][-1][0]['shape_type'], 'velocity': (0, 0), 'position': self.obnor[x][1], 'angle': 0,
                           'angular_velocity': 0, 'vel_limit': self.obnor[x][3], 'ang_vel_limit': radians(200), 'mass': self.obnor[x][-1][0]['shape_info']['mass'],
                           'col_shapes': self.obnor[x][-1]}
            object = {self.obnor[x][2]: {'texture': self.obnor[x][0], 'render': True},
                        'cymunk_physics': object_physics, 'position': self.obnor[x][1],
                        'rotate': 0, 'scale': 1 *scale, 'color': (255, 255, 255, 255),
                      'emitters': []}
            component_order = ['position', 'rotate', 'scale', 'color', 'cymunk_physics', self.obnor[x][2], 'emitters']
            object = init_entity(object, component_order)


    #screen
        size = [(10 *scale, 587 *scale), (10 *scale, 587 *scale),
                (950 *scale, 10 *scale), (950 *scale, 10 *scale),
                (950 *scale, 10 *scale), (950 *scale, 10 *scale),
                (10 *scale, 225*scale), (10*scale, 225*scale),
                (10 *scale, 362*scale), (10*scale, 362*scale),
                (930*scale, 10*scale)]
        col_type = [3,3,3,3,60,60,3,3,83,83,84]
        pos = (-2134*scale, 2343.5*scale)
        tex = ['blank', 'blank', 'blank', 'blank', 'blank', 'blank',
               'screen7', 'screen7', 'screen9', 'screen9', 'screen11'

               ]
        for x in range(len(size)):
            col_shape = [{'shape_info': {'width': size[x][0], 'height': size[x][1], 'mass': 0,},
          'collision_type': col_type[x], 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]

            object_physics = {'main_shape': 'box', 'velocity': (0, 0), 'position': pos, 'angle': 0,
                           'angular_velocity': 0, 'vel_limit': 1000, 'ang_vel_limit': radians(200), 'mass': 0,
                           'col_shapes': col_shape}
            object = {render2: {'texture': 'blank', 'render': True},
                        'cymunk_physics': object_physics, 'position': pos,
                        'rotate': 0, 'scale': 1 *scale, 'color': (255, 255, 255, 255)}
            component_order = ['position', 'rotate', 'scale', 'color', 'cymunk_physics', render2]
            object = init_entity(object, component_order)



    #support x4
        tex = ['blank', 'blank', 'blank', 'blank']
        pos = [(-20, 293.5), (970, 293.5),
               (475, -20), (475, 607)]
        width = [40, 40, 1030, 1030]
        height = [587, 587, 40, 40]


        for x in range(len(pos)):
            col_shape = [{'shape_info': {'width': width[x]*scale, 'height': height[x]*scale, 'mass': 0,},
              'collision_type': 3, 'group': 2, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]

            object_physics = {'main_shape': 'box', 'velocity': (0, 0), 'position': ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale), 'angle': 0,
                           'angular_velocity': 0, 'vel_limit': 1000, 'ang_vel_limit': radians(200), 'mass': 0,
                           'col_shapes': col_shape}
            object = {render: {'texture': tex[x], 'render': True},
                        'cymunk_physics': object_physics, 'position': ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale),
                        'rotate': 0, 'scale': 1 *scale, 'color': (255, 255, 255, 255)}
            component_order = ['position', 'rotate', 'scale', 'color', 'cymunk_physics', render]
            object = init_entity(object, component_order)

    #supportatt
        pos = (-2134*scale, 2343.5*scale)
        width = [1150, 1150, 10, 10]
        height = [10, 10, 787, 787]


        for x in range(4):
            col_shape = [{'shape_info': {'width': width[x]*scale, 'height': height[x]*scale, 'mass': 0,},
              'collision_type': 73, 'group': 2, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]

            object_physics = {'main_shape': 'box', 'velocity': (0, 0), 'position': pos, 'angle': 0,
                           'angular_velocity': 0, 'vel_limit': 1000, 'ang_vel_limit': radians(200), 'mass': 0,
                           'col_shapes': col_shape}
            object = {render: {'texture': 'blank', 'render': True},
                        'cymunk_physics': object_physics, 'position': pos,
                        'rotate': 0, 'scale': 1 *scale, 'color': (255, 255, 255, 255)}
            component_order = ['position', 'rotate', 'scale', 'color', 'cymunk_physics', render]
            object = init_entity(object, component_order)

    #segs
        angle = [0,0,1.6,1.6,.8,-.8,.8,-.8,
                 0,0,1.6,1.6,.8,-.8,.8,-.8,
                 0,0,1.6,1.6,.8,-.8,.8,-.8,
                 0,0,1.6,1.6,.8,-.8,.8,-.8]
        pos = (-2134*scale, 2343.5*scale)
        for x in range(len(angle)):
            col_shape = [{'shape_info': {'width': 31*scale, 'height': 3*scale, 'mass': 0,},
          'collision_type': 5, 'group': 1, 'elasticity': .5, 'friction': 1, 'shape_type': 'box'}]

            object_physics = {'main_shape': 'box', 'velocity': (0, 0), 'position': pos, 'angle': angle[x],
                           'angular_velocity': 0, 'vel_limit': 1000, 'ang_vel_limit': radians(200), 'mass': 0,
                           'col_shapes': col_shape}
            object = {render2: {'texture': 'blank', 'render': True},
                        'cymunk_physics': object_physics, 'position': pos,
                        'rotate': 0, 'scale': 1 *scale, 'color': (255, 255, 255, 255)}
            component_order = ['position', 'rotate', 'scale', 'color', 'cymunk_physics', render2]
            object = init_entity(object, component_order)

    #ropes
        pos = [(2553*scale, 1181 *scale), (2603*scale, 1171 *scale), (2653*scale, 1161 *scale), (2703*scale, 1151 *scale),
               (2753*scale, 1141 *scale), (2803*scale, 1131 *scale), (2853*scale, 1121 *scale), (2903*scale, 1111 *scale),
               (2953*scale, 1101 *scale), (3003*scale, 1091 *scale), (3053*scale, 1081 *scale), (3103*scale, 1071 *scale),
               (3153*scale, 1061 *scale), (3203*scale, 1051 *scale), (3253*scale, 1041 *scale), (3303*scale, 1031 *scale),
               (3353*scale, 1021 *scale), (3403*scale, 1011 *scale), (3453*scale, 1001 *scale), (3503*scale, 991 *scale)]


        for x in range(len(pos)):
            col_shape = [{'shape_info': {'width': 50 *scale, 'height': 10 *scale, 'mass': 150,},
              'collision_type': 14, 'group': 4, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]

            object_physics = {'main_shape': 'box', 'velocity': (0, 0), 'position': pos[x], 'angle': 0,
                           'angular_velocity': 0, 'vel_limit': 1000, 'ang_vel_limit': radians(200), 'mass': 80,
                           'col_shapes': col_shape}
            object = {render2: {'texture': 'rope', 'render': True},
                        'cymunk_physics': object_physics, 'position': pos[x],
                        'rotate': 0, 'scale': 1 *scale, 'color': (255, 255, 255, 255)}
            component_order = ['position', 'rotate', 'scale', 'color', 'cymunk_physics', render2]
            object = init_entity(object, component_order)

    #net
        pos = [(3909 *scale, 1403 *scale), (3909 *scale, 1395 *scale), (3909 *scale, 1387 *scale), (3909 *scale, 1379 *scale), (3909 *scale, 1371 *scale),
               (3954 *scale, 1403 *scale), (3954 *scale, 1395 *scale), (3954 *scale, 1387 *scale), (3954*scale, 1379 *scale), (3954*scale, 1371 *scale) ]

        for x in range(len(pos)):
            col_shape = [{'shape_info': {'width': 2 *scale, 'height': 8 *scale, 'mass': 10,},
          'collision_type': 16, 'group': 4, 'elasticity': .3, 'friction': 1, 'shape_type': 'box'}]

            object_physics = {'main_shape': 'box', 'velocity': (0, 0), 'position': pos[x], 'angle': 0,
                           'angular_velocity': 0, 'vel_limit': 1000, 'ang_vel_limit': radians(200), 'mass': 10,
                           'col_shapes': col_shape}
            object = {rendertop: {'texture': 'net', 'render': True},
                        'cymunk_physics': object_physics, 'position': pos[x],
                        'rotate': 0, 'scale': 1 *scale, 'color': (255, 255, 255, 255)}
            component_order = ['position', 'rotate', 'scale', 'color', 'cymunk_physics', rendertop]
            object = init_entity(object, component_order)

    #nethook
        pos = [(3916.3 *scale, 1408*scale), (3923.9 *scale, 1408*scale), (3931.5 *scale, 1408*scale),
               (3939.1 *scale, 1408*scale), (3946.7 *scale, 1408*scale)]
        col_types = [17, 17, 23, 17, 17]

        for x in range(len(pos)):
            col_shape = [{'shape_info': {'width': 1 *scale, 'height': 2*scale, 'mass': 0,},
              'collision_type': col_types[x], 'group': 4, 'elasticity': .3, 'friction': 1, 'shape_type': 'box'}]

            object_physics = {'main_shape': 'box', 'velocity': (0, 0), 'position': pos[x], 'angle': 0,
                           'angular_velocity': 0, 'vel_limit': 1000, 'ang_vel_limit': radians(200), 'mass': 0,
                           'col_shapes': col_shape}
            object = {render2: {'texture': 'blank', 'render': True},
                        'cymunk_physics': object_physics, 'position': pos[x],
                        'rotate': 0, 'scale': 1 *scale, 'color': (255, 255, 255, 255)}
            component_order = ['position', 'rotate', 'scale', 'color', 'cymunk_physics', render2]
            object = init_entity(object, component_order)

    #innet
        pos = [(3931.5 *scale, 1403*scale), (3931.5 *scale, 1395*scale), (3931.5 *scale, 1387*scale), (3931.5 *scale, 1379*scale), (3931.5 *scale, 1403*scale), (3931.5 *scale, 1395*scale), (3931.5 *scale, 1387*scale), (3931.5 *scale, 1379*scale),
               (3923.9 *scale, 1403*scale), (3923.9 *scale, 1395*scale), (3923.9 *scale, 1387*scale), (3923.9 *scale, 1403*scale), (3923.9 *scale, 1395*scale), (3923.9 *scale, 1387*scale), (3923.9 *scale, 1379*scale), (3923.9 *scale, 1371*scale),
               (3916.3 *scale, 1403*scale), (3916.3 *scale, 1395*scale), (3916.3 *scale, 1403*scale), (3916.3 *scale, 1395*scale), (3916.3 *scale, 1387*scale), (3916.3 *scale, 1379*scale), (3916.3 *scale, 1371*scale), (3916.3 *scale, 1363*scale),
               (3939.1 *scale, 1403*scale), (3939.1 *scale, 1395*scale), (3939.1 *scale, 1387*scale), (3939.1 *scale, 1379*scale), (3939.1 *scale, 1371*scale), (3939.1 *scale, 1403*scale), (3939.1 *scale, 1395*scale), (3939.1 *scale, 1387*scale),
               (3946.7 *scale, 1403*scale), (3946.7 *scale, 1395*scale), (3946.7 *scale, 1387*scale), (3946.7 *scale, 1379*scale), (3946.7 *scale, 1371*scale), (3946.7 *scale, 1363*scale), (3946.7 *scale, 1403*scale), (3946.7 *scale, 1395*scale)]


        for x in range(len(pos)):
            col_shape = [{'shape_info': {'width': 1.5*scale, 'height': 8*scale, 'mass': 4,},
          'collision_type': 17, 'group': 4, 'elasticity': .3, 'friction': 1, 'shape_type': 'box'}]

            object_physics = {'main_shape': 'box', 'velocity': (0, 0), 'position': pos[x], 'angle': 0,
                           'angular_velocity': 0, 'vel_limit': 1000, 'ang_vel_limit': radians(200), 'mass': 4,
                           'col_shapes': col_shape}
            object = {rendertop: {'texture': 'innet', 'render': True},
                        'cymunk_physics': object_physics, 'position': pos[x],
                        'rotate': 0, 'scale': 1 *scale, 'color': (255, 255, 255, 255)}
            component_order = ['position', 'rotate', 'scale', 'color', 'cymunk_physics', rendertop]
            object = init_entity(object, component_order)

    #innethor
        pos = [(3926.5 *scale, 1371*scale), (3931.5 *scale, 1371*scale), (3936.5 *scale, 1371*scale)]

        for x in range(len(pos)):
            col_shape = [{'shape_info': {'width': 5*scale, 'height': 1.5*scale, 'mass': 4,},
              'collision_type': 17, 'group': 4, 'elasticity': .3, 'friction': 1, 'shape_type': 'box'}]

            object_physics = {'main_shape': 'box', 'velocity': (0, 0), 'position': pos[x], 'angle': 0,
                           'angular_velocity': 0, 'vel_limit': 1000, 'ang_vel_limit': radians(200), 'mass': 4,
                           'col_shapes': col_shape}
            object = {rendertop: {'texture': 'innethor', 'render': True},
                        'cymunk_physics': object_physics, 'position': pos[x],
                        'rotate': 0, 'scale': 1 *scale, 'color': (255, 255, 255, 255)}
            component_order = ['position', 'rotate', 'scale', 'color', 'cymunk_physics', rendertop]
            object = init_entity(object, component_order)


    #light
        pos = [(-2134*scale, 2343.5*scale), (-2134*scale, 2343.5*scale)]
        col_type = [18, 53,]
        for x in range(len(pos)):
            shape_dict = {'width': 25 *scale, 'height': 146*scale, 'mass': 0,}
            col_shape = {'shape_type': 'box', 'elasticity': .5, 'collision_type': col_type[x], 'shape_info': shape_dict,
                         'friction': 0.0, 'group': 1}
            col_shapes = [col_shape]
            object_physics = {'main_shape': 'box', 'velocity': (0, 0), 'position': pos[x], 'angle': 0,
                                'angular_velocity': 0, 'vel_limit': 250, 'ang_vel_limit': radians(200),
                                'mass': 0, 'col_shapes': col_shapes}
            vertbound = {render2: {'texture': 'light', 'render': True},
                        'cymunk_physics': object_physics, 'position': pos[x],
                        'rotate': 0, 'scale': 1 *scale, 'color': (255, 255, 255, 255),
                         'emitters': [],}
            component_order = ['position', 'rotate', 'scale', 'color', 'cymunk_physics', render2, 'emitters']
            vertbound = init_entity(vertbound, component_order)

    #bricks
        pos = [(3040*scale, 1944*scale), (3060*scale, 1944*scale), (3080*scale, 1944*scale),
               (3100*scale, 1944*scale), (3120*scale, 1944*scale), (3140*scale, 1944*scale),
               (3160*scale, 1944*scale), (3180*scale, 1944*scale), (3200*scale, 1944*scale),]



        for x in range(len(pos)):
            col_shape = [{'shape_info': {'width': 12*scale, 'height': 8*scale, 'mass': 10,},
          'collision_type': 26, 'group': 0, 'elasticity': .5, 'friction': 1, 'shape_type': 'box'}]

            object_physics = {'main_shape': 'box', 'velocity': (0, 0), 'position': pos[x], 'angle': 0,
                           'angular_velocity': 0, 'vel_limit': 1000, 'ang_vel_limit': radians(200), 'mass': 10,
                           'col_shapes': col_shape}
            object = {render2: {'texture': 'brick', 'render': True},
                        'cymunk_physics': object_physics, 'position': pos[x],
                        'rotate': 0, 'scale': 1 *scale, 'color': (255, 255, 255, 255)}
            component_order = ['position', 'rotate', 'scale', 'color', 'cymunk_physics', render2]
            object = init_entity(object, component_order)


    #Y
        width = [10, 10, 10]
        height = [71, 71, 55]
        pos = (-2134*scale, 2343.5*scale)
        angle = [.87, -.87, 0]

        for x in range(len(width)):

            col_shape = [{'shape_info': {'width': width[x]*scale, 'height': height[x]*scale, 'mass': 0,},
              'collision_type': 3, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]

            object_physics = {'main_shape': 'box', 'velocity': (0, 0), 'position': pos, 'angle': angle[x],
                           'angular_velocity': 0, 'vel_limit': 1000, 'ang_vel_limit': radians(200), 'mass': 0,
                           'col_shapes': col_shape}
            object = {render: {'texture': 'blank', 'render': True},
                        'cymunk_physics': object_physics, 'position': pos,
                        'rotate': 0, 'scale': 1 *scale, 'color': (255, 255, 255, 255)}
            component_order = ['position', 'rotate', 'scale', 'color', 'cymunk_physics', render]
            object = init_entity(object, component_order)



    #bullet30
        pos = (2000 *scale, 3250 *scale)
        col_shape = [{'shape_info': {'inner_radius': 0, 'outer_radius': 10 *scale, 'mass': 50, 'offset': (0, 0)},
          'collision_type': 49, 'group': 11, 'elasticity': 1, 'friction': 1, 'shape_type': 'circle'}]

        for x in range(30):
            object_physics = {'main_shape': 'circle', 'velocity': (0, 0), 'position': pos, 'angle': 0,
                           'angular_velocity': 0, 'vel_limit': 1000, 'ang_vel_limit': radians(200), 'mass': 50,
                           'col_shapes': col_shape}
            object = {render: {'texture': 'bullet', 'render': True},
                        'cymunk_physics': object_physics, 'position': pos,
                        'rotate': 0, 'scale': 1 *scale, 'color': (255, 255, 255, 255)}
            component_order = ['position', 'rotate', 'scale', 'color', 'cymunk_physics', render]
            object = init_entity(object, component_order)


    #horbar
        pos = (-2134*scale, 2343.5*scale)

        for x in range(4):
            col_shape = [{'shape_info': {'width': 372 *scale, 'height': 35 *scale, 'mass': 0,},
          'collision_type': 60, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]

            object_physics = {'main_shape': 'box', 'velocity': (0, 0), 'position': pos, 'angle': 0,
                           'angular_velocity': 0, 'vel_limit': 1000, 'ang_vel_limit': radians(200), 'mass': 0,
                           'col_shapes': col_shape}
            object = {render: {'texture': 'blank', 'render': True},
                        'cymunk_physics': object_physics, 'position': pos,
                        'rotate': 0, 'scale': 1 *scale, 'color': (255, 255, 255, 255)}
            component_order = ['position', 'rotate', 'scale', 'color', 'cymunk_physics', render]
            object = init_entity(object, component_order)

    #vertbar
        pos = (-2134*scale, 2343.5*scale)

        for x in range(2):
            col_shape = [{'shape_info': {'width': 36 *scale, 'height': 378 *scale, 'mass': 0,},
          'collision_type': 3, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]

            object_physics = {'main_shape': 'box', 'velocity': (0, 0), 'position': pos, 'angle': 0,
                           'angular_velocity': 0, 'vel_limit': 1000, 'ang_vel_limit': radians(200), 'mass': 0,
                           'col_shapes': col_shape}
            object = {render: {'texture': 'blank', 'render': True},
                        'cymunk_physics': object_physics, 'position': pos,
                        'rotate': 0, 'scale': 1 *scale, 'color': (255, 255, 255, 255)}
            component_order = ['position', 'rotate', 'scale', 'color', 'cymunk_physics', render]
            object = init_entity(object, component_order)

    #biscuit
        pos = (-2134*scale, 2343.5*scale)
        angle = [1,.5,1,.5,.5,1,.5,1]
        coltype = [60,3,3,60,3,60,60,3]
        for x in range(8):
            col_shape = [{'shape_info': {'width': 23 *scale, 'height': 24 *scale, 'mass': 0,},
          'collision_type': coltype[x], 'group': 1, 'elasticity': .1, 'friction': 1, 'shape_type': 'box'}]

            object_physics = {'main_shape': 'box', 'velocity': (0, 0), 'position': pos, 'angle': angle[x],
                           'angular_velocity': 0, 'vel_limit': 1000, 'ang_vel_limit': radians(200), 'mass': 0,
                           'col_shapes': col_shape}
            object = {render: {'texture': 'blank', 'render': True},
                        'cymunk_physics': object_physics, 'position': pos,
                        'rotate': 0, 'scale': 1 *scale, 'color': (255, 255, 255, 255)}
            component_order = ['position', 'rotate', 'scale', 'color', 'cymunk_physics', render]
            object = init_entity(object, component_order)

    #biscuitsmall
        pos = (-2134*scale, 2343.5*scale)
        angle = [.5,1,1,.5]
        for x in range(len(angle)):
            col_shape = [{'shape_info': {'width': 22 *scale, 'height': 20 *scale, 'mass': 0,},
          'collision_type': 60, 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]

            object_physics = {'main_shape': 'box', 'velocity': (0, 0), 'position': pos, 'angle': angle[x],
                           'angular_velocity': 0, 'vel_limit': 1000, 'ang_vel_limit': radians(200), 'mass': 0,
                           'col_shapes': col_shape}
            object = {render: {'texture': 'blank', 'render': True},
                        'cymunk_physics': object_physics, 'position': pos,
                        'rotate': 0, 'scale': 1 *scale, 'color': (255, 255, 255, 255)}
            component_order = ['position', 'rotate', 'scale', 'color', 'cymunk_physics', render]
            object = init_entity(object, component_order)


    #missles
        pos = (3000*scale, 500*scale)
        col_shape = [{'shape_info': {'width': 49*scale, 'height': 12*scale, 'mass': 40,},
      'collision_type': 62, 'group': 2, 'elasticity': 1, 'friction': 1, 'shape_type': 'box'}]

        for x in range(7):
            object_physics = {'main_shape': 'box', 'velocity': (0, 0), 'position': pos, 'angle': 0,
                           'angular_velocity': 0, 'vel_limit': 3000, 'ang_vel_limit': radians(200), 'mass': 40,
                           'col_shapes': col_shape}
            object = {render: {'texture': 'missle', 'render': True},
                        'cymunk_physics': object_physics, 'position': pos,
                        'rotate': 0, 'scale': 1 *scale, 'color': (255, 255, 255, 255),
                      'emitters': [],}
            component_order = ['position', 'rotate', 'scale', 'color', 'cymunk_physics', render, 'emitters']
            object = init_entity(object, component_order)

    #bigmissle
        pos = (3000*scale, 500*scale)
        col_shape = [{'shape_info': {'mass': 40, 'vertices': [(-30*scale, -8*scale), (17*scale, -8*scale), (28*scale, -4*scale), (30*scale, 0*scale), (28*scale, 3*scale), (17*scale, 8*scale), (-30*scale, 8*scale),], 'offset': (0, 0)},
               'collision_type': 63, 'group': 2, 'elasticity': 1, 'friction': 1.0, 'shape_type': 'poly'},
              ]
        for x in range(7):
            object_physics = {'main_shape': 'poly', 'velocity': (0, 0), 'position': pos, 'angle': 0,
                           'angular_velocity': 0, 'vel_limit': 3000, 'ang_vel_limit': radians(200), 'mass': 40,
                           'col_shapes': col_shape}
            object = {render: {'texture': 'bigmissle', 'render': True},
                        'cymunk_physics': object_physics, 'position': pos,
                        'rotate': 0, 'scale': 1 *scale, 'color': (255, 255, 255, 255),
                      'emitters': [],}
            component_order = ['position', 'rotate', 'scale', 'color', 'cymunk_physics', render, 'emitters']
            object = init_entity(object, component_order)

    #omissle
        pos = (3000*scale, 500*scale)
        col_shape = [{'shape_info': {'inner_radius': 0, 'outer_radius': 13 *scale, 'mass': 40, 'offset': (0, 0)},
      'collision_type': 64, 'group': 2, 'elasticity': 1, 'friction': 1, 'shape_type': 'circle'}]

        for x in range(7):
            object_physics = {'main_shape': 'circle', 'velocity': (0, 0), 'position': pos, 'angle': 0,
                           'angular_velocity': 0, 'vel_limit': 1000, 'ang_vel_limit': radians(200), 'mass': 40,
                           'col_shapes': col_shape}
            object = {render: {'texture': 'omissle', 'render': True},
                        'cymunk_physics': object_physics, 'position': pos,
                        'rotate': 0, 'scale': 1 *scale, 'color': (255, 255, 255, 255),
                      'emitters': [],}
            component_order = ['position', 'rotate', 'scale', 'color', 'cymunk_physics', render, 'emitters']
            object = init_entity(object, component_order)

    #redballs
        pos = [(3500*scale, 260*scale), (3530*scale, 260*scale), (3560*scale, 260*scale),
               (3590*scale, 260*scale), (3620*scale, 260*scale), (3650*scale, 260*scale),
               (3680*scale, 260*scale), (3710*scale, 260*scale), (3740*scale, 260*scale),
               (3770*scale, 260*scale), (3800*scale, 260*scale), (3830*scale, 260*scale),
               (3860*scale, 260*scale), (3890*scale, 260*scale), (3920*scale, 260*scale)]
        col_shape = [{'shape_info': {'inner_radius': 0, 'outer_radius': 11.5 *scale, 'mass': 300, 'offset': (0, 0)},
      'collision_type': 72, 'group': 0, 'elasticity': 1, 'friction': 1, 'shape_type': 'circle'}]

        for x in range(15):
            object_physics = {'main_shape': 'circle', 'velocity': (0, 0), 'position': pos[x], 'angle': 0,
                           'angular_velocity': 0, 'vel_limit': 1000, 'ang_vel_limit': radians(200), 'mass': 300,
                           'col_shapes': col_shape}
            object = {render: {'texture': 'red', 'render': True},
                        'cymunk_physics': object_physics, 'position': pos[x],
                        'rotate': 0, 'scale': 1 *scale, 'color': (255, 255, 255, 255)}
            component_order = ['position', 'rotate', 'scale', 'color', 'cymunk_physics', render]
            object = init_entity(object, component_order)

    #cueblocker
        pos = (-2134*scale, 2343.5*scale)
        width = [32, 32, 32, 32, 150, 32]
        height = [28, 28, 28, 28, 70, 23]
        angle = [-.8,.8,-.8,.8,0,0]

        for x in range(6):
            col_shape = [{'shape_info': {'width': width[x] *scale, 'height': height[x] *scale, 'mass': 0,},
          'collision_type': 74, 'group': 1, 'elasticity': .1, 'friction': 1, 'shape_type': 'box'}]

            object_physics = {'main_shape': 'box', 'velocity': (0, 0), 'position': pos, 'angle': angle[x],
                           'angular_velocity': 0, 'vel_limit': 1000, 'ang_vel_limit': radians(200), 'mass': 0,
                           'col_shapes': col_shape}
            object = {render: {'texture': 'blank', 'render': True},
                        'cymunk_physics': object_physics, 'position': pos,
                        'rotate': 0, 'scale': 1 *scale, 'color': (255, 255, 255, 255)}
            component_order = ['position', 'rotate', 'scale', 'color', 'cymunk_physics', render]
            object = init_entity(object, component_order)

    #detector
        pos = (2200 *scale, 250 *scale)
        coltype = [75, 76, 77, 78, 79, 80]
        for x in range(6):
            col_shape = [{'shape_info': {'inner_radius': 0, 'outer_radius': 5 *scale, 'mass': 0, 'offset': (0, 0)},
          'collision_type': coltype[x], 'group': 1, 'elasticity': 1, 'friction': 1, 'shape_type': 'circle'}]

            object_physics = {'main_shape': 'circle', 'velocity': (0, 0), 'position': pos, 'angle': 0,
                           'angular_velocity': 0, 'vel_limit': 1000, 'ang_vel_limit': radians(200), 'mass': 0,
                           'col_shapes': col_shape}
            object = {render: {'texture': 'blank', 'render': True},
                        'cymunk_physics': object_physics, 'position': pos,
                        'rotate': 0, 'scale': 1 *scale, 'color': (255, 255, 255, 255)}
            component_order = ['position', 'rotate', 'scale', 'color', 'cymunk_physics', render]
            object = init_entity(object, component_order)

        for x in range(len(self.objspoly)):
            object_physics = {'main_shape': 'poly', 'velocity': (0, 0), 'position': self.objspoly[x][1], 'angle': 0,
                  'angular_velocity': 0, 'vel_limit': self.objspoly[x][4], 'ang_vel_limit': radians(1000),
                  'mass': self.objspoly[x][3], 'col_shapes': self.objspoly[x][-1]}
            object = {self.objspoly[x][2]: {'texture': self.objspoly[x][0], 'render': True},
                        'cymunk_physics': object_physics, 'position': self.objspoly[x][1],
                        'rotate': 0, 'scale': 1 *scale, 'color': (255, 255, 255, 255),
                      'emitters': [],}
            component_order = ['position', 'rotate', 'scale', 'color', 'cymunk_physics', self.objspoly[x][2], 'emitters']
            initobj = init_entity(object, component_order)


        tex = [('restartbtn', render),
               ('mainmenubtn', render),
               ('stageselectbtn', render),
               ('successimg', rendertop),
               ('tryagainimg', rendertop),
               ('blanker', render2),
               ('btntex', render2),

               ]



        for x in range(len(tex)):
            pos = (2629 *scale, 4000 *scale)
            areabound = {tex[x][1]: {'texture': tex[x][0], 'render': True},
                  'position': pos, 'rotate': 0, 'scale': 1*scale, 'color': (255,255,255,255),}
            component_order = ['position', 'rotate', 'scale', 'color', tex[x][1]]
            areabound = init_entity(areabound, component_order)

    def rollbackassets(self, *args):
        touch = self.gameworld.system_manager['cymunk_touch']
        ignore = range(1, 85)
        touch.ignore_groups = ignore

        physics = self.gameworld.system_manager['cymunk_physics']
        physics.gravity = (0, 0)

        boundary = self.gameworld.system_manager['boundary']

        boundary.objs = []
        boundary.objs2 = []
        boundary.objs3 = []

        rotation = self.gameworld.system_manager['rotation']

        boundary.paused = True
        rotation.paused = True
        # touch.paused = True
        physics.paused = True

        sysbox = []

        emitter_system = self.ids.emitter

        self.closebutton.pos = (1083 *scale, 1000 *scale)

        if self.timer:
            self.timer.cancel()

        if self.nametimer:
            self.nametimer.cancel()

        try:
            cons = physics.space.constraints
            for x in range(self.consnum):
                physics.space._remove_constraint(cons[0])
            self.consnum = 0

        except:
            pass

        entities = self.gameworld.entities

        objs = ['areabound', 'timeline', 'segtex', 'screentex', 'closex',
                'name1', 'name2', 'name3', 'name4', 'name5',
                'name6', 'name7', 'name8', 'name9', 'name10', 'striker'
                ]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            areaboundpos = entity.position
            areaboundpos.pos = (2629 *scale, 4000 *scale)

        objs = ['seg', 'seg2', 'seg3', 'seg4', 'seg5', 'seg6', 'seg7', 'seg8',
                'screen', 'screen2', 'screen3', 'screen4', 'screen5', 'screen6',
                'screen7', 'screen8', 'screen9', 'screen10', 'screen11',
                'slit']
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = (-2134*scale, 2343.5*scale)
            physics.space.reindex_shape(shape[0])

        objs = ['striker', 'goal']
        pos = [(2702 *scale, 2060 *scale), (2702 *scale, 2000 *scale)]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = pos[x]
            physics.space.reindex_shape(shape[0])
            body.reset_forces()
            body.angle = 0
            body.velocity = (0, 0)
            body.angular_velocity = 0


        if self.level == 1:
            emitter_system.remove_effect(ent['striker'], 0)
            if self.startguide:
                objs = ['showhand', 'showball', 'msg']
                for x in range(len(objs)):
                    entity = entities[ent[objs[x]]]
                    imagepos = entity.position
                    imagepos.pos = (2629 *scale, 2882 *scale)
                self.startguide = False



        elif self.level == 2:
            emitter_system.remove_effect(ent['striker'], 0)

            objs = ['slit2', 'cameraholder']
            pos = [(-2134*scale, 2343.5*scale), (1947*scale, 2326.5*scale)]
            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                body = entity.cymunk_physics.body
                shape = entity.cymunk_physics.shapes
                body.position = pos[x]
                physics.space.reindex_shape(shape[0])

            entity = entities[ent['camera']]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = (2282*scale, 2321.5*scale)
            for x in shape:
                physics.space.reindex_shape(x)
            body.reset_forces()
            body.angle = 0
            body.velocity = (0, 0)
            body.angular_velocity = 0

        elif self.level == 3:
            emitter_system.remove_effect(ent['striker'], 0)

            entity = entities[ent['magicball']]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = (2603*scale, 2060 *scale)
            physics.space.reindex_shape(shape[0])
            body.reset_forces()
            body.velocity = (0, 0)
            body.angular_velocity = 0

            #ropesupport
            objs = ['ropesupport', 'ropesupport2', 'ropestopper']
            pos = [(1980 *scale, 475 *scale), (2970 *scale, 285 *scale), (-2134*scale, 2343.5*scale)]
            for x in range(len(pos)):
                entity = entities[ent[objs[x]]]
                body = entity.cymunk_physics.body
                shape = entity.cymunk_physics.shapes
                body.position = pos[x]
                physics.space.reindex_shape(shape[0])

            #rope
            posz = [2035, 2085, 2135, 2185, 2235, 2285, 2335, 2385, 2435, 2485, 2535, 2585, 2635, 2685, 2735, 2785, 2835, 2885, 2935, 2985]
            posy = [475, 465, 455, 445, 435, 425, 415, 405, 395, 385, 375, 365, 355, 345, 335, 325, 315, 305, 295, 285]
            rope = ['rope', 'rope2', 'rope3', 'rope4', 'rope5', 'rope6', 'rope7', 'rope8', 'rope9', 'rope10', 'rope11',
                    'rope12', 'rope13', 'rope14', 'rope15', 'rope16', 'rope17', 'rope18', 'rope19', 'rope20']
            for x in range(len(posz)):
                entity = entities[ent[rope[x]]]
                body = entity.cymunk_physics.body
                shape = entity.cymunk_physics.shapes
                body.position = (posz[x]*scale, posy[x]*scale)
                physics.space.reindex_shape(shape[0])
                body.reset_forces()
                body.angle = 0
                body.velocity = (0, 0)
                body.angular_velocity = 0


        elif self.level == 4:
            emitter_system.remove_effect(ent['striker'], 0)

            objs = ['areabound2', 'timeline2', 'basketkit']
            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                areaboundpos = entity.position
                areaboundpos.pos = (2629 *scale, 4000 *scale)

            objs = ['basket1', 'basket2', 'basket3', 'basket4', 'basket5',
                    'basketedge', 'basketedge2',
                    'nethook', 'nethook2', 'nethook3', 'nethook4', 'nethook5',
                    'slit3']

            pos = [(2647*scale, 2000*scale), (2647*scale, 2000*scale), (2647*scale, 2000*scale),
                   (2647*scale, 2000*scale), (2647*scale, 2000*scale),
                   (3409*scale, 1410 *scale), (3454 *scale, 1410 *scale),
                   (3916.3 *scale, 1408*scale), (3923.9 *scale, 1408*scale), (3931.5 *scale, 1408*scale),
                   (3939.1 *scale, 1408*scale), (3946.7 *scale, 1408*scale),
                   (-2134*scale, 2343.5*scale)]

            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                body = entity.cymunk_physics.body
                shape = entity.cymunk_physics.shapes
                body.position = pos[x]
                physics.space.reindex_shape(shape[0])

            objs = ['net', 'net2', 'net3', 'net4', 'net5',
            'net6', 'net7', 'net8', 'net9', 'net10',
            'innet', 'innet2', 'innet3', 'innet4',
            'innet5', 'innet6', 'innet7', 'innet8',
            'innet9', 'innet10', 'innet11',
            'innet12', 'innet13','innet14', 'innet15', 'innet16',
            'innet17', 'innet18',
            'innet19', 'innet20','innet21', 'innet22', 'innet23', 'innet24',
            'innet25','innet26', 'innet27', 'innet28', 'innet29',
            'innet30', 'innet31', 'innet32',
            'innet33','innet34', 'innet35', 'innet36', 'innet37', 'innet38',
            'innet39', 'innet40',
            'innethor', 'innethor2', 'innethor3',]

            pos = [(3909 *scale, 1403 *scale), (3909 *scale, 1395 *scale), (3909 *scale, 1387 *scale), (3909 *scale, 1379 *scale), (3909 *scale, 1371 *scale),
                   (3954 *scale, 1403 *scale), (3954 *scale, 1395 *scale), (3954 *scale, 1387 *scale), (3954*scale, 1379 *scale), (3954*scale, 1371 *scale),

                   (3931.5 *scale, 1403*scale), (3931.5 *scale, 1395*scale), (3931.5 *scale, 1387*scale), (3931.5 *scale, 1379*scale),
                   (3931.5 *scale, 1403*scale), (3931.5 *scale, 1395*scale), (3931.5 *scale, 1387*scale), (3931.5 *scale, 1379*scale),

                   (3923.9 *scale, 1403*scale), (3923.9 *scale, 1395*scale), (3923.9 *scale, 1387*scale),
                   (3923.9 *scale, 1403*scale), (3923.9 *scale, 1395*scale), (3923.9 *scale, 1387*scale),
                   (3923.9 *scale, 1379*scale), (3923.9 *scale, 1371*scale),

                   (3916.3 *scale, 1403*scale), (3916.3 *scale, 1395*scale),
                   (3916.3 *scale, 1403*scale), (3916.3 *scale, 1395*scale), (3916.3 *scale, 1387*scale),
                   (3916.3 *scale, 1379*scale), (3916.3 *scale, 1371*scale), (3916.3 *scale, 1363*scale),

                   (3939.1 *scale, 1403*scale), (3939.1 *scale, 1395*scale), (3939.1 *scale, 1387*scale),
                   (3939.1 *scale, 1379*scale), (3939.1 *scale, 1371*scale),
                   (3939.1 *scale, 1403*scale), (3939.1 *scale, 1395*scale), (3939.1 *scale, 1387*scale),

                   (3946.7 *scale, 1403*scale), (3946.7 *scale, 1395*scale), (3946.7 *scale, 1387*scale),
                   (3946.7 *scale, 1379*scale), (3946.7 *scale, 1371*scale), (3946.7 *scale, 1363*scale),
                   (3946.7 *scale, 1403*scale), (3946.7 *scale, 1395*scale),

                   (3926.5 *scale, 1371*scale), (3931.5 *scale, 1371*scale), (3936.5 *scale, 1371*scale)]

            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                body = entity.cymunk_physics.body
                shape = entity.cymunk_physics.shapes
                body.position = pos[x]
                physics.space.reindex_shape(shape[0])
                body.reset_forces()
                body.angle = 0
                body.velocity = (0, 0)
                body.angular_velocity = 0

        elif self.level == 5:
            objs = ['striker', 'light', 'light2']
            for x in range(len(objs)):
                emitter_system.remove_effect(ent[objs[x]], 0)


            objs = ['lv5screen']
            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                areaboundpos = entity.position
                areaboundpos.pos = (2629 *scale, 4000 *scale)

            objs = ['light', 'light2']
            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                areaboundpos = entity.position
                areaboundpos.pos = (-2134*scale, 2343.5*scale)

            objs = ['sc5', 'sc5_2', 'sc5_3', 'sc5_4', 'sc5_5', 'sc5_6', 'sc5_7', 'sc5_8', 'sc5_9', 'sc5_10', 'sc5_11',
                    'light', 'light2', 'teleblocker']
            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                body = entity.cymunk_physics.body
                shape = entity.cymunk_physics.shapes
                body.position = (-2134*scale, 2343.5*scale)
                physics.space.reindex_shape(shape[0])



        elif self.level == 6:
            emitter_system.remove_effect(ent['striker'], 0)


            objs = ['sc6', 'sc6_2', 'sc6_3', 'sc6_4', 'supporter', 'supporter2']
            pos = [(-2134*scale, 2343.5*scale), (-2134*scale, 2343.5*scale),
                   (-2134*scale, 2343.5*scale), (-2134*scale, 2343.5*scale),
                   (3040*scale, 1800*scale), (3055*scale, 1800*scale)]

            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                body = entity.cymunk_physics.body
                shape = entity.cymunk_physics.shapes
                body.position = pos[x]
                physics.space.reindex_shape(shape[0])

            objs = ['lv6screen']
            pos = [(2629 *scale, 4000 *scale),]
            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                areaboundpos = entity.position
                areaboundpos.pos = pos[x]

            objs = ['topbar', 'cart', 'cartwheel',
                    'brick', 'brick2', 'brick3', 'brick4', 'brick5', 'brick6', 'brick7', 'brick8', 'brick9',
                    'leftweight', 'rightweight',]

            pos = [(-2134*scale, 2468.5*scale), (3000*scale, 2060 *scale), (3040*scale, 2045*scale),
                   (3040*scale, 1944*scale), (3060*scale, 1944*scale), (3080*scale, 1944*scale),
                   (3100*scale, 1944*scale), (3120*scale, 1944*scale), (3140*scale, 1944*scale),
                   (3160*scale, 1944*scale), (3180*scale, 1944*scale), (3200*scale, 1944*scale),
                   (-2209*scale, 2458.5*scale), (-2059*scale, 2458.5*scale),]

            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                body = entity.cymunk_physics.body
                shape = entity.cymunk_physics.shapes
                body.position = pos[x]
                for x in shape:
                    physics.space.reindex_shape(x)
                body.reset_forces()
                body.velocity = (0, 0)
                body.angular_velocity = 0
                body.angle = 0


        elif self.level == 7:
            if self.timer:
                self.timer.cancel()

            if self.successchecktimer:
                self.successchecktimer.cancel()

            objs = ['cannonball', 'cannonball2', 'cannonball3', 'cannonball4']
            for x in range(len(objs)):
                emitter_system.remove_effect(ent[objs[x]], 0)

            objs = ['segtex2', 'segtex3', 'segtex4', 'texcnn', 'lv9screen']
            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                areaboundpos = entity.position
                areaboundpos.pos = (2629 *scale, 4000 *scale)


            #bat
            objs = ['bat']
            pos = [(3347 *scale, 2065 *scale)]
            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                body = entity.cymunk_physics.body
                shape = entity.cymunk_physics.shapes
                body.position = pos[x]
                for x in shape:
                    physics.space.reindex_shape(x)
                body.reset_forces()
                body.velocity = (0, 0)
                body.angular_velocity = 0
                body.angle = 0

            objs = ['batholder']
            pos = [(3347 *scale, 2027 *scale)]
            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                body = entity.cymunk_physics.body
                shape = entity.cymunk_physics.shapes
                body.position = pos[x]
                physics.space.reindex_shape(shape[0])

            #segs
            objs = ['seg', 'seg2', 'seg3', 'seg4', 'seg5', 'seg6', 'seg7', 'seg8',
                'seg9', 'seg10', 'seg11', 'seg12', 'seg13', 'seg14', 'seg15', 'seg16',
                'seg17', 'seg18', 'seg19', 'seg20', 'seg21', 'seg22', 'seg23', 'seg24',
                'seg25', 'seg26', 'seg27', 'seg28', 'seg29', 'seg30', 'seg31', 'seg32',]
            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                body = entity.cymunk_physics.body
                shape = entity.cymunk_physics.shapes
                body.position = (-2134*scale, 2343.5*scale)
                physics.space.reindex_shape(shape[0])

            #goals
            objs = ['cgoal', 'cgoal2', 'cgoal3', 'cgoal4',
                    'cannon', 'cannon2',
                    'sensor',
                    'cannonball', 'cannonball2', 'cannonball3', 'cannonball4',
                    ]

            pos = [(3050*scale, 1700*scale), (3120*scale, 1700*scale),
                   (3190 *scale, 1700 *scale), (3260 *scale, 1700 *scale),

                   (-2134*scale, 2343.5*scale), (-2134*scale, 2343.5*scale),
                   (3150 *scale, 1800 *scale),

                   (3070*scale, 1800*scale), (3120*scale, 1800*scale),
                   (3170 *scale, 1800 *scale), (3220 *scale, 1800 *scale),
                   ]

            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                body = entity.cymunk_physics.body
                shape = entity.cymunk_physics.shapes
                body.position = pos[x]
                physics.space.reindex_shape(shape[0])


            objs = ['cannonball', 'cannonball2', 'cannonball3', 'cannonball4',
                    'cgoal', 'cgoal2', 'cgoal3', 'cgoal4']
            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                body = entity.cymunk_physics.body
                body.angle = 0
                body.reset_forces()
                body.velocity = (0, 0)
                body.angular_velocity = 0

        elif self.level == 8:
            objs = ['spstriker', 'spstriker2']
            for x in range(len(objs)):
                emitter_system.remove_effect(ent[objs[x]], 0)


            objs = ['Ytex', 'lv8screen', 'blanker', 'btntex']
            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                areaboundpos = entity.position
                areaboundpos.pos = (2629 *scale, 4000 *scale)

            objs = ['sc8', 'sc8_2', 'sc8_3', 'sc8_4',
                    'sc8_5', 'sc8_6', 'sc8_7', 'sc8_8',
                    'y1', 'y2', 'y3',
                    'buttonblocker', 'buttonblocker2', 'buttonblocker3',
                    'buttonholder', 'buttonholder2',
                    'Ysensor'
                    ]
            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                body = entity.cymunk_physics.body
                shape = entity.cymunk_physics.shapes
                body.position = (-2134*scale, 2343.5*scale)
                physics.space.reindex_shape(shape[0])

            objs = ['bar1', 'bot1', 'bar2', 'bot2']
            pos = [(475 *scale, 2265 *scale), (475 *scale, 2265 *scale),
                   (475 *scale, -1735 *scale), (475 *scale, -1735 *scale)]
            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                body = entity.cymunk_physics.body
                shape = entity.cymunk_physics.shapes
                body.position = pos[x]
                physics.space.reindex_shape(shape[0])

            entity = entities[ent['btn1']]
            renderer = entity.rotate_color_scale_renderer2
            renderer.texture_key = 'blank'

            objs = ['spstriker', 'spstriker2', 'Ynormal', 'btn1', 'btn2',]
            pos = [(3170 *scale, 1600 *scale), (3220 *scale, 1600 *scale),
                   (4500 *scale, 2027*scale), (-1000*scale, 2343.5*scale),
                   (-1000*scale, 2380.5*scale),]
            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                body = entity.cymunk_physics.body
                shape = entity.cymunk_physics.shapes
                body.position = pos[x]
                physics.space.reindex_shape(shape[0])
                body.reset_forces()
                body.velocity = (0,0)
                body.angle = 0
                body.angular_velocity = 0



            entity = entities[ent['btn1']]
            renderer = entity.rotate_color_scale_renderer2
            renderer.texture_key = 'blank'


        elif self.level == 9:
            if self.timer:
                self.timer.cancel()
            if self.ntimer:
                self.ntimer.cancel()

            boundary = self.gameworld.system_manager['boundary']
            boundary.cancelcall = False

            objs = ['lv9screen2','ab', 'tl', 'nblanker',
                    'segtex2', 'ab2', 'tl2', 'nblanker2', 'tankguide']
            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                areaboundpos = entity.position
                areaboundpos.pos = (2629 *scale, 4000 *scale)

            objs = ['screen5', 'screen6','arenahor', 'arenahor2', 'arenahor3', 'arenahor4',
                    'arenahorlong', 'arenavert', 'arenavertsmall',
                    'seg9', 'seg10', 'seg11', 'seg12', 'seg13',
                    'seg14', 'seg15', 'seg16',]
            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                body = entity.cymunk_physics.body
                shape = entity.cymunk_physics.shapes
                body.position = (-2134*scale, 2343.5*scale)
                physics.space.reindex_shape(shape[0])


            objs = ['startpoint', 'endpoint', 'gunstopper']
            pos = [(1700 *scale, 3104 *scale), (1700 *scale, 3340 *scale),
                   (1700 *scale, 3160 *scale)]
            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                body = entity.cymunk_physics.body
                shape = entity.cymunk_physics.shapes
                body.position = pos[x]
                physics.space.reindex_shape(shape[0])
                body.reset_forces()
                body.angular_velocity  = 0
                body.velocity = (0, 0)

            entity = entities[ent['gun']]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = (1700 *scale, 3140 *scale)
            for x in shape:
                physics.space.reindex_shape(x)
            body.reset_forces()
            body.angular_velocity = 0
            body.angle = 0
            body.velocity = (0, 0)

            entity = entities[ent['gunarch']]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = (1700 *scale, 3100 *scale)
            for x in shape:
                physics.space.reindex_shape(x)

            objs = ['ngoal', 'ngoal2',]
            pos = [(2000*scale, 1700*scale), (2050*scale, 1700*scale),
                   ]
            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                body = entity.cymunk_physics.body
                shape = entity.cymunk_physics.shapes
                body.position = pos[x]
                physics.space.reindex_shape(shape[0])
                body.reset_forces()
                body.velocity = (0,0)
                body.angle = 0
                body.angular_velocity = 0

            objs = ['bullet', 'bullet2', 'bullet3', 'bullet4', 'bullet5', 'bullet6', 'bullet7', 'bullet8',
        'bullet9', 'bullet10', 'bullet11', 'bullet12', 'bullet13', 'bullet14', 'bullet15',
        'bullet16', 'bullet17', 'bullet18', 'bullet19', 'bullet20', 'bullet21', 'bullet22',
        'bullet23', 'bullet24', 'bullet25', 'bullet26', 'bullet27', 'bullet28', 'bullet29', 'bullet30',]

            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                body = entity.cymunk_physics.body
                shape = entity.cymunk_physics.shapes
                body.position = (2000 *scale, 3250 *scale)
                physics.space.reindex_shape(shape[0])
                body.reset_forces()
                body.velocity = (0,0)
                body.angular_velocity = 0


        elif self.level == 10:
            if self.attgenctrl:
                self.attgenctrl.cancel()
            if self.timer:
                self.timer.cancel()
            if self.tentimer:
                self.tentimer.cancel()
            self.attgencount = 0


            entity = entities[ent['segtex']]
            renderer = entity.rotate_color_scale_renderer2
            renderer.texture_key = 'segtex'

            objs = ['suppatt1', 'suppatt2', 'suppatt3', 'suppatt4',]
            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                body = entity.cymunk_physics.body
                shape = entity.cymunk_physics.shapes
                body.position = (-2134*scale, 2343.5*scale)
                physics.space.reindex_shape(shape[0])

            objs = ['missle1', 'missle2', 'missle3', 'missle4', 'missle5',
                    'missle6', 'missle7',
                    'bigmissle1', 'bigmissle2', 'bigmissle3', 'bigmissle4', 'bigmissle5',
                    'bigmissle6', 'bigmissle7',
                    'omissle1', 'omissle2', 'omissle3', 'omissle4', 'omissle5',
                    'omissle6', 'omissle7',]

            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                body = entity.cymunk_physics.body

                emitter_system.remove_effect(ent[objs[x]], 0)

                shape = entity.cymunk_physics.shapes
                body.position = (3000*scale, 500*scale)
                physics.space.reindex_shape(shape[0])
                body.reset_forces()
                body.velocity = (0, 0)
                body.angular_velocity = 0
                body.angle = 0

            emitter_system.remove_effect(ent['fireball'], 0)
            emitter_system.remove_effect(ent['fireball2'], 0)

            objs = ['fireball', 'ropehook', 'ropecomp', 'ropecomp2',
                'ropecomp3', 'ropecomp4', 'ropecomp5', 'ropehook2', 'fireball2',]
            pos = [(1200 *scale, 300 *scale), (1211 *scale, 300 *scale),
                   (1227 *scale, 300 *scale), (1239 *scale, 300 *scale),
                   (1251 *scale, 300 *scale), (1263 *scale, 300 *scale), (1275 *scale, 300 *scale),
                   (1291 *scale, 300 *scale), (1302 *scale, 300 *scale)]
            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                body = entity.cymunk_physics.body
                shape = entity.cymunk_physics.shapes
                body.position = pos[x]
                for x in shape:
                    physics.space.reindex_shape(x)
                body.reset_forces()
                body.velocity = (0,0)
                body.angle = 0
                body.angular_velocity = 0


        touch.paused = True
        physics.paused = False
        #touch.paused = False
        sysbox.append('cymunk_physics')
        sysbox.append('cymunk_touch')

        Clock.schedule_once(self.staterefresh, .1)

    def staterefresh(self, dt):
        touch = self.gameworld.system_manager['cymunk_touch']
        physics = self.gameworld.system_manager['cymunk_physics']

        touch.paused = True
        physics.paused = True
        sysbox = []

    def rollbackslam(self):

        entities = self.gameworld.entities
        physics = self.gameworld.system_manager['cymunk_physics']
        touch = self.gameworld.system_manager['cymunk_touch']
        emitter_system = self.ids.emitter
        emitter_system.remove_effect(ent['white'], 0)

        touch.paused = True
        physics.paused = True
        sysbox = []


        self.btnlist[-1].pos = (2629 *scale, 4000 *scale)
        self.slamreset.pos = (2629 *scale, 4000 *scale)

        try:
            cons = physics.space.constraints
            for x in range(self.consnum):
                physics.space._remove_constraint(cons[0])
            self.consnum = 0

        except:
            pass

        objs = ['table', 'backbutton', 'slamre']
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            areaboundpos = entity.position
            areaboundpos.pos = (2629 *scale, 4000 *scale)

        objs = ['yellow', 'green', 'brown', 'blue', 'pink', 'black', 'white', 'cue',
            'red1',
            'red2', 'red3',
            'red4', 'red5', 'red6',
            'red7', 'red8', 'red9', 'red10',
            'red11', 'red12', 'red13', 'red14', 'red15'
            ]
        pos = [(3560 *scale, 293 *scale), (3530 *scale, 293 *scale),
               (3590 *scale, 293 *scale), (3620 *scale, 293 *scale),
               (3650 *scale, 293 *scale), (3680 *scale, 293 *scale),
               (3400 *scale, 293 *scale), (3400 *scale, 293 *scale),
               (3500*scale, 260*scale), (3530*scale, 260*scale), (3560*scale, 260*scale),
           (3590*scale, 260*scale), (3620*scale, 260*scale), (3650*scale, 260*scale),
           (3680*scale, 260*scale), (3710*scale, 260*scale), (3740*scale, 260*scale),
           (3770*scale, 260*scale), (3800*scale, 260*scale), (3830*scale, 260*scale),
           (3860*scale, 260*scale), (3890*scale, 260*scale), (3920*scale, 260*scale)]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = pos[x]
            physics.space.reindex_shape(shape[0])
            body.reset_forces()
            body.velocity = (0, 0)
            body.angular_velocity = 0

        objs = ['horbar1', 'horbar2', 'horbar3', 'horbar4',
                'vertbar1', 'vertbar2',
                'bis1', 'bis2', 'bis3', 'bis4', 'bis5', 'bis6', 'bis7', 'bis8',
                'bsmal1', 'bsmal2', 'bsmal3', 'bsmal4',
                'cueblocker1', 'cueblocker2', 'cueblocker3',
                'cueblocker4', 'cueblocker5', 'cueblocker6',
                'detector1', 'detector2', 'detector3',
                'detector4', 'detector5', 'detector6',
                ]

        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = (-2134*scale, 2343.5*scale)
            physics.space.reindex_shape(shape[0])

        entity = entities[ent['horsupport2']]
        body = entity.cymunk_physics.body
        shape = entity.cymunk_physics.shapes
        body.position = ((475*scale)+wscale,(607*scale)+hscale)
        physics.space.reindex_shape(shape[0])

        touch.paused = False
        physics.paused = False
        sysbox.append('cymunk_physics')
        sysbox.append('cymunk_touch')
        Clock.schedule_once(self.staterefresh, .1)

    def rollbackname(self, once):
        entities = self.gameworld.entities
        names = [None, 'name1', 'name2', 'name3', 'name4', 'name5',
        'name6', 'name7', 'name8', 'name9', 'name10',]
        lvs = [1,2,3,4,5,6,7,8,9,10]
        if self.level in lvs:
            entity = entities[ent[names[self.level]]]
            areaboundpos = entity.position
            areaboundpos.pos = (2629 *scale, 4000 *scale)
        if self.level == 9:
            entity = entities[ent['tankguide']]
            areaboundpos = entity.position
            areaboundpos.pos = (2629 *scale, 4000 *scale)


#Levels

    def lv1(self, *args):

        self.rollbacklevelselect()
        self.nametimer = Clock.schedule_once(self.rollbackname, 2)

        self.more_force = True

        entities = self.gameworld.entities

        touch = self.gameworld.system_manager['cymunk_touch']

        ignore = range(1, 85)
        ignore.remove(4)
        touch.ignore_groups = ignore

        physics = self.gameworld.system_manager['cymunk_physics']
        physics.damping = 0.5

        boundary = self.gameworld.system_manager['boundary']
        boundary.shut = 1
        boundary.level = 1
        self.level = 1
        sysbox.append('boundary')

        emitter_system = self.ids.emitter
        emitter_system.add_effect(ent['striker'], 'strikereffects')

        self.closebutton.pos = ((880*scale)+wscale, (517*scale)+hscale)

        objs = ['areabound', 'timeline', 'segtex', 'screentex', 'closex', 'name1']
        pos = [((475 *scale)+wscale, (224 *scale)+hscale), ((475 *scale)+wscale, (224 *scale)+hscale),
               ((475 *scale)+wscale, (470 *scale)+hscale), ((475 *scale)+wscale, (293.5 *scale)+hscale),
               ((925 *scale)+wscale, (562 *scale)+hscale), ((200 *scale)+wscale, (520 *scale)+hscale)]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            areaboundpos = entity.position
            areaboundpos.pos = pos[x]


        objs = ['screen4', 'screen7', 'screen8', 'screen9', 'screen10', 'screen11',
                'seg', 'seg2', 'seg3', 'seg4', 'seg5', 'seg6', 'seg7', 'seg8',
                'vertsupport', 'vertsupport2', 'horsupport', 'horsupport2',
                'slit',
                'striker',
                'goal',
                ]

        pos = [((475*scale)+wscale, (5*scale)+hscale), ((5*scale)+wscale, (115*scale)+hscale), ((945*scale)+wscale, (115*scale)+hscale),
               ((5*scale)+wscale, (408.5*scale)+hscale), ((945*scale)+wscale, (408.5*scale)+hscale), ((475*scale)+wscale, (582*scale)+hscale),

               ((475*scale)+wscale, (510*scale)+hscale), ((475*scale)+wscale, (430*scale)+hscale), ((435*scale)+wscale, (470*scale)+hscale), ((515*scale)+wscale, (470*scale)+hscale),
               ((447*scale)+wscale, (498*scale)+hscale), ((447*scale)+wscale, (442*scale)+hscale), ((503*scale)+wscale, (442*scale)+hscale), ((503*scale)+wscale, (498*scale)+hscale),

               ((-20*scale)+wscale,(293.5*scale)+hscale), ((970*scale)+wscale,(293.5*scale)+hscale),
               ((475*scale)+wscale,(-20*scale)+hscale), ((475*scale)+wscale,(607*scale)+hscale),

               ((475 *scale)+wscale, (274 *scale)+hscale),
               ((400 *scale)+wscale, (100 *scale)+hscale),
               ((475 *scale)+wscale, (470 *scale)+hscale),
               ]

        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = pos[x]
            physics.space.reindex_shape(shape[0])

        touch.paused = False
        physics.paused = False
        sysbox.append('cymunk_physics')
        sysbox.append('cymunk_touch')

        boundary.objs = ['striker']
        boundary.paused = False

        self.lvprog = self.store2.get('lvprog')['progress']
        if self.lvprog[1] == 'lock':
            self.startguide = True
            objs = ['showhand', 'showball', 'msg']
            pos = [(590, 30), (544, 50), (750, 200)]
            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                imagepos = entity.position
                imagepos.pos = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)

            rotation = self.gameworld.system_manager['rotation']
            rotation.level = 'howtospecial'
            rotation.paused = False
            rotation.count = 0
            rotation.systemspeed(.2)
            sysbox.append('rotation')

    def lv2(self, *args):
        self.rollbacklevelselect()

        self.nametimer = Clock.schedule_once(self.rollbackname, 2)

        self.more_force = True
        sysbox.append('boundary')

        self.closebutton.pos = ((880*scale)+wscale, (517*scale)+hscale)

        init_entity = self.gameworld.init_entity
        entities = self.gameworld.entities

        touch = self.gameworld.system_manager['cymunk_touch']
        ignore = range(1, 85)
        ignore.remove(4)
        touch.ignore_groups = ignore

        physics = self.gameworld.system_manager['cymunk_physics']
        physics.damping = 0.5

        boundary = self.gameworld.system_manager['boundary']
        boundary.shut = 1
        boundary.level = 2
        self.level = 2

        emitter_system = self.ids.emitter
        emitter_system.add_effect(ent['striker'], 'strikereffects')

        rotation = self.gameworld.system_manager['rotation']
        rotation.level = 2
        rotation.paused = False
        rotation.camerastate = 'down'
        rotation.caught = False
        rotation.pushed = False
        rotation.systemspeed(.1)
        sysbox.append('rotation')



        objs = ['areabound', 'timeline', 'segtex', 'screentex', 'closex', 'name2']
        pos = [(475, 224), (475, 224),
               (475, 470), (475, 293.5),
               (925, 562), (190, 520)]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            areaboundpos = entity.position
            areaboundpos.pos = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)

        #segs
        objs = ['screen4', 'screen7', 'screen8', 'screen9', 'screen10', 'screen11',
                'seg', 'seg2', 'seg3', 'seg4', 'seg5', 'seg6', 'seg7', 'seg8',
                'vertsupport', 'vertsupport2', 'horsupport', 'horsupport2',
                'slit',
                'slit2',
                'striker',
                'goal',
                'cameraholder']
        pos = [(475, 5), (5, 115), (945, 115),
               (5, 408.5), (945, 408.5), (475, 582),

               (475, 510), (475, 430), (435, 470), (515, 470),
               (447, 498), (447, 442), (503, 442), (503, 498),

               (-20, 293.5), (970,293.5),
               (475,-20), (475,607),

               (475, 274),
               (475, 750),
               (400, 100),
               (475, 470),
               (40, 400)]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)
            physics.space.reindex_shape(shape[0])

        #camera
        entity = entities[ent['camera']]
        body = entity.cymunk_physics.body
        shape = entity.cymunk_physics.shapes
        body.position = ((375 *scale)+wscale, (395 *scale)+hscale)
        for x in shape:
            physics.space.reindex_shape(x)
        renderer = entity.rotate_color_scale_renderertop
        renderer.texture_key = 'camera'

        Clock.schedule_once(self.cameraconstraint, 0.1)

        touch.paused = False
        physics.paused = False
        sysbox.append('cymunk_physics')
        sysbox.append('cymunk_touch')

        boundary.objs = ['striker']
        boundary.paused = False

    def cameraconstraint(self, once):
        entities = self.gameworld.entities
        physics = self.gameworld.system_manager['cymunk_physics']

        objs = [('camera', 'cameraholder'),]
        anch = [((-314), (14), (22), (10))]
        for x in range(len(objs)):
            entity = entities[ent[objs[x][0]]]
            obj = entity.cymunk_physics.body

            entity = entities[ent[objs[x][1]]]
            obj2 = entity.cymunk_physics.body


            anchr1 = (anch[x][0]*scale, anch[x][1]*scale)
            anchr2 = (anch[x][2]*scale, anch[x][3]*scale)


            joint = PivotJoint(obj, obj2,
                                anchr1,
                                anchr2)
            physics.space.add_constraint(joint)

        self.consnum = len(physics.space.constraints)

    def cameramove(self, once):
        rotation = self.gameworld.system_manager['rotation']
        rotation.camerastate = self.camerastate

    def cameraalert(self, once):
        entities = self.gameworld.entities
        entity = entities[ent['camera']]
        renderer = entity.rotate_color_scale_renderertop
        renderer.texture_key = 'camera2'

        rotation = self.gameworld.system_manager['rotation']
        rotation.caught = True
        self.caught = True

    def camerastateup(self, space, arbiter):
        if arbiter.is_first_contact:
            body = arbiter.shapes[0].body
            body.velocity = (0, 0)
            self.camerastate = 'up'
            Clock.schedule_once(self.cameramove)

        return False

    def camerastatedown(self, space, arbiter):
        if arbiter.is_first_contact:
            body = arbiter.shapes[0].body
            body.velocity = (0, 0)
            self.camerastate = 'down'
            Clock.schedule_once(self.cameramove)


        return False

    def cameralightstriker(self, space, arbiter):
        if not self.caught:
            Clock.schedule_once(self.cameraalert)

        return False

    def camerastriker(self, space, arbiter):

        if not self.caught:
            Clock.schedule_once(self.cameraalert)

        return True

    def lv3(self, *args):

        self.rollbacklevelselect()
        self.nametimer = Clock.schedule_once(self.rollbackname, 2)

        self.more_force = True
        sysbox.append('boundary')

        self.closebutton.pos = ((880*scale)+wscale, (517*scale)+hscale)

        entities = self.gameworld.entities

        touch = self.gameworld.system_manager['cymunk_touch']
        ignore = range(1, 85)
        ignore.remove(4)
        touch.ignore_groups = ignore

        physics = self.gameworld.system_manager['cymunk_physics']
        physics.damping = 0.5

        boundary = self.gameworld.system_manager['boundary']
        boundary.shut = 1
        boundary.level = 3
        self.level = 3

        emitter_system = self.ids.emitter
        emitter_system.add_effect(ent['striker'], 'strikereffects')


        objs = ['areabound', 'timeline', 'segtex', 'screentex', 'closex',
                'name3']
        pos = [(475, 224), (475, 224),
               (800, 500), (475, 293.5),
               (925, 562), (150, 520)]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            areaboundpos = entity.position
            areaboundpos.pos = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)

        #segs
        objs = ['seg', 'seg2', 'seg3', 'seg4', 'seg5', 'seg6', 'seg7', 'seg8',
                'screen4', 'screen7', 'screen8', 'screen9', 'screen10', 'screen11',
                'vertsupport', 'vertsupport2', 'horsupport', 'horsupport2',
                'slit',
                'striker',
                'goal',
                'magicball',
                'ropesupport', 'ropesupport2',
                'ropestopper']
        pos = [(800, 540), (800, 460), (760, 500), (840, 500),
               (772, 528), (772, 472), (828, 472), (828, 528),

               (475, 5), (5, 115), (945, 115),
               (5, 408.5), (945, 408.5), (475, 582),

               (-20, 293.5), (970,293.5),
               (475, -20), (475,607),

               (475, 274),
               (400, 100),
               (800, 500),
               (200, 500),
               (-20, 525), (970, 385),
               (800, 450)]

        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)
            physics.space.reindex_shape(shape[0])


        #rope
        posz = [35, 85, 135, 185, 235, 285, 335, 385, 435, 485, 535, 585, 635, 685, 735, 785, 835, 885, 935, 985]
        posy = [475, 465, 455, 445, 435, 425, 415, 405, 395, 385, 375, 365, 355, 345, 335, 325, 315, 305, 295, 285]
        rope = ['rope', 'rope2', 'rope3', 'rope4', 'rope5', 'rope6', 'rope7', 'rope8', 'rope9', 'rope10', 'rope11',
                'rope12', 'rope13', 'rope14', 'rope15', 'rope16', 'rope17', 'rope18', 'rope19', 'rope20']
        for x in range(len(posz)):
            entity = entities[ent[rope[x]]]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = ((posz[x]*scale)+wscale, (posy[x] *scale)+hscale)
            physics.space.reindex_shape(shape[0])
            body.reset_forces()
            body.velocity = (0, 0)
            body.angular_velocity = 0
            body.angle = 0


        objs = [('ropesupport', 'rope'), ('ropesupport2', 'rope20'),]
        anch = [((30), (0), (-25), (0)), ((-30), (0), (25), (0)),]
        for x in range(len(objs)):
            entity = entities[ent[objs[x][0]]]
            obj = entity.cymunk_physics.body

            entity = entities[ent[objs[x][1]]]
            obj2 = entity.cymunk_physics.body


            anchr1 = (anch[x][0]*scale, anch[x][1]*scale)
            anchr2 = (anch[x][2]*scale, anch[x][3]*scale)


            joint = PivotJoint(obj, obj2,
                                anchr1,
                                anchr2)
            physics.space.add_constraint(joint)

        rope = [('rope', 'rope2'), ('rope2', 'rope3'), ('rope3', 'rope4'), ('rope4', 'rope5'), ('rope5', 'rope6'),
                ('rope6', 'rope7'), ('rope7', 'rope8'), ('rope8', 'rope9'), ('rope9', 'rope10'), ('rope10', 'rope11'),
                ('rope11', 'rope12'), ('rope12', 'rope13'), ('rope13', 'rope14'), ('rope14', 'rope15'),
                ('rope15', 'rope16'), ('rope16', 'rope17'), ('rope17', 'rope18'), ('rope18', 'rope19'),
                ('rope19', 'rope20')]

        for x in range(len(rope)):
            entity = entities[ent[rope[x][0]]]
            body = entity.cymunk_physics.body

            entity = entities[ent[rope[x][1]]]
            body2 = entity.cymunk_physics.body

            anchr1 = (25*scale, 0*scale)
            anchr2 = (-25*scale, 0*scale)

            joint = PivotJoint(body, body2,
                                anchr1,
                                anchr2)
            physics.space.add_constraint(joint)

        touch.paused = False
        physics.paused = False
        sysbox.append('cymunk_physics')
        sysbox.append('cymunk_touch')

        boundary.magicforce = True

        self.consnum = len(physics.space.constraints)

        boundary.objs = ['striker',]
        boundary.objs2 = ['magicball']
        boundary.objs3 = ['rope', 'rope2', 'rope3', 'rope4', 'rope5', 'rope6', 'rope7', 'rope8',
        'rope9', 'rope10', 'rope11', 'rope12', 'rope13', 'rope14', 'rope15', 'rope16',
        'rope17', 'rope18', 'rope19', 'rope20',]
        boundary.paused = False

    def magicballwalltop(self, space, arbiter):
        if arbiter.is_first_contact:
            boundary = self.gameworld.system_manager['boundary']
            boundary.magicforce = False
            self.hittop = True


        return True

    def magicballwallside(self, space, arbiter):
        if arbiter.is_first_contact:
            boundary = self.gameworld.system_manager['boundary']
            boundary.magicforce = False
            self.hitside = True


        return True

    def magicballwall2(self, space, arbiter):
        if arbiter.is_first_contact:
            boundary = self.gameworld.system_manager['boundary']
            boundary.magicforce = False
            Clock.schedule_once(self.wakethegoal)


        return True

    def lv4(self, *args):

        self.rollbacklevelselect()
        self.nametimer = Clock.schedule_once(self.rollbackname, 2)

        self.more_force = True
        sysbox.append('boundary')

        self.closebutton.pos = ((880*scale)+wscale, (517*scale)+hscale)

        entities = self.gameworld.entities

        touch = self.gameworld.system_manager['cymunk_touch']
        ignore = range(1, 85)
        ignore.remove(4)
        touch.ignore_groups = ignore

        physics = self.gameworld.system_manager['cymunk_physics']
        physics.damping = 0.5

        boundary = self.gameworld.system_manager['boundary']
        boundary.shut = 1
        boundary.level = 4
        self.level = 4

        emitter_system = self.ids.emitter
        emitter_system.add_effect(ent['striker'], 'strikereffects')


        objs = ['areabound2', 'timeline2', 'segtex', 'screentex',
                'basketkit', 'closex', 'name4']
        pos = [(363, 293.5), (363, 102),
               (820,  150), (475, 293.5),
               (870, 400), (925, 562),
               (135, 520)]


        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            areaboundpos = entity.position
            areaboundpos.pos = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)

        #segs
        objs = ['seg', 'seg2', 'seg3', 'seg4', 'seg5', 'seg6', 'seg7', 'seg8',
                'screen4', 'screen7', 'screen8', 'screen9', 'screen10', 'screen11',
                'vertsupport', 'vertsupport2', 'horsupport', 'horsupport2',
                'basket1', 'basket2', 'basket3', 'basket4', 'basket5',
                'basketedge', 'basketedge2',
                'slit3',
                'striker',
                'goal',
                'nethook', 'nethook2', 'nethook3', 'nethook4', 'nethook5',]

        pos = [(820, 190), (820, 110), (780, 150), (860, 150),
               (792, 178), (792, 122), (848, 122), (848, 178),

               (475, 5), (5, 115), (945, 115),
               (5, 408.5), (945, 408.5), (475, 582),

               (-20, 293.5), (970, 293.5),
               (475, -20), (475, 607),

               (937, 373), (906, 373), (873, 400),
               (862, 373), (855, 374),

               (800, 375), (845, 375),

               (395, 293.5),

               (150, 100),
               (820,  150),

               (807.3, 373), (814.9, 373), (822.5, 373), (830.1, 373), (837.7, 373),]

        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)
            physics.space.reindex_shape(shape[0])



        #net
        objs = ['net', 'net2', 'net3', 'net4', 'net5', 'net6', 'net7', 'net8', 'net9', 'net10',

                'innet', 'innet2', 'innet3', 'innet4',
                'innet5', 'innet6', 'innet7', 'innet8',
                'innet9', 'innet10', 'innet11',
                'innet12', 'innet13','innet14', 'innet15', 'innet16',
                'innet17', 'innet18',
                'innet19', 'innet20','innet21', 'innet22', 'innet23', 'innet24',
                'innet25','innet26', 'innet27', 'innet28', 'innet29',
                'innet30', 'innet31', 'innet32',
                'innet33','innet34', 'innet35', 'innet36', 'innet37', 'innet38',
                'innet39', 'innet40',
                'innethor', 'innethor2', 'innethor3',]

        pos = [(800, 368), (800, 360), (800, 352), (800, 344), (800, 336),
               (845, 368), (845, 360), (845, 352), (845, 344), (845, 336),

               (822.5, 368), (822.5, 360), (822.5, 352), (822.5, 344),
               (822.5, 368), (822.5, 360), (822.5, 352), (822.5, 344),

               (814.9, 368), (814.9, 360), (814.9, 352),
               (814.9, 368), (814.9, 360), (814.9, 352), (814.9, 344), (814.9, 336),

               (807.3, 368), (807.3, 360),
               (807.3, 368), (807.3, 360), (807.3, 352), (807.3, 344), (807.3, 336), (807.3, 328),

               (830.1, 368), (830.1, 360), (830.1, 352), (830.1, 344),  (830.1, 336),
               (830.1, 368), (830.1, 360), (830.1, 352),

               (837.7, 368), (837.7, 360), (837.7, 352), (837.7, 344), (837.7, 336), (837.7, 328),
               (837.7, 368), (837.7, 360),

               (817.5, 336), (822.5, 336), (827.5, 336)]

        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)
            physics.space.reindex_shape(shape[0])
            body.reset_forces()
            body.velocity = (0, 0)
            body.angular_velocity = 0
            body.angle = 0

    #lv4
        objs = [('basketedge', 'net'), ('basketedge2', 'net6')]
        for x in range(len(objs)):
            entity = entities[ent[objs[x][0]]]
            basketedge = entity.cymunk_physics.body
            entity = entities[ent[objs[x][1]]]
            net = entity.cymunk_physics.body


            anchr1 = (0*scale, 0*scale)
            anchr2 = (0*scale, 4*scale)


            basketnet = PivotJoint(basketedge, net,
                                anchr1,
                                anchr2)
            physics.space.add_constraint(basketnet)

    #net
        objs = [('net', 'net2'), ('net2', 'net3'), ('net3', 'net4'), ('net4', 'net5'),
                ('net6', 'net7'), ('net7', 'net8'), ('net8', 'net9'), ('net9', 'net10')]
        for x in range(len(objs)):
            entity = entities[ent[objs[x][0]]]
            basketedge = entity.cymunk_physics.body
            entity = entities[ent[objs[x][1]]]
            net = entity.cymunk_physics.body


            anchr1 = (0*scale, -4*scale)
            anchr2 = (0*scale, 4*scale)


            basketnet = PivotJoint(basketedge, net,
                                anchr1,
                                anchr2)
            physics.space.add_constraint(basketnet)

    #balancer
        objs = [('nethook3', 'innet'), ('nethook3', 'innet5'),
                ('nethook2', 'innet9'), ('nethook2', 'innet12'),
                ('nethook', 'innet17'), ('nethook', 'innet19'),
                ('nethook4', 'innet25'), ('nethook4', 'innet30'),
                ('nethook5', 'innet33'), ('nethook5', 'innet39')]
        for x in range(len(objs)):
            entity = entities[ent[objs[x][0]]]
            basketedge = entity.cymunk_physics.body
            entity = entities[ent[objs[x][1]]]
            net = entity.cymunk_physics.body


            anchr1 = (0*scale, 0*scale)
            anchr2 = (0*scale, 4*scale)


            basketnet = PivotJoint(basketedge, net,
                                anchr1,
                                anchr2)
            physics.space.add_constraint(basketnet)



    #balancer
        objs = [('innet', 'innet2'), ('innet2', 'innet3'), ('innet3', 'innet4'),
                ('innet5', 'innet6'), ('innet6', 'innet7'), ('innet7', 'innet8'),
                ('innet9', 'innet10'), ('innet10', 'innet11'),
                ('innet12', 'innet13'), ('innet13', 'innet14'), ('innet14', 'innet15'), ('innet15', 'innet16'),
                ('innet17', 'innet18'),
                ('innet19', 'innet20'), ('innet20', 'innet21'), ('innet21', 'innet22'), ('innet22', 'innet23'), ('innet23', 'innet24'),
                ('innet25', 'innet26'), ('innet26', 'innet27'), ('innet27', 'innet28'), ('innet28', 'innet29'),
                ('innet30', 'innet31'), ('innet31', 'innet32'),
                ('innet33', 'innet34'), ('innet34', 'innet35'), ('innet35', 'innet36'), ('innet36', 'innet37'), ('innet37', 'innet38'),
                ('innet39', 'innet40')]
        for x in range(len(objs)):
            entity = entities[ent[objs[x][0]]]
            basketedge = entity.cymunk_physics.body
            entity = entities[ent[objs[x][1]]]
            net = entity.cymunk_physics.body


            anchr1 = (0*scale, -4*scale)
            anchr2 = (0*scale, 4*scale)


            basketnet = PivotJoint(basketedge, net,
                                anchr1,
                                anchr2)
            physics.space.add_constraint(basketnet)


    #balancer
        objs = [('net3', 'innet4'), ('net8', 'innet8'),
                ('net2', 'innet11'), ('net9', 'innet16'),
                ('net', 'innet18'), ('net10', 'innet24'),
                ('net4', 'innet29'), ('net7', 'innet32'),
                ('net5', 'innet38'), ('net6', 'innet40')]
        for x in range(len(objs)):
            entity = entities[ent[objs[x][0]]]
            basketedge = entity.cymunk_physics.body
            entity = entities[ent[objs[x][1]]]
            net = entity.cymunk_physics.body


            anchr1 = (0*scale, 0*scale)
            anchr2 = (0*scale, -4*scale)


            basketnet = PivotJoint(basketedge, net,
                                anchr1,
                                anchr2)
            physics.space.add_constraint(basketnet)

    #balancer
        objs = [('innethor', 'innethor2'), ('innethor2', 'innethor3')]
        for x in range(len(objs)):
            entity = entities[ent[objs[x][0]]]
            basketedge = entity.cymunk_physics.body
            entity = entities[ent[objs[x][1]]]
            net = entity.cymunk_physics.body


            anchr1 = (5*scale, 0*scale)
            anchr2 = (-5*scale, 0*scale)


            basketnet = PivotJoint(basketedge, net,
                                anchr1,
                                anchr2)
            physics.space.add_constraint(basketnet)


    #balancer
        objs = [('innethor', 'net5')]
        for x in range(len(objs)):
            entity = entities[ent[objs[x][0]]]
            basketedge = entity.cymunk_physics.body
            entity = entities[ent[objs[x][1]]]
            net = entity.cymunk_physics.body


            anchr1 = (-5*scale, 0*scale)
            anchr2 = (0*scale, 0*scale)


            basketnet = PivotJoint(basketedge, net,
                                anchr1,
                                anchr2)
            physics.space.add_constraint(basketnet)

    #balancer
        objs = [('innethor3', 'net10')]
        for x in range(len(objs)):
            entity = entities[ent[objs[x][0]]]
            basketedge = entity.cymunk_physics.body
            entity = entities[ent[objs[x][1]]]
            net = entity.cymunk_physics.body


            anchr1 = (5*scale, 0*scale)
            anchr2 = (0*scale, 0*scale)


            basketnet = PivotJoint(basketedge, net,
                                anchr1,
                                anchr2)
            physics.space.add_constraint(basketnet)

    #balancer
        objs = [('innet2', 'innet13'), ('innet6', 'innet26'),
                ('innet10', 'innet20'), ('innet31', 'innet34'),
                ('innet3', 'innet21'), ('innet7', 'innet35'),
                ('innet14', 'innet27'), ]
        for x in range(len(objs)):
            entity = entities[ent[objs[x][0]]]
            basketedge = entity.cymunk_physics.body
            entity = entities[ent[objs[x][1]]]
            net = entity.cymunk_physics.body


            anchr1 = (0*scale, 0*scale)
            anchr2 = (0*scale, 0*scale)


            basketnet = PivotJoint(basketedge, net,
                                anchr1,
                                anchr2,)
            physics.space.add_constraint(basketnet)

        self.consnum = len(physics.space.constraints)


        touch.paused = False
        physics.paused = False
        sysbox.append('cymunk_physics')
        sysbox.append('cymunk_touch')


        boundary.objs = ['striker']
        boundary.objs2 = ['net', 'net2', 'net3', 'net4', 'net5',
            'net6', 'net7', 'net8', 'net9', 'net10',
            'innet', 'innet2', 'innet3', 'innet4',
            'innet5', 'innet6', 'innet7', 'innet8',
            'innet9', 'innet10', 'innet11',
            'innet12', 'innet13','innet14', 'innet15', 'innet16',
            'innet17', 'innet18',
            'innet19', 'innet20','innet21', 'innet22', 'innet23', 'innet24',
            'innet25','innet26', 'innet27', 'innet28', 'innet29',
            'innet30', 'innet31', 'innet32',
            'innet33','innet34', 'innet35', 'innet36', 'innet37', 'innet38',
            'innet39', 'innet40',
            'innethor', 'innethor2', 'innethor3',]

        boundary.paused = False

    def basketsuccess(self, space, arbiter):
        if arbiter.is_first_contact:
            self.basket = True

    def lv5(self, *args):

        self.rollbacklevelselect()
        self.nametimer = Clock.schedule_once(self.rollbackname, 2)

        self.more_force = True
        self.five = False

        self.closebutton.pos = ((880*scale)+wscale, (517*scale)+hscale)

        entities = self.gameworld.entities

        touch = self.gameworld.system_manager['cymunk_touch']
        ignore = range(1, 85)
        ignore.remove(4)
        touch.ignore_groups = ignore

        physics = self.gameworld.system_manager['cymunk_physics']
        physics.damping = 0.5

        boundary = self.gameworld.system_manager['boundary']
        boundary.shut = 1
        boundary.level = 5
        self.level = 5

        emitter_system = self.ids.emitter
        emitter_system.add_effect(ent['striker'], 'strikereffects')
        emitter_system.add_effect(ent['light'], 'teleporteffects')
        emitter_system.add_effect(ent['light2'], 'teleport2effects')



        objs = ['areabound', 'timeline', 'segtex', 'lv5screen', 'closex',
                'name5']
        pos = [(-158, 224), (-158, 224),
               (800,  475), (475, 293.5),
               (925, 562), (100, 520)]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            areaboundpos = entity.position
            areaboundpos.pos = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)

        #screen
        objs = ['screen4', 'screen7', 'screen8', 'screen9', 'screen10', 'screen11',
                'sc5', 'sc5_3', 'sc5_4', 'sc5_2', 'sc5_5',
                'sc5_6', 'sc5_7', 'sc5_8', 'sc5_9', 'sc5_10', 'sc5_11',
                'seg', 'seg2', 'seg3', 'seg4', 'seg5', 'seg6', 'seg7', 'seg8',
                'striker',
                'goal',
                'slit',
                'light',
                'light2',
                'teleblocker']
        pos = [(475, 5), (5, 115), (945, 115),
               (5, 408.5), (945, 408.5), (475, 582),

               (322, 553.5), (322, 289.5), (639, 517.5), (639, 253.5),
               (629, 224.5), (342, 296.5), (633, 244.5), (322, 521.5),
               (322, 367.5), (639, 439.5), (639, 285.5),

               (800, 515), (800, 435), (760, 475), (840, 475),
               (772, 503), (772, 447), (828, 447), (828, 503),

               (475, 100),
               (800, 475),
               (475, 274),
               (322, 444),
               (639, 362),
               (603, 362)]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)
            physics.space.reindex_shape(shape[0])


        self.portlist = range(371, 518)
        self.portlist2 = range(290, 436)
        self.portlist.reverse()

        touch.paused = False
        physics.paused = False
        sysbox.append('cymunk_physics')
        sysbox.append('cymunk_touch')

    def teleport(self, once):
        entities = self.gameworld.entities
        physics = self.gameworld.system_manager['cymunk_physics']

        try:
            entity = entities[ent['striker']]
            body = entity.cymunk_physics.body
            num = int(body.position[1])
            num = (float(num)-hscale)/scale
            num = round(num)

            for x in self.portlist:
                if x == num:
                    numin = self.portlist.index(x)
                    numin += 1

            newpos = self.portlist2[numin]

            body.position = ((660 *scale)+wscale, (newpos*scale)+hscale)
        except:
            pass

    def strikerlight(self, space, arbiter):
        if arbiter.is_first_contact:
            Clock.schedule_once(self.teleport)

    def lv6(self, *args):

        self.rollbacklevelselect()
        self.nametimer = Clock.schedule_once(self.rollbackname, 2)

        self.more_force = True
        sysbox.append('boundary')

        self.closebutton.pos = ((880*scale)+wscale, (517*scale)+hscale)

        entities = self.gameworld.entities

        touch = self.gameworld.system_manager['cymunk_touch']
        ignore = range(1, 85)
        ignore.remove(4)
        touch.ignore_groups = ignore

        physics = self.gameworld.system_manager['cymunk_physics']
        physics.damping = 0.5

        boundary = self.gameworld.system_manager['boundary']
        boundary.shut = 1
        boundary.level = 6
        self.level = 6

        emitter_system = self.ids.emitter
        emitter_system.add_effect(ent['striker'], 'strikereffects')

        objs = ['areabound', 'timeline', 'segtex', 'lv6screen', 'closex',
                'name6']
        pos = [(-5, 224), (-5, 224),
               (600, 300), (475, 293.5),
               (925, 562), (120, 520)]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            areaboundpos = entity.position
            areaboundpos.pos = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)


        objs = ['screen4', 'screen7', 'screen8', 'screen9', 'screen10', 'screen11',
                'sc6', 'sc6_2', 'sc6_3', 'sc6_4',
                'seg', 'seg2', 'seg3', 'seg4', 'seg5', 'seg6', 'seg7', 'seg8',
                'goal',
                'slit',
                'striker',

                'supporter', 'supporter2',]


        pos = [(475, 5), (5, 115), (945, 115),
               (5, 408.5), (945, 408.5), (475, 582),

               (475, 344.5), (708, 224.5),
               (495, 349), (713, 244),

               (600, 340), (600, 260), (560, 300), (640, 300),
               (572, 328), (572, 272), (628, 272), (628, 328),

               (600, 300),
               (475, 274),
               (400, 100),
               (400, 456.5), (550, 455.5),]


        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)
            physics.space.reindex_shape(shape[0])



        objs = ['cart', 'topbar',]
        pos = [(470, 506.5), (475, 469.5),]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            body = entity.cymunk_physics.body
            body.reset_forces()
            body.velocity = (0, 0)
            body.angular_velocity = 0
            body.angle = 0
            shape = entity.cymunk_physics.shapes
            body.position = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)
            for x in shape:
                physics.space.reindex_shape(x)


        objs = ['cartwheel',
                'brick','brick2','brick3', 'brick4', 'brick5', 'brick6', 'brick7', 'brick8', 'brick9',
                'leftweight', 'rightweight',]
        pos = [(510, 491.5),
               (461, 514), (475.5, 514), (490, 514),
               (461, 523), (475.5, 523), (490, 523),
               (468, 532), (482.5, 532), (475, 541),
               (400, 459.5), (550, 459.5),]

        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            body = entity.cymunk_physics.body
            body.reset_forces()
            body.velocity = (0, 0)
            body.angular_velocity = 0
            body.angle = 0
            shape = entity.cymunk_physics.shapes
            body.position = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)
            physics.space.reindex_shape(shape[0])



        objs = [('cart', 'cartwheel'),
                ('sc6', 'topbar'),
                ('leftweight', 'topbar'), ('rightweight', 'topbar'),]

        anch = [((40), (-15), (0), (0)),
                ((0), (125), (0), (0)),
                ((0), (0), (-75), (-10)), ((0), (0), (75), (-10)),]

        for x in range(len(objs)):
            entity = entities[ent[objs[x][0]]]
            obj = entity.cymunk_physics.body

            entity = entities[ent[objs[x][1]]]
            obj2 = entity.cymunk_physics.body


            anchr1 = (anch[x][0]*scale, anch[x][1]*scale)
            anchr2 = (anch[x][2]*scale, anch[x][3]*scale)


            joint = PivotJoint(obj, obj2,
                                anchr1,
                                anchr2)
            physics.space.add_constraint(joint)


        boundary.objs = ['striker',]
        boundary.objs2 = ['topbar', 'cart', 'cartwheel',
                          'brick', 'brick2', 'brick3', 'brick4',
                         'brick5', 'brick6','brick7', 'brick8', 'brick9',
                          'leftweight', 'rightweight']
        boundary.paused = False

        self.consnum = len(physics.space.constraints)


        touch.paused = False
        physics.paused = False
        sysbox.append('cymunk_physics')
        sysbox.append('cymunk_touch')

    def removesupport(self, once):
        entities = self.gameworld.entities
        physics = self.gameworld.system_manager['cymunk_physics']

        #supporters
        objs = ['supporter', 'supporter2']
        pos = [(3040, 1800), (3055, 1800)]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = (pos[x][0] *scale, pos[x][1]*scale)
            physics.space.reindex_shape(shape[0])
        self.remsupport = True

    def strikercartopbar(self, space, arbiter):
        if arbiter.is_first_contact:
            if not self.remsupport:
                Clock.schedule_once(self.removesupport)

        return True

    def lv7(self, *args):

        self.rollbacklevelselect()
        self.nametimer = Clock.schedule_once(self.rollbackname, 2)
        self.level = 7
        self.successcheckcalled = False
        sysbox.append('boundary')
        self.closebutton.pos = ((880*scale)+wscale, (517*scale)+hscale)

        entities = self.gameworld.entities

        touch = self.gameworld.system_manager['cymunk_touch']
        ignore = range(1, 85)
        ignore.remove(20)
        # ignore.remove(33)
        touch.ignore_groups = ignore

        physics = self.gameworld.system_manager['cymunk_physics']

        emitter_system = self.ids.emitter
        emitter_system.add_effect(ent['cannonball'], 'cneffects')
        emitter_system.add_effect(ent['cannonball2'], 'cneffects2')
        emitter_system.add_effect(ent['cannonball3'], 'cneffects3')
        emitter_system.add_effect(ent['cannonball4'], 'cneffects4')

        boundary = self.gameworld.system_manager['boundary']
        boundary.level = 7


        objs = ['lv9screen', 'texcnn',
                'segtex', 'segtex2', 'segtex3', 'segtex4',
                'areabound', 'timeline', 'closex', 'name7']

        pos = [(475, 293.5), (33, 120),
               (190, 450), (380, 450),
               (570, 450), (760, 450),
               (475, 5), (475, 5),
               (925, 562), (130, 520)]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            areaboundpos = entity.position
            areaboundpos.pos = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)

        #segs
        objs = ['seg', 'seg2', 'seg3', 'seg4', 'seg5', 'seg6', 'seg7', 'seg8',
                'seg9', 'seg10', 'seg11', 'seg12', 'seg13', 'seg14', 'seg15', 'seg16',
                'seg17', 'seg18', 'seg19', 'seg20', 'seg21', 'seg22', 'seg23', 'seg24',
                'seg25', 'seg26', 'seg27', 'seg28', 'seg29', 'seg30', 'seg31', 'seg32',
                'screen', 'screen2', 'screen3', 'screen4',
                'cannon', 'cannon2',
                'sensor',
                'batholder',
                'cgoal', 'cgoal2', 'cgoal3', 'cgoal4']

        pos = [(190, 490), (190, 410), (150, 450), (230, 450),
               (162, 478), (162, 422), (218, 422), (218, 478),

               (380, 490), (380, 410), (340, 450), (420, 450),
               (352, 478), (352, 422), (408, 422), (408, 478),

               (570, 490), (570, 410), (530, 450), (610, 450),
               (542, 478), (542, 422), (598, 422), (598, 478),

               (760, 490), (760, 410), (720, 450), (800, 450),
               (732, 478), (732, 422), (788, 422), (788, 478),

               (5, 293.5), (945, 293.5),
               (475, 582), (475, 5),

               (35, 141), (35, 99),
               (940, 120),
               (475, 47),

               (190, 450), (380, 450),
               (570, 450), (760, 450)]

        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)
            physics.space.reindex_shape(shape[0])


        #bat
        objs = ['bat']
        pos = [((475 *scale)+wscale, (85 *scale)+hscale)]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = pos[x]
            for x in shape:
                physics.space.reindex_shape(x)
            body.reset_forces()
            body.angle = 0
            body.velocity = (0, 0)
            body.angular_velocity = 0

        objs = [('batholder', 'bat')]
        anch = [((0), (37), (0), (0))]
        for x in range(len(objs)):
            entity = entities[ent[objs[x][0]]]
            obj = entity.cymunk_physics.body

            entity = entities[ent[objs[x][1]]]
            obj2 = entity.cymunk_physics.body


            anchr1 = (anch[x][0]*scale, anch[x][1]*scale)
            anchr2 = (anch[x][2]*scale, anch[x][3]*scale)


            joint = PivotJoint(obj, obj2,
                                anchr1,
                                anchr2)
            physics.space.add_constraint(joint)

        self.consnum = len(physics.space.constraints)


        touch.paused = False
        physics.paused = False
        sysbox.append('cymunk_physics')
        sysbox.append('cymunk_touch')

        boundary.objs = ['bat']
        boundary.paused = False

        self.cantime = Clock.schedule_once(self.rollball, 2)
        self.cantime2 = Clock.schedule_once(self.rollball, 10)
        self.cantime3 = Clock.schedule_once(self.rollball, 18)
        self.cantime4 = Clock.schedule_once(self.rollball, 26)
        # self.cantime5 = Clock.schedule_once(self.successcheck, 50)
        self.timer = Clock.schedule_interval(self.movetimeline, 1)

    def rollball(self, once):
        entities = self.gameworld.entities
        physics = self.gameworld.system_manager['cymunk_physics']
        boundary = self.gameworld.system_manager['boundary']

        #striker

        pos = [((50 *scale)+wscale, (120 *scale)+hscale)]
        objs = [self.ball[0]]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = pos[x]
            physics.space.reindex_shape(shape[0])

        if not self.more_force:
            mag = 30
            force = (425*mag, 0)
            r = (0, 10*scale)
            body.apply_impulse(force, r)

            mag = 5
            force = (425*mag, 0)
            r = (0, 10*scale)
            body.apply_force(force, r)
        else:
            mag = 35
            force = (425*mag, 0)
            r = (0, 10*scale)
            body.apply_impulse(force, r)

            mag = 15
            force = (425*mag, 0)
            r = (0, 10*scale)
            body.apply_force(force, r)



        del self.ball[0]

    def successcheck(self, *args):
        if self.scgoal and self.scgoal2 and self.scgoal3 and self.scgoal4:
            self.fintime = self.count
            self.successbtn = True
            self.successchecktimer = Clock.schedule_once(self.controlsscreen, 2)
            self.successcheckcalled = True

    def improvise(self, body, body2):
        b = self.gameworld.system_manager['boundary']
        bodies = (body, body2)
        if not self.successcheckcalled:
            for x in bodies:
                if x == ent['cgoal']:
                    if 'cgoal' not in b.objs3:
                        b.paused = True
                        b.objs3.append('cgoal')
                        b.paused = False
                        self.scgoal = True
                        self.successcheck()
                        if self.dovibrate:
                            Clock.schedule_once(self.do_vibrate)

                elif x == ent['cgoal2']:
                    if 'cgoal2' not in b.objs3:
                        b.paused = True
                        b.objs3.append('cgoal2')
                        b.paused = False
                        self.scgoal2 = True
                        self.successcheck()
                        if self.dovibrate:
                            Clock.schedule_once(self.do_vibrate)

                elif x == ent['cgoal3']:
                    if 'cgoal3' not in b.objs3:
                        b.paused = True
                        b.objs3.append('cgoal3')
                        b.paused = False
                        self.scgoal3 = True
                        self.successcheck()
                        if self.dovibrate:
                            Clock.schedule_once(self.do_vibrate)

                elif x == ent['cgoal4']:
                    if 'cgoal4' not in b.objs3:
                        b.paused = True
                        b.objs3.append('cgoal4')
                        b.paused = False
                        self.scgoal4 = True
                        self.successcheck()
                        if self.dovibrate:
                            Clock.schedule_once(self.do_vibrate)

                elif x == ent['cannonball']:
                    if 'cannonball' not in b.objs3:
                        b.paused = True
                        b.objs3.append('cannonball')
                        b.paused = False

                elif x == ent['cannonball2']:
                    if 'cannonball2' not in b.objs3:
                        b.paused = True
                        b.objs3.append('cannonball2')
                        b.paused = False

                elif x == ent['cannonball3']:
                    if 'cannonball3' not in b.objs3:
                        b.paused = True
                        b.objs3.append('cannonball3')
                        b.paused = False

                elif x == ent['cannonball4']:
                    if 'cannonball4' not in b.objs3:
                        b.paused = True
                        b.objs3.append('cannonball4')
                        b.paused = False

    def cgoalstocannoballs(self, space, arbiter):
        if arbiter.is_first_contact:
            boundary = self.gameworld.system_manager['boundary']
            body = arbiter.shapes[0].body
            body2 = arbiter.shapes[1].body
            Clock.schedule_once(lambda x:self.improvise(body.data, body2.data))


            # if 'cgoal4' not in boundary.objs3:
            #     boundary.objs3.append('cgoal4')
            #
            # if body.data == ent['cannonball']:
            #     Clock.schedule_once(self.stopstrikerforce)
            # elif body.data == ent['cannonball2']:
            #     Clock.schedule_once(self.stopstriker2force)
            # elif body.data == ent['cannonball3']:
            #     Clock.schedule_once(self.stopstriker3force)
            # elif body.data == ent['cannonball4']:
            #     Clock.schedule_once(self.stopstriker4force)
            # self.scgoal4 += 1
        return True

    def lv8(self, *args):

        self.rollbacklevelselect()
        self.nametimer = Clock.schedule_once(self.rollbackname, 2)

        self.more_force = True
        sysbox.append('boundary')

        self.closebutton.pos = ((880*scale)+wscale, (517*scale)+hscale)

        self.lv8slit = False
        self.fired = False

        entities = self.gameworld.entities

        touch = self.gameworld.system_manager['cymunk_touch']
        ignore = range(1, 85)
        ignore.remove(42)
        ignore.remove(43)
        touch.ignore_groups = ignore

        physics = self.gameworld.system_manager['cymunk_physics']
        physics.damping = 0.5

        boundary = self.gameworld.system_manager['boundary']
        boundary.shut = 1
        boundary.level = 8
        self.level = 8

        emitter_system = self.ids.emitter
        emitter_system.add_effect(ent['spstriker'], 'strikereffects')
        emitter_system.add_effect(ent['spstriker2'], 'striker2effects')

        entity = entities[ent['btn1']]
        renderer = entity.rotate_color_scale_renderer2
        renderer.texture_key = 'button1'

        objs = ['areabound', 'timeline', 'segtex', 'lv8screen',
                'Ytex',
                'blanker',
                'btntex', 'closex', 'name8']
        pos = [(846, 224), (846, 224),
               (216, 500), (475, 293.5),

               (200, 243),
               (200, 105),
               (750, 572), (925, 562),
               (520, 520)]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            areaboundpos = entity.position
            areaboundpos.pos = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)

        #screen
        objs = ['screen4', 'screen7', 'screen8', 'screen9', 'screen10', 'screen11',
                'sc8', 'sc8_2', 'sc8_3', 'sc8_4',
                'sc8_5', 'sc8_6', 'sc8_7', 'sc8_8',
                'slit',
                'y1',
                'y2',
                'y3',
                'spstriker',
                'spstriker2',
                'seg', 'seg2', 'seg3', 'seg4', 'seg5', 'seg6', 'seg7', 'seg8',
                'goal',
                'Ysensor',
                'buttonblocker', 'buttonblocker2', 'buttonblocker3',
                'buttonholder', 'buttonholder2',
                'btn1', 'btn2',
                'barrier2']

        pos = [(475, 5), (5, 115), (945, 115),
               (5, 408.5), (945, 408.5), (475, 582),

               (368, 264.5), (188, 224.5),
               (368, 499.5), (327, 417.5),
               (348, 269.5), (188, 254),
               (349, 499), (322, 436.5),

               (475, 274),
               (170, 310),
               (229, 310),
               (200, 256),
               (400, 100),
               (500, 100),

               (216, 540), (216, 460), (176, 500), (256, 500),
               (188, 528), (188, 472), (244, 472), (244, 528),

               (216, 500),
               (200, 413),
               (714, 586), (786, 586), (750, 640),
               (738, 572), (762, 572),
               (750, 557), (750, 594),
               (475, -1735)]

        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)
            physics.space.reindex_shape(shape[0])

        objs = ['spstriker', 'spstriker2']
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            body = entity.cymunk_physics.body
            body.reset_forces()
            body.angle = 0
            body.velocity = (0, 0)
            body.angular_velocity = 0

        objs = ['bar1', 'bot1', 'bar2', 'bot2']
        pos = [(475, 2265), (475, 2265),
               (475, -1735), (475, -1735)]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)
            physics.space.reindex_shape(shape[0])

        objs = [('btn1', 'btn2'),]
        anch = [((0), (40), (0), (0))]
        for x in range(len(objs)):
            entity = entities[ent[objs[x][0]]]
            obj = entity.cymunk_physics.body

            entity = entities[ent[objs[x][1]]]
            obj2 = entity.cymunk_physics.body


            anchr1 = (anch[x][0]*scale, anch[x][1]*scale)
            anchr2 = (anch[x][2]*scale, anch[x][3]*scale)


            joint = PivotJoint(obj, obj2,
                                anchr1,
                                anchr2)
            physics.space.add_constraint(joint)

        self.consnum = len(physics.space.constraints)


        touch.paused = False
        physics.paused = False
        sysbox.append('cymunk_physics')
        sysbox.append('cymunk_touch')

        boundary.objs = ['spstriker', 'spstriker2']
        boundary.objs2 = ['btn1', 'btn2']
        boundary.paused = False

    def fireY(self, once):
        if not self.fired:
            entities = self.gameworld.entities
            physics = self.gameworld.system_manager['cymunk_physics']

            #Y
            entity = entities[ent['Ynormal']]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = ((200 *scale)+wscale, (243 *scale)+hscale)
            for x in shape:
                physics.space.reindex_shape(x)
            body.reset_forces()
            body.angular_velocity = 0
            body.velocity = (0, 0)
            body.angle = 0

            for x in range(15):
                force = (0, 3000)
                r = (-4*scale, 40*scale)
                body.apply_force(force,r)

                force = (0, 3000)
                r = (4*scale, 40*scale)
                body.apply_force(force,r)

            #Y
            tex = ['y1', 'y2', 'y3']
            for x in range(len(tex)):
                entity = entities[ent[tex[x]]]
                body = entity.cymunk_physics.body
                shape = entity.cymunk_physics.shapes
                body.position = (-2134*scale, 2343.5*scale)
                physics.space.reindex_shape(shape[0])

            #areabound, timeline
            objs = ['Ytex']
            pos = [((2629 *scale)+wscale, (4000 *scale)+hscale)]
            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                areaboundpos = entity.position
                areaboundpos.pos = pos[x]

            rotation = self.gameworld.system_manager['rotation']
            rotation.level = 8
            rotation.systemspeed(.1)
            rotation.paused = False
            self.fired = True

    def stopfiring(self, touch):
        entities = self.gameworld.entities
        physics = self.gameworld.system_manager['cymunk_physics']

        rotation = self.gameworld.system_manager['rotation']
        rotation.paused = True

        #Ynormal
        entity = entities[ent['Ynormal']]
        body = entity.cymunk_physics.body
        shape = entity.cymunk_physics.shapes
        body.position = ((4500 *scale)+wscale, (2027*scale)+hscale)
        for x in shape:
            physics.space.reindex_shape(x)
        body.reset_forces()
        body.velocity = (0,0)
        body.angular_velocity = 0
        body.angle = 0

        #y
        tex = ['y1', 'y2', 'y3']
        pos = [(170, 387), (229, 387),
               (200, 333)]
        for x in range(len(tex)):
            entity = entities[ent[tex[x]]]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)
            physics.space.reindex_shape(shape[0])

            #areabound, timeline
        objs = ['Ytex']
        pos = [((200 *scale)+wscale, (320 *scale)+hscale)]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            areaboundpos = entity.position
            areaboundpos.pos = pos[x]

    def set_cur_str(self, curstr):
        self.cur_str = curstr

    def YnormalYsensor(self, space, arbiter):
        if arbiter.is_first_contact:
            Clock.schedule_once(self.stopfiring)

        return True

    def spstrikersbutton(self, space, arbiter):
        if arbiter.is_first_contact:
            Clock.schedule_once(self.fireY)

        return True

    def lv9(self, *args):

        self.rollbacklevelselect()
        self.nametimer = Clock.schedule_once(self.rollbackname, 2)

        self.more_force = True
        sysbox.append('boundary')

        self.lv9done = False

        entities = self.gameworld.entities

        self.closebutton.pos = ((880*scale)+wscale, (517*scale)+hscale)

        touch = self.gameworld.system_manager['cymunk_touch']
        ignore = range(1, 85)
        ignore.remove(59)
        touch.ignore_groups = ignore

        physics = self.gameworld.system_manager['cymunk_physics']
        physics.damping = 0.2

        boundary = self.gameworld.system_manager['boundary']
        boundary.cancelcall = False
        boundary.shut = 1
        boundary.level = 9
        self.level = 9


        self.posts = [(835, 305.5), (835, 476.5), (604, 425.5),
                      (330, 471.5), (116, 441.5), (113, 267.5)]

        self.posts2 = [(835, 305.5), (835, 476.5), (604, 425.5),
                      (330, 471.5), (116, 441.5), (113, 267.5)]

      #areabound, timeline
        objs = ['lv9screen2', 'areabound', 'timeline', 'closex', 'name9', 'tankguide']
        pos = [(475, 293.5), (475, 5),
               (475, 5), (925, 562),
               (120, 520), (650, 120)]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            areaboundpos = entity.position
            areaboundpos.pos = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)

        #screen
        objs = ['screen', 'screen2', 'screen5', 'screen6',
                'arenahor', 'arenahor2', 'arenahor3', 'arenahor4',
                'arenahorlong', 'arenavert', 'arenavertsmall',
                'gunarch',
                'startpoint',
                'endpoint',
                'gunstopper',
                ]

        pos = [(5, 293.5), (945, 293.5),
               (475, 582), (475, 5),

               (158, 332.5), (497, 391.5),
               (557, 331.5), (798, 375.5),
               (243, 255.5), (188, 334.5),
               (527, 361.5),

               (475, 20),
               (475, 124),
               (475, 282),
               (493, 112),
               (475, 102)]

        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)
            physics.space.reindex_shape(shape[0])



        #gun
        entity = entities[ent['gun']]
        body = entity.cymunk_physics.body
        shape = entity.cymunk_physics.shapes
        body.position = ((475 *scale)+wscale, (82 *scale)+hscale)
        for x in shape:
            physics.space.reindex_shape(x)
        body.reset_forces()
        body.angle = 0
        body.velocity = (0, 0)
        body.angular_velocity = 0

        objs = ['startpoint', 'endpoint', 'gunstopper']
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            body = entity.cymunk_physics.body
            body.reset_forces()
            body.angle = 0
            body.velocity = (0, 0)
            body.angular_velocity = 0

        objs = [('gun', 'endpoint'), ('gun', 'startpoint'),
                ('gunarch', 'gun'),]
        anch = [((0), (200), (0), (0)), ((0), (42), (0), (0)),
                ((0), (24), (0), (-40)),]
        for x in range(len(objs)):
            entity = entities[ent[objs[x][0]]]
            obj = entity.cymunk_physics.body

            entity = entities[ent[objs[x][1]]]
            obj2 = entity.cymunk_physics.body


            anchr1 = (anch[x][0]*scale, anch[x][1]*scale)
            anchr2 = (anch[x][2]*scale, anch[x][3]*scale)


            joint = PivotJoint(obj, obj2,
                                anchr1,
                                anchr2)
            physics.space.add_constraint(joint)

        self.consnum = len(physics.space.constraints)

        touch.paused = False
        physics.paused = False
        sysbox.append('cymunk_physics')
        sysbox.append('cymunk_touch')

        boundary.objs2 = ['gun']
        boundary.paused = False


        Clock.schedule_once(self.goalgen)
        self.timer = Clock.schedule_interval(self.movetimeline, 1)

    def goalgen(self, dt):
        entities = self.gameworld.entities
        physics = self.gameworld.system_manager['cymunk_physics']

        if len(self.posts) != 0:
            newpos = choice(self.posts)
            self.posts.remove(newpos)

            pos = [newpos,
                   (newpos[0], newpos[1]+40), (newpos[0], newpos[1]-40),
                   (newpos[0]-40, newpos[1]), (newpos[0]+40, newpos[1]),
                   (newpos[0]-28, newpos[1]+28), (newpos[0]-28, newpos[1]-28),
                   (newpos[0]+28, newpos[1]-28), (newpos[0]+28, newpos[1]+28),
                   ]

            #ngoal
            objs = ['ngoal', 'seg', 'seg2', 'seg3', 'seg4', 'seg5',
                    'seg6', 'seg7', 'seg8',]

            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                body = entity.cymunk_physics.body
                shape = entity.cymunk_physics.shapes
                body.position = ((pos[x][0]*scale)+wscale, (pos[x][1]*scale)+hscale)
                physics.space.reindex_shape(shape[0])

            entity = entities[ent['ngoal']]
            body = entity.cymunk_physics.body
            body.reset_forces()
            body.velocity = (0, 0)
            body.angular_velocity = 0
            body.angle = 0


          #ab,tl
            objs = ['segtex', 'ab', 'tl', 'nblanker']
            pos = [newpos, (newpos[0], newpos[1]-60), (newpos[0], newpos[1]-60),
                   (newpos[0]-110, newpos[1]-60)]
            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                areaboundpos = entity.position
                areaboundpos.pos = ((pos[x][0]*scale)+wscale, (pos[x][1]*scale)+hscale)
            if self.ntimer:
                self.ntimer.cancel()

            self.ntimer = Clock.schedule_interval(self.movetm, 1)
            self.ncount = 0
            self.ngoalkey = False



        elif len(self.posts) == 0 and not self.double:
            newpos = choice(self.posts2)
            self.posts2.remove(newpos)
            newpos2 = choice(self.posts2)
            self.posts2.remove(newpos2)
            self.double = True
            self.doubletm = True

            pos = [(newpos[0], newpos[1]),
                   (newpos[0], newpos[1]+40), (newpos[0], newpos[1]-40),
                   (newpos[0]-40, newpos[1]), (newpos[0]+40, newpos[1]),
                   (newpos[0]-28, newpos[1]+28), (newpos[0]-28, newpos[1]-28),
                   (newpos[0]+28, newpos[1]-28), (newpos[0]+28, newpos[1]+28),

                   (newpos2[0], newpos2[1]),
                   (newpos2[0], newpos2[1]+40), (newpos2[0], newpos2[1]-40),
                   (newpos2[0]-40, newpos2[1]), (newpos2[0]+40, newpos2[1]),
                   (newpos2[0]-28, newpos2[1]+28), (newpos2[0]-28, newpos2[1]-28),
                   (newpos2[0]+28, newpos2[1]-28), (newpos2[0]+28, newpos2[1]+28),
                   ]

            #ngoal
            objs = ['ngoal', 'seg', 'seg2', 'seg3', 'seg4', 'seg5',
                    'seg6', 'seg7', 'seg8',
                    'ngoal2', 'seg9', 'seg10', 'seg11', 'seg12', 'seg13',
                    'seg14', 'seg15', 'seg16',]

            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                body = entity.cymunk_physics.body
                shape = entity.cymunk_physics.shapes
                body.position = ((pos[x][0]*scale)+wscale, (pos[x][1]*scale)+hscale)
                physics.space.reindex_shape(shape[0])

            entity = entities[ent['ngoal']]
            body = entity.cymunk_physics.body
            body.reset_forces()
            body.velocity = (0, 0)
            body.angular_velocity = 0
            body.angle = 0

            entity = entities[ent['ngoal2']]
            body = entity.cymunk_physics.body
            body.reset_forces()
            body.velocity = (0, 0)
            body.angular_velocity = 0
            body.angle = 0

          #ab,tl
            objs = ['segtex', 'ab', 'tl', 'nblanker',
                    'segtex2', 'ab2', 'tl2', 'nblanker2']
            pos = [newpos, (newpos[0], newpos[1]-60), (newpos[0], newpos[1]-60),
                   (newpos[0]-110, newpos[1]-60),
                   newpos2, (newpos2[0], newpos2[1]-60), (newpos2[0], newpos2[1]-60),
                   (newpos2[0]-110, newpos2[1]-60)]
            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                areaboundpos = entity.position
                areaboundpos.pos = ((pos[x][0]*scale)+wscale, (pos[x][1]*scale)+hscale)
            if self.ntimer:
                self.ntimer.cancel()
            self.ntimer = Clock.schedule_interval(self.movetm, 1)
            self.ncount = 0
            self.ngoalkey = False
            self.ngoal2key = False



        elif len(self.posts) == 0 and self.double:
            if self.ngoalkey and self.ngoal2key:
                if len(self.posts2) == 0:
                    if not self.successbtn:
                        self.successbtn = True
                        self.controlsscreen()
                    self.timer.cancel()
                    self.lv9done = True
                else:
                    newpos = choice(self.posts2)
                    self.posts2.remove(newpos)
                    newpos2 = choice(self.posts2)
                    self.posts2.remove(newpos2)

                    pos = [newpos,
                           (newpos[0], newpos[1]+40), (newpos[0], newpos[1]-40),
                           (newpos[0]-40, newpos[1]), (newpos[0]+40, newpos[1]),
                           (newpos[0]-28, newpos[1]+28), (newpos[0]-28, newpos[1]-28),
                           (newpos[0]+28, newpos[1]-28), (newpos[0]+28, newpos[1]+28),

                           newpos2,
                           (newpos2[0], newpos2[1]+40), (newpos2[0], newpos2[1]-40),
                           (newpos2[0]-40, newpos2[1]), (newpos2[0]+40, newpos2[1]),
                           (newpos2[0]-28, newpos2[1]+28), (newpos2[0]-28, newpos2[1]-28),
                           (newpos2[0]+28, newpos2[1]-28), (newpos2[0]+28, newpos2[1]+28),
                           ]

                    #ngoal
                    objs = ['ngoal', 'seg', 'seg2', 'seg3', 'seg4', 'seg5',
                            'seg6', 'seg7', 'seg8',
                            'ngoal2', 'seg9', 'seg10', 'seg11', 'seg12', 'seg13',
                            'seg14', 'seg15', 'seg16',]

                    for x in range(len(objs)):
                        entity = entities[ent[objs[x]]]
                        body = entity.cymunk_physics.body
                        shape = entity.cymunk_physics.shapes
                        body.position = ((pos[x][0]*scale)+wscale, (pos[x][1]*scale)+hscale)
                        physics.space.reindex_shape(shape[0])

                    entity = entities[ent['ngoal']]
                    body = entity.cymunk_physics.body
                    body.reset_forces()
                    body.velocity = (0, 0)
                    body.angular_velocity = 0
                    body.angle = 0

                    entity = entities[ent['ngoal2']]
                    body = entity.cymunk_physics.body
                    body.reset_forces()
                    body.velocity = (0, 0)
                    body.angular_velocity = 0
                    body.angle = 0

                  #ab,tl
                    objs = ['segtex', 'ab', 'tl', 'nblanker',
                            'segtex2', 'ab2', 'tl2', 'nblanker2']
                    pos = [newpos, (newpos[0], newpos[1]-60), (newpos[0], newpos[1]-60),
                           (newpos[0]-110, newpos[1]-60),
                           newpos2, (newpos2[0], newpos2[1]-60), (newpos2[0], newpos2[1]-60),
                           (newpos2[0]-110, newpos2[1]-60)]
                    for x in range(len(objs)):
                        entity = entities[ent[objs[x]]]
                        areaboundpos = entity.position
                        areaboundpos.pos = ((pos[x][0]*scale)+wscale, (pos[x][1]*scale)+hscale)
                    if self.ntimer:
                        self.ntimer.cancel()
                    self.ntimer = Clock.schedule_interval(self.movetm, 1)
                    self.ncount = 0
                    self.ngoalkey = False
                    self.ngoal2key = False

    def controlgate(self, once):
        self.opengate = True

    def controlgate2(self, once):
        self.opengate2 = True

    def removebullets(self, data):
        entities = self.gameworld.entities
        physics = self.gameworld.system_manager['cymunk_physics']
        entity = entities[data]
        body = entity.cymunk_physics.body
        shape = entity.cymunk_physics.shapes
        body.position = (2000 *scale, 3250 *scale)
        physics.space.reindex_shape(shape[0])

    def revertforceY(self, force, data):
        X = force['x']
        Y = force['y']

        if Y < 0:
            new = abs(Y)*2
            Y = new+Y
        elif Y > 0:
            new = Y*2
            Y = Y-new


        entities = self.gameworld.entities
        entity = entities[data]
        body = entity.cymunk_physics.body
        body.reset_forces()
        force_ = (X,Y)
        body.apply_force(force_)

    def revertforceX(self, force, data):
        X = force['x']
        Y = force['y']

        if X < 0:
            new = abs(X)*2
            X = new+X
        elif X > 0:
            new = X*2
            X = X-new



        entities = self.gameworld.entities
        entity = entities[data]
        body = entity.cymunk_physics.body
        body.reset_forces()
        force_ = (X,Y)
        body.apply_force(force_)

    def ngoaltoseg(self, space, arbiter):
        if arbiter.is_first_contact:
            self.ngoalkey = True
            if self.opengate and not self.lv9done:
                Clock.schedule_once(self.goalgen)
                self.opengate = False
                Clock.schedule_once(self.controlgate, .2)
                if self.dovibrate:
                    Clock.schedule_once(self.do_vibrate)


        return True

    def ngoal2toseg(self, space, arbiter):
        if arbiter.is_first_contact:
            self.ngoal2key = True
            if self.opengate2 and not self.lv9done:
                Clock.schedule_once(self.goalgen)
                self.opengate2 = False
                Clock.schedule_once(self.controlgate2, .2)
                if self.dovibrate:
                    Clock.schedule_once(self.do_vibrate)

        return True

    def screentobullet(self, space, arbiter):
        if arbiter.is_first_contact:
            body = arbiter.shapes[1].body
            Clock.schedule_once(lambda x:self.revertforceX(body.force, body.data))



        return True

    def screentobulletY(self, space, arbiter):
        if arbiter.is_first_contact:
            body = arbiter.shapes[1].body
            Clock.schedule_once(lambda x:self.revertforceY(body.force, body.data))



        return True

    def gunbullets(self, space, arbiter):
        if arbiter.is_first_contact:
            body = arbiter.shapes[1].body
            Clock.schedule_once(lambda x:self.removebullets(body.data))




        return True

    def movetm(self, dt):
        entities = self.gameworld.entities

        if self.ncount >= 10:
            boundary = self.gameworld.system_manager['boundary']
            if self.ntimer:
                self.ntimer.cancel()
            self.ncount = 0
            if not self.successbtn:
                boundary.cancelcall = True
                self.controlsscreen()
                if self.timer:
                    self.timer.cancel()

        else:
            if not self.doubletm:
                entity = entities[ent['tl']]
                timelinepos = entity.position
                less = ((105*scale)/10)
                timelinepos.x -= less
                self.ncount += 1
            else:
                entity = entities[ent['tl']]
                timelinepos = entity.position
                less = ((105*scale)/10)
                timelinepos.x -= less


                entity = entities[ent['tl2']]
                timelinepos = entity.position
                less = ((105*scale)/10)
                timelinepos.x -= less

                self.ncount += 1

    def lv10(self, *args):

        self.rollbacklevelselect()
        self.nametimer = Clock.schedule_once(self.rollbackname, 2)

        self.more_force = True
        sysbox.append('boundary')

        sound_manager = self.gameworld.sound_manager
        sound_manager.stop('track1')
        sound_manager.play_loop('track2', float(self.soundvol))
        self.currenttrack = 'track2'

        self.closebutton.pos = ((5*scale)+wscale, (517*scale)+hscale)

        self.lv10breached = False

        init_entity = self.gameworld.init_entity
        entities = self.gameworld.entities

        touch = self.gameworld.system_manager['cymunk_touch']
        ignore = range(1, 85)
        ignore.remove(50)
        ignore.remove(51)
        touch.ignore_groups = ignore

        physics = self.gameworld.system_manager['cymunk_physics']
        physics.damping = 0.5

        boundary = self.gameworld.system_manager['boundary']
        boundary.shut = 1
        boundary.level = 10
        self.level = 10

        emitter_system = self.ids.emitter
        emitter_system.add_effect(ent['fireball'], 'strikereffects')
        emitter_system.add_effect(ent['fireball2'], 'strikereffects')


        entity = entities[ent['segtex']]
        renderer = entity.rotate_color_scale_renderer2
        renderer.texture_key = 'segtex'

      #areabound, timeline
        objs = ['segtex', 'areabound', 'timeline', 'closex', 'name10']
        pos = [(475, 293.5), (475, 582),
               (475, 582), (20, 560),
               (150, 520)]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            areaboundpos = entity.position
            areaboundpos.pos = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)

        #segs
        objs = ['seg', 'seg2', 'seg3', 'seg4', 'seg5', 'seg6', 'seg7', 'seg8',
                'suppatt1', 'suppatt2', 'suppatt3', 'suppatt4',]
        pos = [(475, 333.5), (475, 253.5), (435, 293.5), (515, 293.5),
               (447, 321.5), (447, 265.5), (503, 265.5), (503, 321.5),
               (475, 687), (475, -100), (-100, 293.5), (1050, 293.5)]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)
            physics.space.reindex_shape(shape[0])

        objs = ['fireball', 'ropehook', 'ropecomp', 'ropecomp2',
                'ropecomp3', 'ropecomp4', 'ropecomp5', 'ropehook2', 'fireball2',
                ]
        pos = [(424, 293.5), (435, 293.5), (451, 293.5),
                (463, 293.5), (475, 293.5), (487, 293.5),
                (499, 293.5), (515, 293.5), (526, 293.5),
                ]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)
            for x in shape:
                physics.space.reindex_shape(x)
            body.reset_forces()
            body.angle = 0
            body.velocity = (0, 0)
            body.angular_velocity = 0


        objs = ['missle1', 'missle2', 'missle3', 'missle4', 'missle5',
        'missle6', 'missle7', ]

        for x in objs:
            emitter_system.add_effect(ent[x], 'meffects')

        objs = ['bigmissle1', 'bigmissle2', 'bigmissle3', 'bigmissle4', 'bigmissle5',
        'bigmissle6', 'bigmissle7', ]

        for x in objs:
            emitter_system.add_effect(ent[x], 'beffects')

        objs = ['omissle1', 'omissle2', 'omissle3', 'omissle4', 'omissle5',
        'omissle6', 'omissle7', ]

        for x in objs:
            emitter_system.add_effect(ent[x], 'oeffects')

        objs = [('ropehook2', 'fireball2'), ('fireball', 'ropehook'),
                ('ropecomp5', 'ropehook2'), ('ropehook', 'ropecomp'),]

        anch = [((11), (0), (0), (0)), ((0), (0), (-11), (0)),
                ((5), (0), (-11), (0)), ((12), (0), (-4), (0)),]

        for x in range(len(objs)):
            entity = entities[ent[objs[x][0]]]
            obj = entity.cymunk_physics.body

            entity = entities[ent[objs[x][1]]]
            obj2 = entity.cymunk_physics.body


            anchr1 = (anch[x][0]*scale, anch[x][1]*scale)
            anchr2 = (anch[x][2]*scale, anch[x][3]*scale)


            joint = PivotJoint(obj, obj2,
                                anchr1,
                                anchr2)
            physics.space.add_constraint(joint)

        objs = [('ropecomp', 'ropecomp2'), ('ropecomp2', 'ropecomp3'),
                ('ropecomp3', 'ropecomp4'), ('ropecomp4', 'ropecomp5')]
        for x in range(len(objs)):
            entity = entities[ent[objs[x][0]]]
            basketedge = entity.cymunk_physics.body
            entity = entities[ent[objs[x][1]]]
            net = entity.cymunk_physics.body


            anchr1 = (5*scale, 0*scale)
            anchr2 = (-7*scale, 0*scale)


            basketnet = PivotJoint(basketedge, net,
                                anchr1,
                                anchr2)
            physics.space.add_constraint(basketnet)

        touch.paused = False
        physics.paused = False
        sysbox.append('cymunk_physics')
        sysbox.append('cymunk_touch')

        self.consnum = len(physics.space.constraints)


        boundary.objs2 = ['fireball', 'fireball2',]
        boundary.objs3 = ['ropehook', 'ropecomp', 'ropecomp2','ropecomp3', 'ropecomp4', 'ropecomp5', 'ropehook2',]
        boundary.paused = False

        self.attgenctrl = Clock.schedule_interval(self.attackgen, 1.5)
        self.timer = Clock.schedule_interval(self.movetimeline, 1)

    def attackgen(self, dt):
        self.attgencount += 1
        emitter_system = self.ids.emitter
        entities = self.gameworld.entities
        physics = self.gameworld.system_manager['cymunk_physics']
        if len(self.attobj[0]) < 3:
            self.attobj[0] = ['missle1', 'missle2', 'missle3', 'missle4', 'missle5', 'missle6', 'missle7',]
        elif len(self.attobj[1]) < 3:
            self.attobj[1] = ['bigmissle1', 'bigmissle2', 'bigmissle3', 'bigmissle4', 'bigmissle5', 'bigmissle6', 'bigmissle7',]
        elif len(self.attobj[2]) < 3:
            self.attobj[2] = ['omissle1', 'omissle2', 'omissle3', 'omissle4', 'omissle5', 'omissle6', 'omissle7',]

        type = choice(self.type)
        obj = self.attobj[type][0]
        del self.attobj[type][0]


        ser = choice(self.ser)
        pos = ((attgen[ser][0][0]*scale)+wscale, (attgen[ser][0][1]*scale)+hscale)
        angle = attgen[ser][1]
        mags = [10, 20]
        mag = choice(mags)
        force = ((attgen[ser][2][0])*mag, (attgen[ser][2][1])*mag)

        entity = entities[ent[obj]]
        body = entity.cymunk_physics.body
        shape = entity.cymunk_physics.shapes

        body.angle = angle
        body.position = pos
        physics.space.reindex_shape(shape[0])

        if obj[0] == 'o':
            r = (0, 10*scale)
            body.apply_force(force, r)
        else:
            body.apply_force(force)

        if self.attgencount == 60:
            self.attgenctrl.cancel()
            self.attgenctrl = Clock.schedule_interval(self.attackgen, 1)

    def breached(self, data):
        entities = self.gameworld.entities
        physics = self.gameworld.system_manager['cymunk_physics']

        entity = entities[data]
        body = entity.cymunk_physics.body
        shape = entity.cymunk_physics.shapes
        newforce = (body.force['x']*.1, body.force['y']*.1)
        body.reset_forces()
        body.velocity = (0, 0)
        body.apply_force(newforce)

        if self.attgenctrl:
            self.attgenctrl.cancel()
            self.timer.cancel()
        if not self.lv10breached and not self.successbtn:
            self.tentimer = Clock.schedule_once(self.controlsscreen, 2)
            self.lv10breached = True
            if self.dovibrate:
                Clock.schedule_once(self.do_vibrate)

            entity = entities[ent['segtex']]
            renderer = entity.rotate_color_scale_renderer2
            renderer.texture_key = 'segbreach'

    def removemissle(self, data):
        entities = self.gameworld.entities
        physics = self.gameworld.system_manager['cymunk_physics']

        entity = entities[data]
        body = entity.cymunk_physics.body
        shape = entity.cymunk_physics.shapes
        body.reset_forces()


        Clock.schedule_once(lambda x:self.placemissle(data), 2)

    def placemissle(self, data):
        entities = self.gameworld.entities
        physics = self.gameworld.system_manager['cymunk_physics']

        entity = entities[data]
        body = entity.cymunk_physics.body
        shape = entity.cymunk_physics.shapes
        body.reset_forces()
        body.position = (3000*scale, 500*scale)
        physics.space.reindex_shape(shape[0])
        body.velocity = (0, 0)
        body.angle = 0

    def diffuse(self, space, arbiter):
        if arbiter.is_first_contact:
            body = arbiter.shapes[1].body
            Clock.schedule_once(lambda x:self.placemissle(body.data))

        return True

    def weaponmissle(self, space, arbiter):
        if arbiter.is_first_contact:
            body = arbiter.shapes[1].body
            Clock.schedule_once(lambda x:self.removemissle(body.data))

        return True

    def segsmissle(self, space, arbiter):
        if arbiter.is_first_contact:
            body = arbiter.shapes[1].body

            Clock.schedule_once(lambda x:self.breached(body.data))

        return True

    def slam(self, touch):

        self.rollbackextras()
        self.level = 'slam'

        self.more_force = True

        self.slamrollpos = 2500

        init_entity = self.gameworld.init_entity
        physics = self.gameworld.system_manager['cymunk_physics']
        entities = self.gameworld.entities
        physics.damping = .5

        emitter_system = self.ids.emitter
        emitter_system.add_effect(ent['white'], 'whiteeffects')

        touch = self.gameworld.system_manager['cymunk_touch']
        ignore = range(1, 85)
        ignore.remove(65)
        touch.ignore_groups = ignore

        boundary = self.gameworld.system_manager['boundary']
        boundary.level = 'slam'

        if self.intropart:
            emitter_system = self.ids.emitter
            emitter_system.remove_effect(ent['blankdecor'], 0)
            self.intropart = False

        self.btnlist[-1].pos = (((50-40)*scale)+wscale, ((550-40)*scale)+hscale)
        self.slamreset.pos = (((890-25)*scale)+wscale, ((550-25)*scale)+hscale)

        #areabound, timeline
        objs = ['table', 'backbutton', 'slamre']
        pos = [(475, 255), (50, 550),
               (890, 550)]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            areaboundpos = entity.position
            areaboundpos.pos = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)

        #screen
        objs = ['horbar1', 'horbar2', 'horbar3', 'horbar4',
                'vertbar1', 'vertbar2',
                'bis1', 'bis2', 'bis3', 'bis4', 'bis5', 'bis6', 'bis7', 'bis8',
                'bsmal1', 'bsmal2', 'bsmal3', 'bsmal4',
                'cueblocker1', 'cueblocker2', 'cueblocker3',
                'cueblocker4', 'cueblocker5', 'cueblocker6',
                'detector1', 'detector2', 'detector3',
                'detector4', 'detector5', 'detector6',
                'horsupport2',

                ]

        pos = [(252, 491), (701, 493),
               (252, 18), (699, 18),
               (18, 257), (933, 257),

               (62, 490), (19, 451),
               (19, 63), (62, 19),
               (931, 63), (889, 19),
               (889, 490), (931, 450),

               (441, 488), (510, 488),
               (441, 21), (510, 21),

               (33, 477), (33, 33),
               (917, 33), (917, 477),
               (475, 505), (475, 20),

               (30, 480), (32, 32),
               (920, 30), (922, 482),
               (475, 496), (475, 14),
               (475, 530)
               ]



        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)
            physics.space.reindex_shape(shape[0])

        #screen
        objs = ['yellow', 'green', 'brown', 'blue', 'pink', 'black', 'white', 'cue',
                'red1',
                'red2', 'red3',
                'red4', 'red5', 'red6',
                'red7', 'red8', 'red9', 'red10',
                'red11', 'red12', 'red13', 'red14', 'red15'
                ]

        pos = [(241, 158), (241, 352), (241, 255),
               (475, 255), (632, 255), (826, 255),
               (200, 210), (200, 210),

               (660, 255),
               (680, 266.5), (680, 243.5),
               (700, 278), (700, 255), (700, 232),
               (720, 289.5), (720, 266.5), (720, 243.5), (720, 220.5),
               (740, 301), (740, 278), (740, 255),
               (740, 232), (740, 209)
               ]

        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)
            physics.space.reindex_shape(shape[0])

        objs = [('white', 'cue'), ('gun', 'gunstopper'),]
        anch = [((0), (0), (0), (0)), ((0), (20), (0), (0)),]
        for x in range(len(objs)):
            entity = entities[ent[objs[x][0]]]
            obj = entity.cymunk_physics.body

            entity = entities[ent[objs[x][1]]]
            obj2 = entity.cymunk_physics.body


            anchr1 = (anch[x][0]*scale, anch[x][1]*scale)
            anchr2 = (anch[x][2]*scale, anch[x][3]*scale)


            joint = PivotJoint(obj, obj2,
                                anchr1,
                                anchr2)
            physics.space.add_constraint(joint)

        self.consnum = len(physics.space.constraints)


        touch.paused = False
        physics.paused = False
        sysbox.append('cymunk_physics')
        sysbox.append('cymunk_touch')

    def slamresetmini(self, touch):
        entities = self.gameworld.entities
        physics = self.gameworld.system_manager['cymunk_physics']

        #screen
        objs = ['yellow', 'green', 'brown', 'blue', 'pink', 'black', 'white', 'cue',
                'red1',
                'red2', 'red3',
                'red4', 'red5', 'red6',
                'red7', 'red8', 'red9', 'red10',
                'red11', 'red12', 'red13', 'red14', 'red15'
                ]

        pos = [(241, 158), (241, 352), (241, 255),
               (475, 255), (632, 255), (826, 255),
               (200, 210), (200, 210),

               (660, 255),
               (680, 266.5), (680, 243.5),
               (700, 278), (700, 255), (700, 232),
               (720, 289.5), (720, 266.5), (720, 243.5), (720, 220.5),
               (740, 301), (740, 278), (740, 255),
               (740, 232), (740, 209)
               ]

        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            body.position = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)
            physics.space.reindex_shape(shape[0])
            body.reset_forces()
            body.angle = 0
            body.velocity = (0, 0)
            body.angular_velocity = 0

        Clock.schedule_once(self.showad)

    def horbar(self, force, data):
        X = force['x']
        Y = force['y']

        if X < 0:
            new = abs(X)*2
            X = new+X
        elif X > 0:
            new = X*2
            X = X-new


        entities = self.gameworld.entities
        entity = entities[data]
        body = entity.cymunk_physics.body
        body.reset_forces()
        force_ = (X,Y)
        body.apply_force(force_)

    def vertbar(self, force, data):
        X = force['x']
        Y = force['y']

        if Y < 0:
            new = abs(Y)*2
            Y = new+Y
        elif Y > 0:
            new = Y*2
            Y = Y-new


        entities = self.gameworld.entities
        entity = entities[data]
        body = entity.cymunk_physics.body
        body.reset_forces()
        force_ = (X,Y)
        body.apply_force(force_)

    def horbartoballs(self, space, arbiter):
        if arbiter.is_first_contact:
            body = arbiter.shapes[1].body
            Clock.schedule_once(lambda x:self.horbar(body.force, body.data))



        return True

    def vertbartoballs(self, space, arbiter):
        if arbiter.is_first_contact:
            body = arbiter.shapes[1].body
            Clock.schedule_once(lambda x:self.vertbar(body.force, body.data))



        return True

    def det1(self, data):
        entities = self.gameworld.entities
        physics = self.gameworld.system_manager['cymunk_physics']

        if data != ent['white']:
            entity = entities[data]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            self.slamrollpos += 25
            body.position = (self.slamrollpos *scale, self.slamrolly*scale)
            physics.space.reindex_shape(shape[0])
            body.reset_forces()
            body.angle = 0
            body.velocity = (0, 0)
            body.angular_velocity = 0

            cur = None
            if data == ent['yellow']:
                cur = 'yellowimg'
            elif data == ent['green']:
                cur = 'greenimg'
            elif data == ent['brown']:
                cur = 'brownimg'
            elif data == ent['blue']:
                cur = 'blueimg'
            elif data == ent['pink']:
                cur = 'pinkimg'
            elif data == ent['black']:
                cur = 'blackimg'
            elif data in range(ent['red1'], ent['red15']+1):
                cur = 'redimg'

            entity = entities[ent[cur]]
            areaboundpos = entity.position
            areaboundpos.pos = ((33*scale)+wscale, (477*scale)+hscale)

            Clock.schedule_once(lambda x:self.removeimg(cur), .5)

    def detector1balls(self, space, arbiter):
        if arbiter.is_first_contact:
            body = arbiter.shapes[1].body
            Clock.schedule_once(lambda x:self.det1(body.data))



        return True

    def det2(self, data):
        entities = self.gameworld.entities
        physics = self.gameworld.system_manager['cymunk_physics']

        if data != ent['white']:
            entity = entities[data]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            self.slamrollpos += 25
            body.position = (self.slamrollpos *scale, self.slamrolly*scale)
            physics.space.reindex_shape(shape[0])
            body.reset_forces()
            body.angle = 0
            body.velocity = (0, 0)
            body.angular_velocity = 0

            cur = None
            if data == ent['yellow']:
                cur = 'yellowimg'
            elif data == ent['green']:
                cur = 'greenimg'
            elif data == ent['brown']:
                cur = 'brownimg'
            elif data == ent['blue']:
                cur = 'blueimg'
            elif data == ent['pink']:
                cur = 'pinkimg'
            elif data == ent['black']:
                cur = 'blackimg'
            elif data in range(ent['red1'], ent['red15']+1):
                cur = 'redimg'

            entity = entities[ent[cur]]
            areaboundpos = entity.position
            areaboundpos.pos = ((33*scale)+wscale, (33*scale)+hscale)

            Clock.schedule_once(lambda x:self.removeimg(cur), .5)

    def detector2balls(self, space, arbiter):
        if arbiter.is_first_contact:
            body = arbiter.shapes[1].body
            Clock.schedule_once(lambda x:self.det2(body.data))



        return True

    def det3(self, data):
        entities = self.gameworld.entities
        physics = self.gameworld.system_manager['cymunk_physics']

        if data != ent['white']:
            entity = entities[data]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            self.slamrollpos += 25
            body.position = (self.slamrollpos *scale, self.slamrolly*scale)
            physics.space.reindex_shape(shape[0])
            body.reset_forces()
            body.angle = 0
            body.velocity = (0, 0)
            body.angular_velocity = 0

            cur = None
            if data == ent['yellow']:
                cur = 'yellowimg'
            elif data == ent['green']:
                cur = 'greenimg'
            elif data == ent['brown']:
                cur = 'brownimg'
            elif data == ent['blue']:
                cur = 'blueimg'
            elif data == ent['pink']:
                cur = 'pinkimg'
            elif data == ent['black']:
                cur = 'blackimg'
            elif data in range(ent['red1'], ent['red15']+1):
                cur = 'redimg'

            entity = entities[ent[cur]]
            areaboundpos = entity.position
            areaboundpos.pos = ((917*scale)+wscale, (33*scale)+hscale)

            Clock.schedule_once(lambda x:self.removeimg(cur), .5)

    def detector3balls(self, space, arbiter):
        if arbiter.is_first_contact:
            body = arbiter.shapes[1].body
            Clock.schedule_once(lambda x:self.det3(body.data))



        return True

    def det4(self, data):
        entities = self.gameworld.entities
        physics = self.gameworld.system_manager['cymunk_physics']

        if data != ent['white']:
            entity = entities[data]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            self.slamrollpos += 25
            body.position = (self.slamrollpos *scale, self.slamrolly*scale)
            physics.space.reindex_shape(shape[0])
            body.reset_forces()
            body.angle = 0
            body.velocity = (0, 0)
            body.angular_velocity = 0

            cur = None
            if data == ent['yellow']:
                cur = 'yellowimg'
            elif data == ent['green']:
                cur = 'greenimg'
            elif data == ent['brown']:
                cur = 'brownimg'
            elif data == ent['blue']:
                cur = 'blueimg'
            elif data == ent['pink']:
                cur = 'pinkimg'
            elif data == ent['black']:
                cur = 'blackimg'
            elif data in range(ent['red1'], ent['red15']+1):
                cur = 'redimg'

            entity = entities[ent[cur]]
            areaboundpos = entity.position
            areaboundpos.pos = ((917*scale)+wscale, (477*scale)+hscale)

            Clock.schedule_once(lambda x:self.removeimg(cur), .5)

    def detector4balls(self, space, arbiter):
        if arbiter.is_first_contact:
            body = arbiter.shapes[1].body
            Clock.schedule_once(lambda x:self.det4(body.data))



        return True

    def det5(self, data):
        entities = self.gameworld.entities
        physics = self.gameworld.system_manager['cymunk_physics']

        if data != ent['white']:
            entity = entities[data]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            self.slamrollpos += 25
            body.position = (self.slamrollpos *scale, self.slamrolly*scale)
            physics.space.reindex_shape(shape[0])
            body.reset_forces()
            body.angle = 0
            body.velocity = (0, 0)
            body.angular_velocity = 0

            cur = None
            if data == ent['yellow']:
                cur = 'yellowimg'
            elif data == ent['green']:
                cur = 'greenimg'
            elif data == ent['brown']:
                cur = 'brownimg'
            elif data == ent['blue']:
                cur = 'blueimg'
            elif data == ent['pink']:
                cur = 'pinkimg'
            elif data == ent['black']:
                cur = 'blackimg'
            elif data in range(ent['red1'], ent['red15']+1):
                cur = 'redimg'

            entity = entities[ent[cur]]
            areaboundpos = entity.position
            areaboundpos.pos = ((475*scale)+wscale, (488*scale)+hscale)

            Clock.schedule_once(lambda x:self.removeimg(cur), .5)

    def detector5balls(self, space, arbiter):
        if arbiter.is_first_contact:
            body = arbiter.shapes[1].body
            Clock.schedule_once(lambda x:self.det5(body.data))



        return True

    def det6(self, data):
        entities = self.gameworld.entities
        physics = self.gameworld.system_manager['cymunk_physics']

        if data != ent['white']:
            entity = entities[data]
            body = entity.cymunk_physics.body
            shape = entity.cymunk_physics.shapes
            self.slamrollpos += 25
            body.position = (self.slamrollpos *scale, self.slamrolly*scale)
            physics.space.reindex_shape(shape[0])
            body.reset_forces()
            body.angle = 0
            body.velocity = (0, 0)
            body.angular_velocity = 0

            cur = None
            if data == ent['yellow']:
                cur = 'yellowimg'
            elif data == ent['green']:
                cur = 'greenimg'
            elif data == ent['brown']:
                cur = 'brownimg'
            elif data == ent['blue']:
                cur = 'blueimg'
            elif data == ent['pink']:
                cur = 'pinkimg'
            elif data == ent['black']:
                cur = 'blackimg'
            elif data in range(ent['red1'], ent['red15']+1):
                cur = 'redimg'

            entity = entities[ent[cur]]
            areaboundpos = entity.position
            areaboundpos.pos = ((475*scale)+wscale, (22*scale)+hscale)

            Clock.schedule_once(lambda x:self.removeimg(cur), .5)

    def detector6balls(self, space, arbiter):
        if arbiter.is_first_contact:
            body = arbiter.shapes[1].body
            Clock.schedule_once(lambda x:self.det6(body.data))



        return True

    def removeimg(self, data):
        entities = self.gameworld.entities
        entity = entities[ent[data]]
        areaboundpos = entity.position
        areaboundpos.pos = (2629 *scale, 4000 *scale)

    def turnover(self, once):
        if self.level != 8:
            if self.turned == False:
                boundary = self.gameworld.system_manager['boundary']
                boundary.shut = 0
                boundary.bottomborder()
                self.timer = Clock.schedule_interval(self.movetimeline, 1)
                self.turned = True

        else:
            boundary = self.gameworld.system_manager['boundary']
            boundary.cur_str = self.cur_str
            if self.cur_str == ent['spstriker']:
                boundary.sp1 = True
            elif self.cur_str == ent['spstriker2']:
                boundary.sp2 = True
            boundary.call8()

    def success(self):
        if self.level == 4:
            if self.basket:
                self.successbtn = True

        else:
            if not self.caught:
                self.successbtn = True

    def movetimeline(self, dt):
        if self.level in self.samelevels:
            if self.count == 4:
                self.timer.cancel()
                self.controlsscreen()
                self.count = 0

            else:
                entities = self.gameworld.entities
                entity = entities[ent['timeline']]
                timelinepos = entity.position
                less = ((973*scale)/4)
                timelinepos.x -= less
                self.count += 1


        elif self.level == 4:
            if self.count == 6:
                self.timer.cancel()
                self.controlsscreen()
                self.count = 0

            else:
                entities = self.gameworld.entities
                entity = entities[ent['timeline2']]
                timelinepos = entity.position
                less = ((587*scale)/6)
                timelinepos.y -= less
                self.count += 1


        elif self.level == 5:
            if self.count == 6:
                self.timer.cancel()
                self.controlsscreen()
                self.count = 0

            else:
                entities = self.gameworld.entities
                entity = entities[ent['timeline']]
                timelinepos = entity.position
                less = ((320*scale)/6)
                timelinepos.x -= less
                self.count += 1


        elif self.level == 6:
            if self.count == 6:
                self.timer.cancel()
                self.controlsscreen()
                self.count = 0

            else:
                entities = self.gameworld.entities
                entity = entities[ent['timeline']]
                timelinepos = entity.position
                less = ((475*scale)/6)
                timelinepos.x -= less
                self.count += 1


        elif self.level == 7:
            if self.count == 50:
                self.timer.cancel()
                self.count = 0
                self.controlsscreen()
                if self.successchecktimer:
                    self.successchecktimer.cancel()

            else:
                entities = self.gameworld.entities
                entity = entities[ent['timeline']]
                timelinepos = entity.position
                less = ((950*scale)/50)
                timelinepos.x -= less
                self.count += 1



        elif self.level == 8:
            if self.count == 8:
                self.timer.cancel()
                self.controlsscreen()
                self.count = 0

            else:
                entities = self.gameworld.entities
                entity = entities[ent['timeline']]
                timelinepos = entity.position
                less = ((580*scale)/8)
                timelinepos.x += less
                self.count += 1


        elif self.level == 9:
            if self.count == 90:
                self.timer.cancel()
                self.count = 0

            else:
                entities = self.gameworld.entities
                entity = entities[ent['timeline']]
                timelinepos = entity.position
                less = ((973*scale)/90)
                timelinepos.x -= less
                self.count += 1


        elif self.level == 10:
            if self.count == 180:
                self.timer.cancel()
                self.attgenctrl.cancel()
                self.successbtn = True
                self.controlsscreen()
                self.count = 0

            else:
                entities = self.gameworld.entities
                entity = entities[ent['timeline']]
                timelinepos = entity.position
                less = ((973*scale)/180)
                timelinepos.x -= less
                self.count += 1

    def reset(self, *args):
        boundary = self.gameworld.system_manager['boundary']
        lvls = [7, 9, 10]
        if self.level not in lvls:
            boundary.bottomborderoff()
        boundary.level = 0
        boundary.sp1 = False
        boundary.sp2 = False
        boundary.cur_str = None
        boundary.stopbullets = False
        self.turned = False
        self.successbtn = False
        self.caught = False
        self.basket = False
        self.success2 = False
        self.remsupport = False
        self.ball = ['cannonball', 'cannonball2', 'cannonball3', 'cannonball4']

        self.hitside = False
        self.hittop = False
        self.touchedside = False
        self.touchedtop = False
        self.fintime = 0
        self.rank = 0

        self.sresetstriker = False
        self.sresetstriker2 = False
        self.sresetstriker3 = False
        self.sresetstriker4 = False
        self.scannoncannon2 = False
        self.scannoncannon3 = False
        self.scannoncannon4 = False
        self.scannon2cannon3 = False
        self.scannon2cannon4 = False
        self.scannon3cannon4 = False

        self.scgoal = False
        self.scgoal2 = False
        self.scgoal3 = False
        self.scgoal4 = False

        self.count = 0

        self.double = False
        self.doubletm = False

        timers = [self.cantime, self.cantime2, self.cantime3, self.cantime4, self.cantime5]
        for x in range(len(timers)):
            if timers[x]:
                timers[x].cancel()

    def controlsscreen(self, *args):
        self.rollbackassets()

        emitter_system = self.ids.emitter
        touch = self.gameworld.system_manager['cymunk_touch']
        ignore = range(1, 85)
        touch.ignore_groups = ignore
        entities = self.gameworld.entities

        if self.level == 7:
            touch = self.gameworld.system_manager['cymunk_touch']
            ignore = range(1, 85)
            touch.ignore_groups = ignore

            timers = [self.cantime, self.cantime2, self.cantime3, self.cantime4, self.cantime5]
            for x in range(len(timers)):
                if timers[x]:
                    timers[x].cancel()


        elif self.level == 9:
            boundary = self.gameworld.system_manager['boundary']
            boundary.stopbullets = True

        entity = entities[ent['blankdecor']]
        cardshowpos = entity.position
        cardshowpos.pos = ((475*scale)+wscale, (293.5*scale)+hscale)

        if self.successbtn:
            emitter_system.add_effect(ent['blankdecor'], 'successeffects')
            samelevels = [1, 3, 4, 6]
            if self.level in samelevels:
                if self.touchedtop:
                    self.rank = 2
                if self.touchedside:
                    self.rank = 3

            elif self.level == 2:
                if self.touchedside or self.touchedtop:
                    self.rank = 3
                    if self.caught:
                        self.rank -= 1
                else:
                    self.rank = 2
                    if self.caught:
                        self.rank -= 1

            elif self.level == 5:
                curranklist = []
                if self.touchedtop:
                    curranklist.append('top')
                if self.touchedside:
                    curranklist.append('side')
                if 'top' in curranklist:
                    self.rank = 3
                elif 'side' in curranklist:
                    self.rank = 2

            elif self.level == 7:
                if self.fintime <= 20:
                    self.rank = 3
                elif self.fintime >= 20 and self.fintime <= 35:
                    self.rank = 2
                else:
                    self.rank = 1

            elif self.level == 8:
                if self.fintime <= 3:
                    self.rank = 3
                elif self.fintime == 5:
                    self.rank = 2
                else:
                    self.rank = 1

            elif self.level == 9:
                if self.fintime <= 35:
                    self.rank = 3
                elif self.fintime == 50:
                    self.rank = 2
                else:
                    self.rank = 1

            elif self.level == 10:
                self.rank = 3

            if self.rank == 0:
                self.rank = 1

            if self.rank > self.ranklist[self.level-1]:
                self.ranklist[self.level-1] = self.rank


            self.store3.put('rankingsys',
                            ranks=self.ranklist,
               )

            Clock.schedule_once(self.sucessimg, .5)
            Clock.schedule_once(self.sucessbtns, .8)


            if self.level != 10:
                lv = ['one', 'two', 'three', 'four', 'five', 'six', 'seven',
                      'eight', 'nine', 'ten']
                self.lvprog[self.level] = lv[self.level]
                self.store2.put('lvprog',
                               progress=self.lvprog,
                               )


            self.won = True

        else:
            emitter_system.add_effect(ent['blankdecor'], 'failureeffects')
            Clock.schedule_once(self.failimg, .5)
            Clock.schedule_once(self.failbtns, .8)

    def sucessimg(self, once):
        entities = self.gameworld.entities
        if self.rank == 2:
            entity = entities[ent['star']]
            renderer = entity.rotate_color_scale_renderer
            renderer.texture_key = 'star2'
        elif self.rank == 3:
            entity = entities[ent['star']]
            renderer = entity.rotate_color_scale_renderer
            renderer.texture_key = 'star3'
        else:
            entity = entities[ent['star']]
            renderer = entity.rotate_color_scale_renderer
            renderer.texture_key = 'star1'

        objs = ['successimg', 'star']
        pos = [((475*scale)+wscale, (420*scale)+hscale), ((475*scale)+wscale, (320*scale)+hscale)]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            cardshowpos = entity.position
            cardshowpos.pos = pos[x]

    def sucessbtns(self, once):
        entities = self.gameworld.entities

        objs = ['restartbtn', 'mainmenubtn', 'stageselectbtn']
        pos = [(237.5, 193),
               (475, 193), (712.5, 193)]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            cardshowpos = entity.position
            cardshowpos.pos = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)

        self.btnlist[15].pos = (((237.5-60)*scale)+wscale, ((193-60)*scale)+hscale)
        self.btnlist[16].pos = (((475-60)*scale)+wscale, ((193-60)*scale)+hscale)
        self.btnlist[17].pos = (((712.5-60)*scale)+wscale, ((193-60)*scale)+hscale)

        Clock.schedule_once(self.showad)

    def failimg(self, once):
        entities = self.gameworld.entities

        objs = ['failedimg']
        pos = [((475*scale)+wscale, (400*scale)+hscale)]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            cardshowpos = entity.position
            cardshowpos.pos = pos[x]

    def failbtns(self, once):
        entities = self.gameworld.entities

        objs = ['stageselectbtn', 'mainmenubtn', 'restartbtn', ]
        pos = [(237.5, 193),
               (475, 193), (712.5, 193)]
        for x in range(len(objs)):
            entity = entities[ent[objs[x]]]
            cardshowpos = entity.position
            cardshowpos.pos = ((pos[x][0] *scale)+wscale, (pos[x][1] *scale)+hscale)


        self.btnlist[17].pos = (((237.5-60)*scale)+wscale, ((193-60)*scale)+hscale)
        self.btnlist[16].pos = (((475-60)*scale)+wscale, ((193-60)*scale)+hscale)
        self.btnlist[15].pos = (((712.5-60)*scale)+wscale, ((193-60)*scale)+hscale)

        Clock.schedule_once(self.showad)

    def controlscreenoff(self, *args):
        entities = self.gameworld.entities
        emitter_system = self.ids.emitter
        emitter_system.remove_effect(ent['blankdecor'], 0)

        if self.successbtn:
            objs = ['successimg', 'restartbtn', 'mainmenubtn', 'stageselectbtn', 'star']
            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                cardshowpos = entity.position
                cardshowpos.pos = (2629 *scale, 4000 *scale)

            self.btnlist[15].pos = (2629 *scale, 4000 *scale)
            self.btnlist[16].pos = (2629 *scale, 4000 *scale)
            self.btnlist[17].pos = (2629 *scale, 4000 *scale)

        else:
            objs = ['failedimg', 'restartbtn', 'mainmenubtn', 'stageselectbtn']
            for x in range(len(objs)):
                entity = entities[ent[objs[x]]]
                cardshowpos = entity.position
                cardshowpos.pos = (2629 *scale, 4000 *scale)

            self.btnlist[15].pos = (2629 *scale, 4000 *scale)
            self.btnlist[16].pos = (2629 *scale, 4000 *scale)
            self.btnlist[17].pos = (2629 *scale, 4000 *scale)


        if self.won:
            self.won = False

    def wakethegoal(self, once):
        if self.level != 5:
            boundary = self.gameworld.system_manager['boundary']
            if 'goal' not in boundary.objs:
                boundary.paused = True
                boundary.objs.append('goal')
                boundary.paused = False
                if self.dovibrate:
                    if self.level != 4:
                        Clock.schedule_once(self.do_vibrate)
                    else:
                        if self.basket:
                            Clock.schedule_once(self.do_vibrate)
        elif self.level == 7:
            pass

        else:
            if not self.five and self.dovibrate:
                Clock.schedule_once(self.do_vibrate)
                self.five = True




        if self.hitside:
            self.touchedside = True
        if self.hittop:
            self.touchedtop = True
        self.fintime = self.count

    def striker_side(self, space, arbiter):
        if arbiter.is_first_contact:
            self.hitside = True


        return True

    def striker_top(self, space, arbiter):
        if arbiter.is_first_contact:
            self.hittop = True


        return True

    def magic_side(self, space, arbiter):
        if arbiter.is_first_contact:
            self.hitside = True


        return True

    def magic_top(self, space, arbiter):
        if arbiter.is_first_contact:
            self.hittop = True


        return True

    def do_vibrate(self, once):
        if vibrator.hasVibrator():
            vibrator.vibrate(100)

    def true(self, space, arbiter):
        return True

    def false(self, space, arbiter):
        return False

    def striker_slit(self, space, arbiter):
        if self.turned == False:
            touch = self.gameworld.system_manager['cymunk_touch']
            if self.level != 8:
                ignore = range(1, 85)
                touch.ignore_groups = ignore

            if self.level == 8:
                if arbiter.is_first_contact:
                    body = arbiter.shapes[0].body
                    curstr = body.data

                    Clock.schedule_once(lambda x:self.set_cur_str(curstr))
                    if not self.lv8slit:
                        self.timer = Clock.schedule_interval(self.movetimeline, 1)
                        self.lv8slit = True
                    if curstr == ent['spstriker']:
                        touch.ignore_groups.append(42)
                    elif curstr == ent['spstriker2']:
                        touch.ignore_groups.append(43)




            Clock.schedule_once(self.turnover)

        return True

    def succeeded(self, space, arbiter):
        if arbiter.is_first_contact:
            self.success()
        return False

    def striker2goal(self, space, arbiter):
        try:
            if arbiter.is_first_contact:
                Clock.schedule_once(self.wakethegoal)
        except:
            pass

        return True

    def clear_up(self, *args):
        self.gameworld.state = 'pause'
        self.setup_states2()

    def restore(self, *args):
        Clock.schedule_once(self.restore_par, .1)

    def restore_par(self, once):
        self.gameworld.state = 'resume'

#collision callbacks

    def collision_callbacks(self):
        physics_system = self.gameworld.system_manager['cymunk_physics']
    #ranking
        physics_system.add_collision_handler(
            4, 83,
            begin_func=self.striker_side,
            pre_solve_func=self.true)

        physics_system.add_collision_handler(
            4, 84,
            begin_func=self.striker_top,
            pre_solve_func=self.true)



    #basics

        physics_system.add_collision_handler(
            4, 7,
            begin_func=self.striker_slit,
            pre_solve_func=self.false)
        physics_system.add_collision_handler(
            6, 5,
            begin_func=self.true,
            pre_solve_func=self.succeeded)
        physics_system.add_collision_handler(
            6, 4,
            begin_func=self.true,
            pre_solve_func=self.striker2goal)

        col_types = [(4,5), (7, 6),(8, 3),(8, 5),(8, 6),(8, 7)]
        for x in range(len(col_types)):
            physics_system.add_collision_handler(
                col_types[x][0],col_types[x][1],
                begin_func=self.true,
                pre_solve_func=self.false)

    #lv2
        physics_system.add_collision_handler(
            10, 4,
            begin_func=self.true,
            pre_solve_func=self.cameralightstriker)
        physics_system.add_collision_handler(
            10, 7,
            begin_func=self.true,
            pre_solve_func=self.camerastateup)
        physics_system.add_collision_handler(
            10, 12,
            begin_func=self.true,
            pre_solve_func=self.camerastatedown)
        physics_system.add_collision_handler(
            11, 4,
            begin_func=self.true,
            pre_solve_func=self.camerastriker)

        col_types = [(10, 8),(10, 3),(10, 5),(10, 6),(11, 8),(11, 3), (10, 84), (10, 9)]
        for x in range(len(col_types)):
            physics_system.add_collision_handler(
                col_types[x][0],col_types[x][1],
                begin_func=self.true,
                pre_solve_func=self.false)


    #lv3
        physics_system.add_collision_handler(
            13, 6,
            begin_func=self.true,
            pre_solve_func=self.magicballwall2)

        physics_system.add_collision_handler(
            13, 83,
            begin_func=self.true,
            pre_solve_func=self.magicballwallside)
        physics_system.add_collision_handler(
            13, 84,
            begin_func=self.true,
            pre_solve_func=self.magicballwalltop)
#(14, 6)
        col_types = [(9, 14),(13, 5),(13, 7),(13, 8),(14, 8),(14, 3),
                     (14, 7),(15, 14),(22, 3),(22, 5),
                     (22, 6), (22, 8), (17, 6), (14, 83)]
        for x in range(len(col_types)):
            physics_system.add_collision_handler(
                col_types[x][0],col_types[x][1],
                begin_func=self.true,
                pre_solve_func=self.false)

    #lv4
        physics_system.add_collision_handler(
            23, 4,
            begin_func=self.true,
            pre_solve_func=self.basketsuccess)

        col_types = [(3, 16),(16, 17),(16, 8),(17, 8),(17, 4)]
        for x in range(len(col_types)):
            physics_system.add_collision_handler(
                col_types[x][0],col_types[x][1],
                begin_func=self.true,
                pre_solve_func=self.false)

    #lv5
        physics_system.add_collision_handler(
            18, 4,
            begin_func=self.true,
            pre_solve_func=self.strikerlight)

        physics_system.add_collision_handler(
            53, 4,
            begin_func=self.true,
            pre_solve_func=self.false)


    #lv6
        #topbar          24
        #leftrightweight 25
        #supportarea     27
        #screen           3
        #supporters      28
        #striker
        #cart            26
        #cartwheel       26
#
        col_types = [(24, 27), (4, 27), (26, 27),
                     (24, 3), (7, 26),
                     (5, 26), (6, 27), (26, 8),
                     (27, 8), (28, 8),  (24, 8),
                     (25, 27), (25, 3), (25, 26),
                     (25, 6), (4, 25), (25, 8), (28, 25),]
        for x in range(len(col_types)):
            physics_system.add_collision_handler(
                col_types[x][0],col_types[x][1],
                begin_func=self.true,
                pre_solve_func=self.false)

        col_types = [(24, 4), (28, 4),
                     (26, 4)]
        for x in range(len(col_types)):
            physics_system.add_collision_handler(
                col_types[x][0],col_types[x][1],
                begin_func=self.true,
                pre_solve_func=self.strikercartopbar)

        physics_system.add_collision_handler(
            26, 6,
            begin_func=self.true,
            pre_solve_func=self.striker2goal)

    #lv7
        col_types = [(20, 3),
                     (21, 4),
                     (33, 5), (34, 5), (35, 5), (36, 5),
                     (5, 38), (5, 39), (5, 40), (5, 41),]
        for x in range(len(col_types)):
            physics_system.add_collision_handler(
                col_types[x][0],col_types[x][1],
                begin_func=self.true,
                pre_solve_func=self.false)

        col_types = [(33, 34), (33, 35), (33, 36), (33, 37),
                     (33, 38), (33, 39), (33, 40), (33, 41),
                     (34, 33), (34, 35), (34, 36), (34, 37),
                     (34, 38), (34, 39), (34, 40), (34, 41),
                     (35, 33), (35, 34), (35, 36), (35, 37),
                     (35, 38), (35, 39), (35, 40), (35, 41),
                     (36, 33), (36, 34), (36, 35), (36, 37),
                     (36, 38), (36, 39), (36, 40), (36, 41),
                     (37, 33), (37, 34), (37, 35), (37, 36),
                     (37, 38), (37, 39), (37, 40), (37, 41),
                     (38, 33), (38, 34), (38, 35), (38, 36),
                     (38, 37), (38, 39), (38, 40), (38, 41),
                     (39, 33), (39, 34), (39, 35), (39, 36),
                     (39, 37), (39, 38), (39, 40), (39, 41),
                     (40, 33), (40, 34), (40, 35), (40, 36),
                     (40, 37), (40, 38), (40, 39), (40, 41),
                     (41, 33), (41, 34), (41, 35), (41, 36),
                     (41, 37), (41, 38), (41, 39), (41, 40),
                     (20, 33), (20, 34), (20, 35), (20, 36),
                     (20, 37), (20, 38), (20, 39), (20, 40),
                     (20, 41), (37, 33), (37, 34), (37, 35),
                     (37, 36), (37, 37), (37, 38), (37, 39),
                     (37, 40), (37, 41)]
        for x in range(len(col_types)):
            physics_system.add_collision_handler(
                col_types[x][0],col_types[x][1],
                begin_func=self.true,
                pre_solve_func=self.cgoalstocannoballs)


    #lv8
        physics_system.add_collision_handler(
            42, 6,
            begin_func=self.true,
            pre_solve_func=self.striker2goal)

        physics_system.add_collision_handler(
            43, 6,
            begin_func=self.true,
            pre_solve_func=self.striker2goal)

        physics_system.add_collision_handler(
            42, 7,
            begin_func=self.striker_slit,
            pre_solve_func=self.false)

        physics_system.add_collision_handler(
            43, 7,
            begin_func=self.striker_slit,
            pre_solve_func=self.false)

        physics_system.add_collision_handler(
            19, 44,
            begin_func=self.YnormalYsensor,
            pre_solve_func=self.false)


        col_types = [(45, 42), (45, 43)]
        for x in range(len(col_types)):
            physics_system.add_collision_handler(
                col_types[x][0],col_types[x][1],
                begin_func=self.spstrikersbutton,
                pre_solve_func=self.true)

        col_types = [(42, 5), (42, 44),
                     (43, 5), (43, 44),
                     (6,44), (19,3),
                     (45, 3),
                     (47, 3),
                     (42, 27), (43, 27),
                     (42, 46), (43, 46),
                     (19, 8), (44, 8), (45, 8),
                     (19,55), (19,56), (45, 55), (45,56), (19,57), (19,58),
                     (42, 55), (42, 58), (43, 56), (43, 57),
                     (6, 55), (6, 56)]
        for x in range(len(col_types)):
            physics_system.add_collision_handler(
                col_types[x][0],col_types[x][1],
                begin_func=self.true,
                pre_solve_func=self.false)

    #lv9

        physics_system.add_collision_handler(
            3, 49,
            begin_func=self.screentobullet,
            pre_solve_func=self.true)

        physics_system.add_collision_handler(
            60, 49,
            begin_func=self.screentobulletY,
            pre_solve_func=self.true)
        physics_system.add_collision_handler(
            61, 5,
            begin_func=self.ngoaltoseg,
            pre_solve_func=self.false)
        physics_system.add_collision_handler(
            54, 5,
            begin_func=self.ngoal2toseg,
            pre_solve_func=self.false)

        physics_system.add_collision_handler(
            82, 49,
            begin_func=self.gunbullets,
            pre_solve_func=self.true)


        col_types = [(48, 49), (49, 52),
                     (49, 5)]
        for x in range(len(col_types)):
            physics_system.add_collision_handler(
                col_types[x][0],col_types[x][1],
                begin_func=self.true,
                pre_solve_func=self.false)

    #lv10

        col_types = [(5, 62), (5, 63), (5, 64),]
        for x in range(len(col_types)):
            physics_system.add_collision_handler(
                col_types[x][0],col_types[x][1],
                begin_func=self.segsmissle,
                pre_solve_func=self.false)

        col_types = [(50, 62), (50, 63), (50, 64),
                     (51, 62), (51, 63), (51, 64)]
        for x in range(len(col_types)):
            physics_system.add_collision_handler(
                col_types[x][0],col_types[x][1],
                begin_func=self.weaponmissle,
                pre_solve_func=self.true)

        col_types = [(73, 62), (73, 63), (73, 64)]
        for x in range(len(col_types)):
            physics_system.add_collision_handler(
                col_types[x][0],col_types[x][1],
                begin_func=self.diffuse,
                pre_solve_func=self.true)

        col_types = [(5, 50), (5, 51),
                     (50, 51), ]
        for x in range(len(col_types)):
            physics_system.add_collision_handler(
                col_types[x][0],col_types[x][1],
                begin_func=self.true,
                pre_solve_func=self.false)

    #slam
        col_types = [(3, 65), (3, 66), (3, 67),
                     (3, 68), (3, 69), (3, 70),
                     (3, 71), (3, 72)]
        for x in range(len(col_types)):
            physics_system.add_collision_handler(
                col_types[x][0],col_types[x][1],
                begin_func=self.vertbartoballs,
                pre_solve_func=self.true)

        col_types = [(60, 65), (60, 66), (60, 67),
                     (60, 68), (60, 69), (60, 70),
                     (60, 71), (60, 72)]
        for x in range(len(col_types)):
            physics_system.add_collision_handler(
                col_types[x][0],col_types[x][1],
                begin_func=self.horbartoballs,
                pre_solve_func=self.true)

        col_types = [(75, 65), (75, 66), (75, 67),
                     (75, 68), (75, 69), (75, 70),
                     (75, 71), (75, 72)]
        for x in range(len(col_types)):
            physics_system.add_collision_handler(
                col_types[x][0],col_types[x][1],
                begin_func=self.detector1balls,
                pre_solve_func=self.true)

        col_types = [(76, 65), (76, 66), (76, 67),
                     (76, 68), (76, 69), (76, 70),
                     (76, 71), (76, 72)]
        for x in range(len(col_types)):
            physics_system.add_collision_handler(
                col_types[x][0],col_types[x][1],
                begin_func=self.detector2balls,
                pre_solve_func=self.true)

        col_types = [(77, 65), (77, 66), (77, 67),
                     (77, 68), (77, 69), (77, 70),
                     (77, 71), (77, 72)]
        for x in range(len(col_types)):
            physics_system.add_collision_handler(
                col_types[x][0],col_types[x][1],
                begin_func=self.detector3balls,
                pre_solve_func=self.true)

        col_types = [(78, 65), (78, 66), (78, 67),
                     (78, 68), (78, 69), (78, 70),
                     (78, 71), (78, 72)]
        for x in range(len(col_types)):
            physics_system.add_collision_handler(
                col_types[x][0],col_types[x][1],
                begin_func=self.detector4balls,
                pre_solve_func=self.true)

        col_types = [(79, 65), (79, 66), (79, 67),
                     (79, 68), (79, 69), (79, 70),
                     (79, 71), (79, 72)]
        for x in range(len(col_types)):
            physics_system.add_collision_handler(
                col_types[x][0],col_types[x][1],
                begin_func=self.detector5balls,
                pre_solve_func=self.true)

        col_types = [(80, 65), (80, 66), (80, 67),
                     (80, 68), (80, 69), (80, 70),
                     (80, 71), (80, 72)]
        for x in range(len(col_types)):
            physics_system.add_collision_handler(
                col_types[x][0],col_types[x][1],
                begin_func=self.detector6balls,
                pre_solve_func=self.true)


        col_types = [(74, 66), (74, 67), (74, 68),
                     (74, 69), (74, 70), (74, 71), (74, 72),
                     (81, 60), (81, 3), (81, 65), (81, 66),
                     (81, 67), (81, 68), (81, 69), (81, 70),
                     (81, 71), (81, 72), (81, 73), (81, 72),
                     (81, 73), (81, 74), (81, 75), (81, 76),
                     (81, 77), (81, 78), (81, 79), (81, 80)
                     ]
        for x in range(len(col_types)):
            physics_system.add_collision_handler(
                col_types[x][0],col_types[x][1],
                begin_func=self.true,
                pre_solve_func=self.false)

    def update(self, dt):
        self.gameworld.update(dt)

    def setup_states(self):
        self.gameworld.add_state(state_name='main', 
            systems_added=[rendertop, render, render2, 'camera1', 'particle_renderer','rotate'],
            systems_removed=[],
            systems_paused= ['cymunk_physics', 'cymunk_touch', 'boundary', 'rotation',],
            systems_unpaused= ['position', 'rotate', 'color', 'scale',
                              rendertop, render, render2, 'camera1',
                              'particles', 'emitters', 'particle_renderer',],
            screenmanager_screen='main')

        self.gameworld.add_state(state_name='pause',
            systems_added=[],
            systems_removed=[],
            systems_paused=['position', 'rotate', 'color', 'scale',
                            'cymunk_physics', 'cymunk_touch',
                            rendertop, render, render2, 'camera1',
                            'particles', 'emitters', 'particle_renderer',
                            'boundary', 'rotation',],
            systems_unpaused=[],
            screenmanager_screen='main')

    def setup_states2(self):
        sys_unpaused = ['position', 'rotate', 'color', 'scale',
                            rendertop, render, render2, 'camera1',
                            'particles', 'emitters', 'particle_renderer',]

        self.gameworld.add_state(state_name='resume',
            systems_added=[],
            systems_removed=[],
            systems_paused=[],
            systems_unpaused=sys_unpaused+sysbox,
            screenmanager_screen='main')

    def set_state(self):
        self.gameworld.state = 'main'

class Gloworld(App):

    def on_pause(self):
        self.root.clear_up()
        return True

    def on_resume(self):
        self.root.restore()

if __name__ == '__main__':
    Gloworld().run()
