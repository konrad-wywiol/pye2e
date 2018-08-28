from pye2e.step_decorator import step
from tests.data import page_url_data

search_input_xp = '//input[@id="lst-ib"]'
search_result_xp = '//div[@id="search"]//div[@class="g"]//cite[text()="%s"]'


@step('user searches for "{search_word}"')
def search_for(driver, search_word):
    driver.fill_element(search_input_xp, search_word, enter=True)


@step('site "{site}" should be in results')
def confirm_search_results(driver, site):
    driver.element_is_visible(search_result_xp % page_url_data.url[site])
