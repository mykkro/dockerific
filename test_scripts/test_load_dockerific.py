import sys
sys.path.append("..")

import yaml
from dockerific import load_dockerific_project, DockerificValidator, DockerificRenderer


if __name__ == "__main__":

    dockerific_schema_path = "../dockerific.schema.v1.0.yaml"
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

    with open(dockerific_schema_path, 'r', encoding="utf-8") as infile:
        schema = yaml.safe_load(infile)

    print(schema)

    with open(dockerific_project_path + "/dockerific_with_errors.yaml", 'r', encoding="utf-8") as infile:
        raw = yaml.safe_load(infile)


    
    
    dv = DockerificValidator(schema)
    errors = dv.validate_dockerific_data(raw)
    print(errors)

    dr = DockerificRenderer(schema)
    dr.render_dockerific_data(raw)