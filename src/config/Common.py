import json
import os.path as path

class Common:
    '''
    Common values and constants used over the project
    This method reads the configuration file, 
    database user name and password, and other parameters. 
    '''
    
    def __init__(self):
        #app.config file source
        self.APP_CONFIG_FILE = 'app.config.json'
        self.configuration = self._read_config_file()
        
            
    def _read_config_file(self) -> dict:
        ''' 
        It reads the configuration file app.config.json
        '''
        
        file_path    = path.abspath(__file__)
        dir_config   = path.dirname(file_path)
        dir_src      = path.dirname(dir_config)
        dir_proj     = path.dirname(dir_src)            
        file_path    = path.join(dir_config, self.APP_CONFIG_FILE)
        appconf      = dict()

        try:
            
            with (open(file_path, mode='r', encoding='utf-8')) as f:                
                appconf = json.loads(f.read())
                
            return appconf['Configuration']
        
        except Exception as ex:
            raise FileNotFoundError( f"Could not open the app.config.json file. {ex.args[0]}")
        
    def get_Database(self) -> dict():
        return self.configuration['Database']
    
    def get_TimeZone(self) -> str:        
        return self.configuration['TIMEZONE']
    
    def get_Period_history(self) -> str:
        return self.configuration['Period_history']

    def get_Period_history_unit(self) -> str: 
        return self.configuration['Period_history_unit']

    def get_Stocks_Price_Granularity(self) -> str:
        return self.configuration['Stocks_Price_Granularity']

    def get_File_Name_Date_Format(self) -> str:
        return self.configuration['FILE_NAME_DT_FMT']

    def get_Field_Date_Format(self) -> str:
        return self.configuration['DATA_FIELD_DT_FMT']

