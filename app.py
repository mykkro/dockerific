# app.py

import yaml
from flask import Flask, render_template, jsonify, make_response
from dockerific import load_dockerific_project, DockerificValidator, DockerificRenderer, Dockerific


# https://stackoverflow.com/questions/34667108/ignore-dates-and-times-while-parsing-yaml
class NoDatesSafeLoader(yaml.SafeLoader):
    @classmethod
    def remove_implicit_resolver(cls, tag_to_remove):
        """
        Remove implicit resolvers for a particular tag

        Takes care not to modify resolvers in super classes.

        We want to load datetimes as strings, not dates, because we
        go on to serialise as json which doesn't have the advanced types
        of yaml, and leads to incompatibilities down the track.
        """
        if not 'yaml_implicit_resolvers' in cls.__dict__:
            cls.yaml_implicit_resolvers = cls.yaml_implicit_resolvers.copy()

        for first_letter, mappings in cls.yaml_implicit_resolvers.items():
            cls.yaml_implicit_resolvers[first_letter] = [(tag, regexp) 
                                                         for tag, regexp in mappings
                                                         if tag != tag_to_remove]

NoDatesSafeLoader.remove_implicit_resolver('tag:yaml.org,2002:timestamp')


app = Flask(__name__)

@app.route("/project/<projectname>")
def project(projectname):
    # load static data
    with open('version', 'r') as file:
        version = file.read()
    return render_template("base.html", title="Dockerific", version=version, projectname=projectname)

@app.route("/api/schema")
def api_schema():
    dockerific_schema_path = "dockerific.schema.v1.0.yaml"
    with open(dockerific_schema_path, 'r') as file:
        data = yaml.load(file, Loader=NoDatesSafeLoader)    
    return jsonify(data)


dockerific_schema_path = "dockerific.schema.v1.0.yaml"
with open(dockerific_schema_path, 'r', encoding="utf-8") as infile:
    schema = yaml.safe_load(infile)
    
dv = DockerificValidator(schema)


@app.route("/api/project/<projectname>/dockerfile")
def api_project_dockerfile(projectname):
    dockerific_project_path = f"projects/{projectname}/Dockerfile"
    with open(dockerific_project_path, 'r') as file:
        dockerfile = file.read()
    response = make_response(dockerfile, 200)
    response.mimetype = "text/plain"
    return response

@app.route("/api/project/<name>/generate", methods = ['POST'])
def api_project_generate(name):
    dockerific_project_path = f"projects/{name}"

    with open(f"{dockerific_project_path}/dockerific.yaml", 'r', encoding="utf-8") as infile:
        raw = yaml.safe_load(infile)
        errors = dv.validate_dockerific_data(raw)
        if len(errors) > 0:
            return jsonify(dict(status="error", errors=errors))
        
        data = Dockerific.from_dict(raw, dockerific_project_path)

    dockerfile = data.dockerify()

    dockerfile_path = f"{dockerific_project_path}/Dockerfile"
    with open(dockerfile_path, 'w', encoding="utf-8") as outfile:
        outfile.write(dockerfile)

    dockerbuild_path = f"{dockerific_project_path}/build.sh"
    with open(dockerbuild_path, 'w', encoding="utf-8") as outfile:
        outfile.write(f"#!/bin/bash\n\n{data.build_command()}")

    return jsonify(dict(status="ok", message=f"Dockerfile and build.sh generated for project {name}!"))


@app.route("/api/project/<name>")
def api_project(name):
    dockerific_project_path = f"projects/{name}"
    dockerific_yaml_path = f"{dockerific_project_path}/dockerific.yaml"
    with open(dockerific_yaml_path, 'r') as file:
        data = yaml.load(file, Loader=NoDatesSafeLoader)    
    return jsonify(data)




if __name__ == "__main__":
    app.run(debug=True)