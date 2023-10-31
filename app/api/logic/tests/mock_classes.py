class AutenticationFailedSourceMock:
  identifier = 'TestSource'
  def authenticate(self, username, password):
    raise Exception()


class AutenticationNoneSourceMock:
  identifier = 'TestSource'
  def authenticate(self, username, password):
    return None


class FetchFailedSourceMock:
  identifier = 'TestSource'
  def authenticate(self, username, password):
    return ''
  def fetch(self, auth, start_date, end_date):
    raise Exception()


class FetchNoneSourceMock:
  identifier = 'TestSource'
  def authenticate(self, username, password):
    return ''
  def fetch(self, auth, start_date, end_date):
    raise None()


class ParseFailedSourceMock:
  identifier = 'TestSource'
  def authenticate(self, username, password):
    return ''
  def fetch(self, auth, start_date, end_date):
    return ''
  def parse(self, html):
    raise Exception()


class ParseNoneSourceMock:
  identifier = 'TestSource'
  def authenticate(self, username, password):
    return ''
  def fetch(self, auth, start_date, end_date):
    return ''
  def parse(self, html):
    return None


class ParseValidResponseSourceMock:
  identifier = 'TestSource'
  def authenticate(self, username, password):
    return ''
  def fetch(self, auth, start_date, end_date):
    return ''
  def parse(self, html):
    return [{}]