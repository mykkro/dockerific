import sys
sys.path.append("..")

import yaml
from dockerific import load_dockerific_project


if __name__ == "__main__":

    dockerific_project_path = "../projects/ros2-foxy-moveit"
    data = load_dockerific_project(dockerific_project_path)

    dockerfile = data.dockerify()
    print(dockerfile)

    dockerfile_path = f"{dockerific_project_path}/Dockerfile"
    with open(dockerfile_path, 'w', encoding="utf-8") as outfile:
        outfile.write(dockerfile)

    dockerbuild_path = f"{dockerific_project_path}/build.sh"
    with open(dockerbuild_path, 'w', encoding="utf-8") as outfile:
        outfile.write(f"#!/bin/bash\n\n{data.build_command()}")