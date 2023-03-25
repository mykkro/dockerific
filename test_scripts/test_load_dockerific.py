import sys
sys.path.append("..")

import yaml
from dockerific import load_dockerific_project


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

    with open(dockerific_project_path + "/dockerific.yaml", 'r', encoding="utf-8") as infile:
        raw = yaml.safe_load(infile)


    
    # schema can be used for validating the raw YAML data
    class DockerificValidator(object):
        def __init__(self, schema):
            self.schema = schema

        @staticmethod
        def determine_action_type(act, action_keys):
            for key in action_keys:
                if key in act:
                    return key
            return None

        @staticmethod
        def validate_type(value, type):
            if type == "string" and isinstance(value, str):
                return None
            if type == "string_list":
                for item in value:
                    errors = DockerificValidator.validate_type(item, "string")
                    if errors is not None:
                        return errors + [f"Type validation failed: {value} {type}"]
                return None
            if type == "int" and isinstance(value, int):
                return None
            if type == "bool" and isinstance(value, bool):
                return None
            return [f"Type validation failed: {value} {type}"]

        @staticmethod
        def validate_prop(act, prop):
            prop_key = prop["key"]
            prop_required = prop.get("required", False)
            prop_type = prop["type"]
            prop_default = prop.get("default")
            prop_value = act.get(prop_key, prop_default)
            if not prop_required and prop_value is None:
                return None
            print(" ", prop_key, prop_required, prop_type, prop_value)
            assert(not prop_required or prop_value is not None)
            errors = DockerificValidator.validate_type(prop_value, prop_type)
            if errors is not None:
                return errors + [f"Type validation failed for field: {prop_key}"]
            return None    

        @staticmethod
        def validate_action(act, schema):
            for prop in schema["props"]:
                errors = DockerificValidator.validate_prop(act, prop)
                if errors is not None:
                    return errors
            return None


        def validate_dockerific_data(self, raw):
            assert(self.schema["$type"] == "cz.mykkro.dockerific.schema")
            assert(raw["$type"] == "cz.mykkro.dockerific")
            assert(self.schema["$version"] == raw["$version"])
            actions = self.schema["build_actions"]
            action_keys = set(actions.keys())

            for act in raw["build"]:
                type = self.determine_action_type(act, action_keys)
                if type is None:
                    return [f"Invalid action - no type recognized {act} {action_keys}"]

                print("Action:", type, act.get("title"))

                errors = self.validate_action(act, actions[type])
                if errors is not None:
                    return errors
            
            return None

    dv = DockerificValidator(schema)
    errors = dv.validate_dockerific_data(raw)
    print(errors)