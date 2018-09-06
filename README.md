# About
Pye2e is "framework" for automated tests written in python and gherkin. Project is in an unfinished state! 

## Installing
pip install --extra-index-url https://test.pypi.org/simple/ pye2e

## Requirements
python 3   

## Running
create run.py in project/ and write simple script

```
from pye2e import start
from project_config import config


if __name__ == '__main__':
    start(config)
```

## Example
https://github.com/konrad-wywiol/pye2e_example/tree/develop

## File structure
project/project_config.py  
project/steps/  
project/features/  

### project_config.py
debug - show traceback and stop tests after first failure  
timout - the max time in which selenium webdriver will wait for elements  
main_url - base url which will be open on start  
custom_wait - additional waiting for loading elements that covers page  

### feature/
Here you create .feature files with gherkin scenarios. You can add tags to scenarios and features.
@wip - run only these
@disabled - skip 

### tests/steps/
This is the place where you create your .py files with steps. Write functions, decorate them with @step and add gherkin step text into decorator parameter. All defined functions must have a unique name. First argument is driver, you can check list of driver's methods below.

## Webdriver methods:
element_is_visible(xpath)  
element_is_present(xpath)  
element_is_not_visible(xpath)  
element_is_not_present(xpath)  
click(xpath)  
fill_element(xpath, text, enter=False, clear=False)  
open_url(url, add_base_url=True)  
check_url(url, add_base_url=True, check_exactly=False)  
get_text(xpath)  
open_new_window(url)  
close_new_window  
upload_file(xpath, file_path)  
wait(seconds)  
refresh_webdriver()  
refresh_page()  


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
