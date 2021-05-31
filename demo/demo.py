from gomer.robot import Robot
import time
if __name__ == '__main__':
    robot = Robot('Gomer_a2dc6e')
    for i in range(4):
        robot.straight_move(1, 400)
        robot.turn(1, 90)
    robot.tts("haha, I can draw a square", 'square')
    robot.play('square')
    time.sleep(3)
    robot.play_emotion('hrt_a')
