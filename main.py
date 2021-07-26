from mako.template import Template
import sys,os


def write_rendered_template_to_file(content, filename):
    try:
        file = open(filename, "w")
        file.write(content)
        file.close()
        print("the content of the rendered template was writen successfully")
    except:
        print("error while writing the content of the rendered template")


def check_arguments(arguments_list):
    arguments_size = len(arguments_list)
    error_message = "-> python3 main.py [ dev <node-name> | prod <nodes-base-name> <nodes-number> ]"
    if arguments_size < 1:
        print(error_message)
        return False
    elif arguments_list[1] == "dev" and arguments_size != 3:
        print(error_message)
        return False
    elif arguments_list[1] == "prod" and arguments_size != 4:
        print(error_message)
        return False

    else:
        return True


def generate_client_dockerfile(elastic_search_container_name):
    try:
        dockerfile_template=Template(filename="dockerfile-tmp")
        rendered_template=dockerfile_template.render(elasticsearch_node_name=elastic_search_container_name)
    except:
        print("error while generating dockerfile")
    write_rendered_template_to_file(rendered_template,"dockerfile")

def launch_provisioning(command):
    os.system(command)

def provision_dev_enviromnt(arguments):
    node_base_name_arg = arguments[2]
    docker_compose_file_path = "dev/docker-compose-dev.yaml"

    try:
        docker_compose_dev_template = Template(filename="dev/docker-compose-dev-tmp.yaml")
        rendered_template = docker_compose_dev_template.render(node_base_name=node_base_name_arg)
        write_rendered_template_to_file(rendered_template, docker_compose_file_path)
        generate_client_dockerfile(node_base_name_arg)
        launch_provisioning("docker-compose -f " + docker_compose_file_path + " up")

    except:
        print("-> error while rendering template")


def provision_prod_enviromnt(arguments):
    node_base_name_arg = arguments[2]
    nodes_number_cluster = int(arguments[3])
    docker_compose_file_path = "prod/docker-compose-prod.yaml"

    try:
        docker_compose_dev_template = Template(filename="prod/docker-compose-prod-tmp.yaml")
        rendered_template = docker_compose_dev_template.render(
            node_base_name=node_base_name_arg,
            nodes_number=nodes_number_cluster
        )
        print("-> docker-compose for prod environment  was generated")
        write_rendered_template_to_file(rendered_template, docker_compose_file_path)
        generate_client_dockerfile(node_base_name_arg)
        launch_provisioning("docker-compose -f " + docker_compose_file_path + " up")
    except:
        print("-> error while rendering template")


arguments = sys.argv
if check_arguments(arguments):
    if arguments[1] == "dev":
        print("-> dev environment elasticsearch provisioning scripts are generating ...")
        provision_dev_enviromnt(arguments)

    if arguments[1] == "prod":
        print("-> prod environment elasticsearch provisioning scripts are generating ...")
        provision_prod_enviromnt(arguments)
