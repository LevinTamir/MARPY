import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import termios
import tty

def get_key():
    """Read a single key press from the terminal."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key

class TeleopKeyboard(Node):
    def __init__(self):
        super().__init__('teleop_keyboard')
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.speed = 0.5
        self.turn = 1.0

        self.move_bindings = {
            'i': (1, 0, 0, 0),
            'o': (1, 0, 0, -1),
            'j': (0, 0, 0, 1),
            'l': (0, 0, 0, -1),
            'u': (1, 0, 0, 1),
            ',': (-1, 0, 0, 0),
            '.': (-1, 0, 0, -1),
            'm': (-1, 0, 0, 1),
        }

        self.speed_bindings = {
            'q': (1.1, 1.1),
            'z': (0.9, 0.9),
            'w': (1.1, 1.0),
            'x': (0.9, 1.0),
            'e': (1.0, 1.1),
            'c': (1.0, 0.9),
        }

    def run(self):
        print(self.get_instructions())
        try:
            while True:
                key = get_key()
                if key in self.move_bindings.keys():
                    x, y, z, th = self.move_bindings[key]
                elif key in self.speed_bindings.keys():
                    self.speed *= self.speed_bindings[key][0]
                    self.turn *= self.speed_bindings[key][1]
                    print(f"Speed: {self.speed}, Turn: {self.turn}")
                    continue
                else:
                    x, y, z, th = 0, 0, 0, 0

                twist = Twist()
                twist.linear.x = x * self.speed
                twist.linear.y = y * self.speed
                twist.linear.z = z * self.speed
                twist.angular.z = th * self.turn
                self.cmd_pub.publish(twist)
                self.get_logger().info('Message sent')

                if key == '\x03':  # Ctrl+C
                    break
        except Exception as e:
            print(e)
        finally:
            twist = Twist()
            self.cmd_pub.publish(twist)

    @staticmethod
    def get_instructions():
        return """
Control your robot with the following keys:

---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .
   

anything else : stop

q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%
        """

def main(args=None):
    rclpy.init(args=args)
    teleop_node = TeleopKeyboard()
    teleop_node.run()

    rclpy.shutdown()

if __name__ == '__main__':
    main()