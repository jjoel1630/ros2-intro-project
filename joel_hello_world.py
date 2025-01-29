import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from ackermann_msgs.msg import AckermannDriveStamped, AckermannDrive

class AckermannPublisher(Node):
    def __init__(self):
        super().__init__('joel_drive_publisher')
        self.laser_subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.lidar_callback,
            10
        )

        self.publisher = self.create_publisher(
            AckermannDriveStamped, 
            '/ackermann_cmd',
            10
		)
    def lidar_callback(self, msg):
        # Get the middle value of the lidar: msg.ranges[500]
        lidar_reading = msg.ranges[500]
        self.get_logger().info(f'Lidar reading: {lidar_reading}')

        speed = 0.5
        if lidar_reading > 0.5:
            speed = 0.5
        else:
            speed = 0.0

        stamped_msg = AckermannDriveStamped()
        stamped_msg.drive = AckermannDrive()
        stamped_msg.drive.steering_angle = 0.0
        stamped_msg.drive.speed = speed

        self.publisher.publish(stamped_msg)

def main(args=None):
    rclpy.init(args=args)
    ackermann_publisher = AckermannPublisher()
    rclpy.spin(ackermann_publisher)
    
    ackermann_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()