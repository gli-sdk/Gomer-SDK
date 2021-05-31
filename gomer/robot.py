
from .motion import *
from .transceiver import *
from .player import *
from .sensor import *
from .face_detection import *
from .hardware import *
from .screen import *
from .uploader import *
from .emotion import *
from .pattern_detection import *
from .video import *
import logging


class Robot(object):
    def __init__(self, name):
        self.__name = name
        self._logger = logging.getLogger('gomer.robot')
        self.__handler = Handler()
        self.__start_handler()
        self._connection = Connection()
        self._hardware = Hardware()

        self.__connect()
        self._wheel = Wheel()
        self._forearm = Forearm()
        self._arm = Arm()
        self._head = Head()
        self._paw = Paw()

        self._player = Player()
        self._screen = Screen()
        self._sensor = Sensor()
        self._uploader = Uploader()

        self._emotion = Emotion()
        self._face_detection = FaceDetection()
        self._video = Video()
        self._pattern_detection = PatternDetection()

    def __del__(self):
        self._connection.destroy()
        time.sleep(2)

    def __start_handler(self):
        """start a thread for handling messages from gomer."""
        handle_thread = threading.Thread(target=self.__handler.handle,
                                         args=(Connection.message_queue,))
        handle_thread.setDaemon(True)
        handle_thread.start()

    def __connect(self):
        """connect gomer."""
        self._connection.connect(self.__name)
        self._hardware.check_version()

    # Sensors (including gyroscope, infrared, cliff_detection) and Lights
    def set_light_color(self, r=255, g=255, b=255):
        """set light color, if you want to change the color of light, try this function
        before light_on().

        :param r: int 0~255 (red), default 255
        :param g: int 0~255 (green), default 255
        :param b: int 0~255 (blue), default 255
        """
        self._sensor.set_light_color(r, g, b)

    def set_light_mode(self, mode='on', duration=3000, on_time=1000, off_time=1000):
        """set light mode

        :param mode: (on, blink, breathe)
                on  light will be alaways on,  default
                blink  light will blink, you should set the on_time and off_time
                breathe  light will breathe
        :param duration: int 0~30000 (ms), if 0, light will be always on. default 3000
        :param on_time: int 0~10000 (ms), take effect if mode is blink or breathe, default 1000
        :param off_time: int 0~10000 (ms), take effect if mode is blink or breathe, default 1000
        """
        self._sensor.set_light_mode(mode, duration, on_time, off_time)

    def light_on(self):
        """open light"""
        self._sensor.light_on()

    def light_off(self):
        """light off"""
        self._sensor.light_off()

    def turn_on_cliff_detection(self):
        self._sensor.turn_on_cliff_detection()

    def turn_off_cliff_detection(self):
        self._sensor.turn_off_cliff_detection()

    def read_infrared(self, location):
        """Gomer has 2 infrared sensors in his body, one is in the front, another is in the end.

        :param location: (front, end)
                    front read the front infrared sensor.
                    end  read the end infrared sensor.
        :return: int 0~4096, increase when obstacle is faraway
        """
        return self._sensor.read_infrared(location)

    def read_gyroscope(self):
        """Read the reading of gyroscope in Gomer.

        :rtype: tuple[float, float, float,float]
        :return: quaternion of gyroscope: w, x, y, z.
        """
        return self._sensor.read_gyroscope()

    def read_gyroscope2(self):
        """Read the reading of gyroscope in Gomer.

        :rtype: tuple[float, float, float]
        :return: euler angles of gyroscope: pitch, roll, yaw.
        """
        w, x, y, z = self._sensor.read_gyroscope()
        return self._sensor.quaternion_to_euler_angles(w, x, y, z)

    # Motion (including wheels, arm, forearm, head, hand)
    def move_in_open_loop(self, speed, timeout=3000, block='auto'):
        """open loop control for wheels of Gomer.

        :param speed: int -2~2 not 0
        :param timeout: int 0~10000 (ms), default 3000, the wheel will not stop until time is out.
        :param block: str (auto, never, all)
                    auto: function callings in the same group after this instruction will be waiting until this
                            instruction is over.
                    never: when a new function about wheel is called after this instruction.  if this instruction
                            is not over, gomer will execute the new function.
                    all: all function callings after this instruction will be waiting until this instruction is over.
        """
        self._wheel.move(speed, timeout, block=block)

    def straight_move(self, speed, distance, timeout=3000, block='auto'):
        """Gomer will move straight foward or backward, depends on the sign of distance.

        :param speed: int 1~3
        :param distance: int -1000~1000 (mm)
        :param timeout: int 0~10000, default 3000, this function will be over if timeout or Gomer reach the distance
                        generally, you don't need to set this parameter.
        :param block: str (auto, never, all)
                    auto: function callings in the same group after this instruction will be waiting until this
                            instruction is over.
                    never: when a new function about wheel is called after this instruction.  if this instruction
                            is not over, gomer will execute the new function.
                    all: all function callings after this instruction will be waiting until this instruction is over.
        """
        self._wheel.move_directly(
            speed, distance, timeout=timeout, block=block)

    def turn(self, speed, angle, timeout=3000, block='auto'):
        """closed-loop control for turn function

        :param speed: int 1~3
        :param angle: int -360 ~ 360 (degrees)
        :param timeout: int 0~10000, default 3000, this function will be over if timeout or Gomer reach the angle
                        generally, you don't need to set this parameter.
        :param block: str (auto, never, all)
                    auto: function callings in the same group after this instruction will be waiting until this
                            instruction is over.
                    never: when a new function about wheel is called after this instruction.  if this instruction
                            is not over, gomer will execute the new function.
                    all: all function callings after this instruction will be waiting until this instruction is over.
        """
        self._wheel.turn(speed, angle, timeout=timeout, block=block)

    def forearm_move_in_open_loop(self, speed, timeout=3000, block='auto'):
        """open-loop control for forearm. not accurate.

        :param speed: int -2~2 not 0
        :param timeout: int 0~10000, default 3000, this function will be over if timeout or Gomer reach the angle
                        generally, you don't need to set this parameter.
        :param block: str (auto, never, all)
                    auto: function callings in the same group after this instruction will be waiting until this
                            instruction is over.
                    never: when a new function about wheel is called after this instruction.  if this instruction
                            is not over, gomer will execute the new function.
                    all: all function callings after this instruction will be waiting until this instruction is over.
        """
        self._forearm.open_loop_move(speed, timeout, block)

    def forearm_move(self, speed, angle, timeout=3000, block='auto'):
        """closed-loop control for forearm.

        :param speed: int 1~3
        :param angle: int 0 ~ 210 (degrees)
        :param timeout: int 0~10000, default 3000, this function will be over if timeout or Gomer reach the angle
                        generally, you don't need to set this parameter.
        :param block: str (auto, never, all)
                    auto: function callings in the same group after this instruction will be waiting until this
                            instruction is over.
                    never: when a new function about wheel is called after this instruction.  if this instruction
                            is not over, gomer will execute the new function.
                    all: all function callings after this instruction will be waiting until this instruction is over.
        """
        self._forearm.closed_loop_move(
            speed, angle, timeout=timeout, block=block)

    def arm_move_in_open_loop(self, speed, timeout=3000, block='auto'):
        """open-loop control for arm. not accurate.

        :param speed: int -2~2 not 0
        :param timeout: int 0~10000, default 3000, this function will be over if timeout or Gomer reach the angle
                        generally, you don't need to set this parameter.
        :param block: str (auto, never, all)
                    auto: function callings in the same group after this instruction will be waiting until this
                            instruction is over.
                    never: when a new function about wheel is called after this instruction.  if this instruction
                            is not over, gomer will execute the new function.
                    all: all function callings after this instruction will be waiting until this instruction is over.
        """
        self._arm.open_loop_move(speed, timeout, block)

    def arm_move(self, speed, angle, timeout=3000, block='auto'):
        """closed-loop control for arm.

        :param speed: int 1~3
        :param angle: int 0 ~ 160 (degrees)
        :param timeout: int 0~10000, default 3000, this function will be over if timeout or Gomer reach the angle
                        generally, you don't need to set this parameter.
        :param block: str (auto, never, all)
                    auto: function callings in the same group after this instruction will be waiting until this
                            instruction is over.
                    never: when a new function about wheel is called after this instruction.  if this instruction
                            is not over, gomer will execute the new function.
                    all: all function callings after this instruction will be waiting until this instruction is over.
        """
        self._arm.closed_loop_move(speed, angle, timeout=timeout, block=block)

    def head_move_in_open_loop(self, speed, timeout=3000, block='auto'):
        """open-loop control for arm. not accurate.

        :param speed: int -2~2 not 0
        :param timeout: int 0~10000, default 3000, this function will be over if timeout or Gomer reach the angle
                        generally, you don't need to set this parameter.
        :param block: str (auto, never, all)
                    auto: function callings in the same group after this instruction will be waiting until this
                            instruction is over.
                    never: when a new function about wheel is called after this instruction.  if this instruction
                            is not over, gomer will execute the new function.
                    all: all function callings after this instruction will be waiting until this instruction is over.
        """
        self._head.open_loop_move(speed, timeout=timeout, block=block)

    def head_move(self, speed, angle, timeout=3000, block='auto'):
        """closed-loop control for arm.

        :param speed: int 1~3
        :param angle: int -15 ~ 65 (degrees)
        :param timeout: int 0~10000, default 3000, this function will be over if timeout or Gomer reach the angle
                        generally, you don't need to set this parameter.
        :param block: str (auto, never, all)
                    auto: function callings in the same group after this instruction will be waiting until this
                            instruction is over.
                    never: when a new function about wheel is called after this instruction.  if this instruction
                            is not over, gomer will execute the new function.
                    all: all function callings after this instruction will be waiting until this instruction is over.
        """
        self._head.closed_loop_move(speed, angle, timeout=timeout, block=block)

    def paw_move_in_open_loop(self, speed, timeout=3000, block='auto'):
        """open-loop control for arm. not accurate.

        :param speed: int -2~2 not 0
        :param timeout: int 0~10000, default 3000, this function will be over if timeout or Gomer reach the angle
                        generally, you don't need to set this parameter.
        :param block: str (auto, never, all)
                    auto: function callings in the same group after this instruction will be waiting until this
                            instruction is over.
                    never: when a new function about wheel is called after this instruction.  if this instruction
                            is not over, gomer will execute the new function.
                    all: all function callings after this instruction will be waiting until this instruction is over.
        """
        self._paw.open_loop_move(speed, timeout, block)

    def paw_move(self, speed, angle, timeout=3000, block='auto'):
        """closed-loop control for arm.

        :param speed: int 1~3
        :param angle: int 0 ~ 100 (degrees)
        :param timeout: int 0~10000, default 3000, this function will be over if timeout or Gomer reach the angle
                        generally, you don't need to set this parameter.
        :param block: str (auto, never, all)
                    auto: function callings in the same group after this instruction will be waiting until this
                            instruction is over.
                    never: when a new function about wheel is called after this instruction.  if this instruction
                            is not over, gomer will execute the new function.
                    all: all function callings after this instruction will be waiting until this instruction is over.
        """
        self._paw.closed_loop_move(speed, angle, timeout=timeout, block=block)

    # player module
    def tts(self, string, filename):
        """text to speak, filename is used for play()

        :param string: str len(string) < 100
        :param filename: str len(str) < 10
        """
        self._player.tts(string, filename)

    def play(self, filename):
        """play voice file

        :param filename: str
        """
        self._player.play_file(filename)

    def get_play_status(self):
        """get player status

        :rtype: bool
        :return: if player is busy, return True, else return False.
        """
        return self._player.get_play_status()

    def set_volume(self, volume):
        """set volume of Gomer.

        :param volume: int 1~5
        """
        self._player.set_volume(volume)

    def get_volume(self):
        """get volume of Gomer.

        :return volume: int 1~5
        """
        return self._player.get_volume()

    def stop_playing(self):
        """stop a voice"""
        return self._player.stop()

    # File operations
    def upload(self, path):
        """upload a image or voice file.

        :param path: path of file. file_types:
                    image: .jpg .jpeg .png .bmp
                    voice: .mp3 .wav
        """
        self._uploader.upload(path)

    # Screen
    def show_image(self, image):
        """show image, before showing the image, you should upload the image first.
        if you want to show another image, you should wait at least 1 second, or
        the instruction will be ignored.

        :param image: string  filename of the image.
        """
        self._screen.show_image(image)

    def get_show_status(self):
        """get screen status

        :rtype: bool
        :return: if screen is busy, return True, else return False.
        """
        return self._screen.is_showing()

    def show_camera(self):
        """Gomer will show camera in his face."""
        self._screen.show_camera()

    def stop_showing(self):
        """stop screen show of gomer."""

        self._screen.stop_showing()

    # Emotion
    def play_emotion(self, emotion):
        """play emotion. for example: play_emotion('a_apl')

        :param emotion: str, now we have emotions below:
                        a_apl: letter a for apple
                        agy_a: angry
                        b_blk: letter b for block
                        c_cat: letter c for cat
                        cat_a: see a cat
                        dbt_a: doubt
                        dizy: dizziness
                        dns_a: turn and dance
                        dog_a: see a dog
                        hi_a: greeting hi
                        hi_b: greeting hi
                        hll_a: say hello
                        hpy_a: happy
                        hpy_b: happy
                        hpy_sl: happy with shy
                        hpy_swl: happy with show off
                        hrt_a: love heart
                        nap_a: nap
                        nap_b: nap
                        obt_a: blindfolded eyes
                        obt_b: blindfolded eyes
                        obt_c: blindfolded eyes
                        scr_a: scared
                        scr_b: scared
                        sd_a: sad
                        sd_e: sad
                        sgh_a: sigh
                        shy_a: shy
                        slp_a: sleep
                        snz_a: sneeze
                        sok_a: shocked
                        sok_wt: shocked
                        st_a: star in eyes
                        td_a: exciting tada
                        wgl_a: joggle to wake up
                        ywn_a: stretch
                        ywn_b: stretch
                        hry: say how are you
                        ntsy: say nice to see you
                        song_a: sing little star
                        song_b: jingle bell
                        song_c: ten little fingers
        """
        self._emotion.play_emotion(emotion)

    def turn_on_expression(self):
        """when Gomer is playing emotion, turn on the expression in face"""
        self._emotion.turn_on_expression()

    def turn_off_expression(self):
        """when Gomer is playing emotion, turn off the expression in face"""
        self._emotion.turn_off_expression()

    def turn_on_motion(self):
        """when Gomer is playing emotion, turn on the motion of wheels and arms"""
        self._emotion.turn_on_motion()

    def turn_off_motion(self):
        """when Gomer is playing emotion, turn off the motion of wheels and arms"""

        self._emotion.turn_off_motion()

    def stop_emotion(self):
        self._emotion.stop()

    def get_emotion_status(self):
        """get emotion status

        :rtype: bool
        :return: if Gomer is playing emotion, return True, else return False.
        """
        return self._emotion.is_showing()

    # face-detection
    def detect_face(self, min_size=10, max_size=300):
        """detect face, gomer can detect at most 5 faces once, usually 1 or 2.

        :param min_size: int 10 <= min_size <= 300, default 10, generally you just keep it default.
        :param max_size: int 10 <= max_size <= 300, default 300, generally you just keep it default.

        :rtype: list[list]
        :return: list of faces, each face is a list like [int, int, int, int].
                 four ints in face stands for [x, y, w, h]. x, y is the coordinate
                 of the left-top point of face, w is width, h is height.
        """
        return self._face_detection.detect_face(min_size, max_size)

    def get_face_feature(self, index):
        """ get face feature point, before get face feature, you should use detect_face() method

        :param index: int 0 <= index <= len(faces) -1
        :return: coordinate of five feature_points [[int, int], [int, int], [int, int], [int, int], [int, int]]
        """
        return self._face_detection.get_face_feature(index)

    def register_face(self, index, name):
        """register face to database, before get face feature, you should use detect_face() method

        :param index: int 0 <= index <= len(faces) -1
        :param name: str  length <= 10
        """

        self._face_detection.register_face(index, name)

    def get_name(self, index):
        """get face name, before get name, you should use detect_face() method

        :param index: int 0 <= index <= len(faces) -1
        :return: str name of the face
        """
        self._face_detection.get_name(index)

    def generate_face_feature_file(self, index, filename):
        """store a face feature file in Gomer, before generate file, you should use detect_face() method

        :param index: int 0 <= index <= len(faces) -1
        :param filename: str len(str) <= 10
        """

        self._face_detection.set_face_feature_file(index, filename)

    def calc_similarity(self, name1, name2):
        """ calc similarity of 2 faces, before calc similarity, you should use detect_face() method
        and use generate_face_feature_file() generate at least 2  face feature file.

        :param name1: face feature filename of name1, generated by generate_face_feature_file()
        :param name2: face feature filename of name2, generated by generate_face_feature_file()
        :return: similartiry 0~100
        """
        return self._face_detection.get_similarity(name1, name2)

    def rename(self, old_name, new_name):
        """rename a face, you should use detect_face() method or you can get_face_list() to see the
        faces in Gomer database.

        :param old_name:
        :param new_name: str len(str) <= 10
        """
        self._face_detection.rename(old_name, new_name)

    def get_face_list(self):
        """get faces in Gomer database.

        :return: list[str]
        """
        return self._face_detection.get_face_list()

    def turn_to_face(self):
        """When gomer detect only 1 face, he can turn to the face."""
        width = 320
        height = 180
        faces = self.detect_face()

        if faces:
            face = faces[0]
            x = face[0] + face[2] / 2
            diff_x = x - width / 2
            if diff_x < -20:
                self._turn_and_see(-10, diff_x)
            elif diff_x > 20:
                self._turn_and_see(10, diff_x)
            else:
                print('already turn to face.')
                return
        else:
            print('can not see the face.')

    def _turn_and_see(self, angle, diff_x):
        width = 320
        self.turn(2, angle)
        n_faces = self.detect_face()
        if n_faces:
            n_face = n_faces[0]
            n_x = n_face[0] + n_face[2] / 2
            n_diff_x = n_x - width / 2
            if n_diff_x < -20:
                diff_angle = self._calc_diff_angle2(10, diff_x, n_diff_x)
                self.turn(2, -diff_angle)
            elif n_diff_x > 20:
                diff_angle = self._calc_diff_angle2(10, diff_x, n_diff_x)
                self.turn(2, diff_angle)
            else:
                return

    @staticmethod
    def _calc_diff_angle(angle, distance, n_distance):
        # angle = 10
        cos = 0.9848
        sin = 0.1736
        tan = 0.1763
        ratio = n_distance / distance
        direction = True
        if ratio < 0:
            direction = False
        n_distance = abs(n_distance)
        distance = abs(distance)
        if direction:
            ratio = 1.2 * ratio
            c = abs(math.pow(1 - ratio * cos, 2) - 4 * ratio * sin * tan)
            tan_theta = (1 - ratio * cos + math.sqrt(c)) / (2 * ratio * sin)
            theta = math.degrees(math.atan(tan_theta))
        else:
            theta = math.degrees(math.atan(distance * sin / (distance * cos + n_distance)))

        print(angle - theta)
        return int(abs(angle - theta))

    @staticmethod
    def _calc_diff_angle2(angle, distance, n_distance):
        print(distance)
        print(n_distance)
        theta = (angle * distance) / (distance - n_distance) - angle
        return int(theta)

    # pattern detection
    def detect_pattern(self, group, min_size=10, max_size=300):
        """

        :param group: str in ('all', 'number','letter','animal','custom')
        :param min_size: int 10 <= min_size <= 300, default 10, generally you just keep it default.
        :param max_size: int 10 <= max_size <= 300, default 300, generally you just keep it default.
        :return:list[pattern_points]
                pattern_points: [lux, luy, lbx, lby, rbx, rby, rux, ruy]
                        lu: left upper point
                        lb: left bottom point
                        rb: right bottom point
                        ru: right upper point
        """
        self._pattern_detection.detect_pattern(group=group, min_size=min_size, max_size=max_size)

    def get_pattern_location(self, index=0):
        """get three dimensional coordinate of pattern, you should detect_pattern() first.

        :param index: index of pattern detected from function detect_pattern()
        :return: [float, float, float, float, float, float] stands for [x, y, z, theta_x, theta_y, theta_z]
        """
        self._pattern_detection.get_pattern_location(index)

    def add_custom_pattern(self, pattern_name):
        """add a custom pattern, before you use this function, you should upload the pattern file first.

        :param pattern_name: str,  file must match: sdk1_30x30_name.jpg
                            30x30 means the actual size in mm you want to detect, size should in 30~50 , ratio 1:1
                            for example:  sdk1_30x30_cat.jpg    or   sdk1_40x40_dog.jpg
        """
        self._pattern_detection.add_pattern(pattern_name)

    def get_custom_patterns(self):
        """get custom patterns in Gomer

        :return: list[str]
        """
        return self._pattern_detection.get_custom_patterns()

    def move_to_pattern(self, pattern_name, distance, times=5):
        """move to pattern

        :param pattern_name:  for example: std_a_cat.jpg
                    animals: std_a_cat.jpg std_a_dog.jpg std_a_panda.jpg
                    numbers: std_n_0.jpg ~ std_n_9.jpg
                    letters: std_l_A.jpg ~ std_l_Z.jpg
                    custom: your custom pattern
                    blocks: std_c_G.jpg std_c_L.jpg std_c_I.jpg

        :param distance:
        :param times: int default 5, to avoid infinte loop, Gomer will try at most 5 times.
                        you can set it yourself.
        """
        for i in range(times):
            result = self._pattern_detection.move_to_pattern(pattern=pattern_name, distance=distance)
            if not result:
                return
            head, turn_1, move, turn_2 = result
            if head != 255:
                self.head_move(2, head)
            if turn_1 != 0:
                self.turn(2, turn_1)
            if move != 0:
                self.straight_move(2, move)
            if turn_2 != 0:
                self.turn(2, turn_2)

    # video
    def open_video(self):
        """open video, you will see a video in your PC, the video shows what Gomer's camera see."""
        self._video.open_video()

    def close_video(self):
        """close video"""
        self._video.close_video()

    def open_video_data(self):
        """open video data stream, you can capture a image from the data stream
        with get_image_from_video()
        """
        self._video.open_video_data(Connection.yuvs)

    def close_video_data(self):
        """close video data stream"""
        self._video.close_video_data()

    def get_image_from_video(self):
        """get image from video, before you use this function, you must open_video_data() first.

        :return: BGR data in opencv
        """
        return self._video.get_image()
