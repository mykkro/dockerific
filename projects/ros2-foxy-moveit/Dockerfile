FROM ros:foxy
ENV DOCKER_IMAGE_VER=3.0
ENV HOME=/home/rosdemos
ENV ROS2_WORKSPACE=workspace
ENV LIBDIR=libs
ARG ROS_DISTRO=foxy
# Basic Packages install
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    curl \
    gnupg \
    lsb-release \
    git \
    apt-utils \
    python3-dev \
    python3-distutils \
    python3-pip \
    unzip \
    sudo \
    wget \
    software-properties-common \
    iputils-ping \
    vim \
    figlet \
    toilet \
    mc \
    featherpad \
    dos2unix \
    tmux \
    libpoco-dev \
    libeigen3-dev \
    ros-foxy-ament-cmake-clang-format
RUN mkdir -p $HOME && cd $HOME && wget https://github.com/foxglove/studio/releases/download/v1.45.0/foxglove-studio-1.45.0-linux-amd64.deb && apt install $HOME/foxglove-studio-*.deb -y
# ROS Packages install
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    vim \
    iputils-ping \
    ros-${ROS_DISTRO}-gazebo-ros-pkgs \
    ros-${ROS_DISTRO}-xacro \
    python3-rosdep \
    python3-colcon-common-extensions \
    python3-colcon-mixin \
    python3-vcstool
RUN rosdep update --rosdistro=$ROS_DISTRO && apt dist-upgrade
RUN mkdir -p $HOME/$ROS2_WORKSPACE
RUN mkdir -p $HOME/$LIBDIR
RUN git clone https://github.com/frankaemika/libfranka.git --recursive $HOME/$LIBDIR/libfranka && cd $HOME/$LIBDIR/libfranka && mkdir $HOME/$LIBDIR/libfranka/build && cd $HOME/$LIBDIR/libfranka/build && cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTS=OFF  .. && cmake --build . -j$(nproc) && cpack -G DEB && sudo dpkg -i libfranka-*.deb
# franka_ros2
RUN mkdir -p $HOME/$ROS2_WORKSPACE/src/franka_ros2 && \
    git clone \
    https://github.com/frankaemika/franka_ros2.git \
    $HOME/$ROS2_WORKSPACE/src/franka_ros2
# Moveit2
RUN mkdir -p $HOME/$ROS2_WORKSPACE/src/moveit2 && \
    git clone \
    -b $ROS_DISTRO \
    https://github.com/ros-planning/moveit2.git \
    $HOME/$ROS2_WORKSPACE/src/moveit2
# Simulation - Joint State Publisher
RUN mkdir -p $HOME/$ROS2_WORKSPACE/src/joint_state_publisher && \
    git clone \
    -b $ROS_DISTRO \
    https://github.com/ros/joint_state_publisher \
    $HOME/$ROS2_WORKSPACE/src/joint_state_publisher
RUN mkdir -p $HOME/$ROS2_WORKSPACE/src/ros2_control && \
    git clone \
    -b $ROS_DISTRO \
    https://github.com/ros-controls/ros2_control.git \
    $HOME/$ROS2_WORKSPACE/src/ros2_control
RUN mkdir -p $HOME/$ROS2_WORKSPACE/src/moveit2_tutorials && \
    git clone \
    -b $ROS_DISTRO \
    --depth 1 \
    https://github.com/ros-planning/moveit2_tutorials.git \
    $HOME/$ROS2_WORKSPACE/src/moveit2_tutorials
RUN cd $HOME/$ROS2_WORKSPACE/src && vcs import < $HOME/$ROS2_WORKSPACE/src/moveit2_tutorials/moveit2_tutorials.repos && rosdep update && rosdep install -r --ignore-src --rosdistro $ROS_DISTRO --from-paths . -y
RUN cd $HOME/$ROS2_WORKSPACE && . /opt/ros/$ROS_DISTRO/setup.sh && colcon build
RUN echo "source $HOME/$ROS2_WORKSPACE/install/setup.bash" >> /root/.bashrc
RUN echo "figlet -c -f slant MOVEIT2 TUTORIAL" >> /root/.bashrc
RUN echo "echo 'ROS2 sourced, sail away'" >> /root/.bashrc

COPY run_tmux.sh $HOME/workspace/run_tmux.sh
RUN dos2unix $HOME/workspace/run_tmux.sh
RUN chmod +x $HOME/workspace/run_tmux.sh
WORKDIR $HOME/workspace
CMD ["/bin/bash", "-c" ]