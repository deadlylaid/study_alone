from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from users.models import User


class OurClientLogInTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        User.objects.create_user(username='MyTestID', password='123', nickname='NICKNAMETEST', phone='01011111111')

    def tearDown(self):
        self.browser.quit()

    def test_our_client_can_log_in_and_create_booksale_this_website(self):

        # 민수는 중고 도서공유 사이트가 있다는 소릴듣고 url접속을 한다.
        self.browser.get(self.live_server_url)

        # 웹 페이지는 헤더가 '남서울 도서공유'를 표시하고 있다.
        self.assertIn('남서울 도서공유', self.browser.title)

        # 메인 페이지에 있는 로그인 버튼을 클릭한다.
        log_in = self.browser.find_element_by_id('log_in')
        log_in.send_keys(Keys.ENTER)
        self.assertIn('로그인', self.browser.title)

        # 로그인 페이지에서 아이디와 비빌번호를 입력하고
        # 확인 버튼을 누른다
        username_box = self.browser.find_element_by_name('username')
        password_box = self.browser.find_element_by_name('password')

        username_box.send_keys('MyTestID')
        password_box.send_keys('123')

        self.browser.find_element_by_id('button').click()
        self.assertIn('남서울 도서공유', self.browser.title)

        # 로그인한 민수는 도서등록 버튼을 누른다
        book_sale = self.browser.find_element_by_id('book_sale')
        book_sale.click()

        bookname_box = self.browser.find_element_by_name('bookname')
        bookprice_box = self.browser.find_element_by_name('bookprice')

        # 책을 등록하고 추가버튼을 누른다
        bookname_box.send_keys('글쓰기와 말하기')
        bookprice_box.send_keys('10000')
        self.browser.find_element_by_name('addlist').send_keys(Keys.ENTER)

        # 두 번째 책을 등록한다
        bookname_box.send_keys('필요없는 도서1')
        self.browser.find_element_by_name('addlist').send_keys(Keys.ENTER)

        # 제목을 쓰고 포스트를 등록한다
        title_box = self.browser.find_element_by_name('title')
        self.browser.find_element_by_id('button').click()

        # 포스트가 등록되면서 포스트 장으로 이동한다
        self.assertIn('판매페이지', self.browser.title)
