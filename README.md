# About

Pye2e is "framework" for automated tests written in python and gherkin. Project is in an unfinished state! 

## Installing

git clone
virtualenv -p python3 venv  
source venv/bin/active  
pip install -r requirements.txt 

## File structure

/venv/  
/tests/  
/tests/config/  
/tests/data/  
/tests/data/files/  
/tests/features/  
/tests/pages/  

### project_config.py
debug - show traceback and stop tests after first failure  
timout - the max time in which selenium webdriver will wait for elements  
main_url - base url which will be open on start  
custom_wait - additional waiting for loading elements that covers page  

### tests/data/
Here you can store data, for example user_data.py that contains users names, passwords etc.

### tests/data/files/
From this directory you can upload files using upload_file(xpath, file_name) method

### tests/feature/
Here you create .feature files with gherkin scenarios

#### example
Feature: Feature example text
    Scenario: Scenario example text
        Given user is on "homepage" page

### tests/pages/
This is the place where you create your .py files. Write functions, decorate them with @step and add gherkin step into decorator parameter. All defined functions must have a unique name. First argument is driver, you can check list of driver methods below.

#### example

```
from pye2e.step_decorator import step
from tests.data import page_url_data

@step('user is on "{page_name}" page') 
def check_url(driver, page_name):
    driver.check_url(page_url_data.url[page_name])
```
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
upload_file(xpath, file_name)  
wait(seconds)  
refresh_webdriver()  
refresh_page()  


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
