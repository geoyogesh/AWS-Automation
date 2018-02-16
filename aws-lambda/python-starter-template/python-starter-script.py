from pprint import pprint
import utilities


script_name = 'python-starter-script'


def lambda_handler(event, context):
    script_parameters = utilities.read_parameters()
    pprint(script_parameters)

    utilities.config_logging(script_name, str(script_parameters['log_level']))

    # TODO handle exception if script environment is not defined
    config_section = script_parameters['script_environment']
    config_variables = utilities.read_config_file(config_section, script_name)
    utilities.log_info('config parameters....')
    pprint(config_variables)
    if len(config_variables) == 0:
        utilities.log_error('Failed to run {1}.py: Error reading settings from section {0} in file config/{1}.cfg'.format(config_section, script_name))
        return

    utilities.log_info('------------------------------------------------')

    print('completed...')

if __name__ == "__main__":
    lambda_handler(None, None)
