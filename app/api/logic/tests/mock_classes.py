class AutenticationFailedSourceMock:
  def authenticate(self, username, password):
    raise Exception()


class AutenticationNoneSourceMock:
  def authenticate(self, username, password):
    return None


class FetchFailedSourceMock:
  def authenticate(self, username, password):
    return ''
  def fetch(self, auth, start_date, end_date):
    raise Exception()


class FetchNoneSourceMock:
  def authenticate(self, username, password):
    return ''
  def fetch(self, auth, start_date, end_date):
    raise None()


class ParseFailedSourceMock:
  def authenticate(self, username, password):
    return ''
  def fetch(self, auth, start_date, end_date):
    return ''
  def parse(self, html):
    raise Exception()


class ParseNoneSourceMock:
  def authenticate(self, username, password):
    return ''
  def fetch(self, auth, start_date, end_date):
    return ''
  def parse(self, html):
    return None


class ParseValidResponseSourceMock:
  def authenticate(self, username, password):
    return ''
  def fetch(self, auth, start_date, end_date):
    return ''
  def parse(self, html):
    return [{}]