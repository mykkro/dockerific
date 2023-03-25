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
                return True
            if type == "string_list":
                for item in value:
                    if not DockerificValidator.validate_type(item, "string"):
                        print("Type validation failed:", value, type)
                        return False
                return True
            if type == "int" and isinstance(value, int):
                return True
            if type == "bool" and isinstance(value, bool):
                return True
            print("Type validation failed:", value, type)
            return False

        @staticmethod
        def validate_prop(act, prop):
            prop_key = prop["key"]
            prop_required = prop.get("required", False)
            prop_type = prop["type"]
            prop_default = prop.get("default")
            prop_value = act.get(prop_key, prop_default)
            if not prop_required and prop_value is None:
                return True
            print(prop_key, prop_required, prop_type, prop_value)
            assert(not prop_required or prop_value is not None)
            if not DockerificValidator.validate_type(prop_value, prop_type):
                print("Type validation failed for field:", prop_key)     
                return False   
            return True    

        @staticmethod
        def validate_action(act, schema):
            print("Validating action against schema...")
            schema_title = schema.get("title") 
            schema_description = schema.get("description") 
            title = act.get("title") # every action can have a Title
            for prop in schema["props"]:
                if not DockerificValidator.validate_prop(act, prop):
                    print("Action validation failed:", act)
                    return False
            return True


        def validate_dockerific_data(self, raw):
            print("Validating data against schema...")
            assert(self.schema["$type"] == "cz.mykkro.dockerific.schema")
            assert(raw["$type"] == "cz.mykkro.dockerific")
            assert(self.schema["$version"] == raw["$version"])
            actions = self.schema["build_actions"]
            action_keys = set(actions.keys())

            for act in raw["build"]:
                type = self.determine_action_type(act, action_keys)
                if type is None:
                    print("Invalid action - no type recognized", act, action_keys)
                    return False
                
                if not self.validate_action(act, actions[type]):
                    return False
            
            return True

    dv = DockerificValidator(schema)
    dv.validate_dockerific_data(raw)